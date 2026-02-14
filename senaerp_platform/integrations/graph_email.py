"""Send emails via Microsoft Graph API instead of SMTP.

Frappe hook: override_email_send
Sends the raw MIME message through the Graph API /sendMail endpoint
over HTTPS (port 443), bypassing SMTP port restrictions.
"""

import base64

import requests

import frappe


GRAPH_SEND_URL = "https://graph.microsoft.com/v1.0/users/{email}/sendMail"
GRAPH_SCOPE = "https://graph.microsoft.com/Mail.Send"


def send_via_graph(queue_doc, sender, recipient, message):
	"""Override email send to use Microsoft Graph API.

	Called by Frappe's email queue when override_email_send hook is set.
	Signature: (queue_doc, sender, recipient, message)
	"""
	email_account = _get_email_account(queue_doc)
	if not email_account:
		frappe.throw("No outgoing Email Account found for Graph API sending")

	access_token = _get_graph_token(email_account)
	if not access_token:
		frappe.throw("Could not obtain Graph API access token")

	email_id = email_account.email_id

	# message is bytes (raw MIME), base64-encode it for Graph API
	if isinstance(message, str):
		message = message.encode("utf-8")
	mime_b64 = base64.b64encode(message).decode("ascii")

	url = GRAPH_SEND_URL.format(email=email_id)
	headers = {
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "text/plain",
	}

	response = requests.post(url, headers=headers, data=mime_b64, timeout=30)

	if response.status_code == 202:
		frappe.logger("email_graph").info(
			f"Email sent via Graph API to {recipient} (queue: {queue_doc.name})"
		)
	else:
		error_detail = response.text[:500]
		frappe.logger("email_graph").error(
			f"Graph API send failed: {response.status_code} - {error_detail}"
		)
		frappe.throw(
			f"Graph API email send failed ({response.status_code}): {error_detail}",
			title="Graph API Error",
		)


def _get_email_account(queue_doc):
	"""Get the Email Account doc for this queue entry."""
	account_name = queue_doc.email_account
	if account_name:
		return frappe.get_doc("Email Account", account_name)

	# Fallback: get the default outgoing account
	default = frappe.db.get_value(
		"Email Account",
		{"enable_outgoing": 1, "default_outgoing": 1},
		"name",
	)
	if default:
		return frappe.get_doc("Email Account", default)

	return None


def _get_graph_token(email_account):
	"""Get a Graph API access token using the Connected App's refresh token.

	Microsoft OAuth refresh tokens can obtain access tokens for different
	resource scopes. We use the existing refresh token (from outlook.office.com
	auth) to request a token scoped for graph.microsoft.com/Mail.Send.
	"""
	if email_account.auth_method != "OAuth" or not email_account.connected_app:
		return None

	connected_app = frappe.get_doc("Connected App", email_account.connected_app)
	user = email_account.connected_user or "Administrator"

	token_cache = connected_app.get_token_cache(user)
	if not token_cache:
		frappe.logger("email_graph").error("No token cache found for Graph API")
		return None

	refresh_token = token_cache.get_password("refresh_token", raise_exception=False)
	if not refresh_token:
		frappe.logger("email_graph").error("No refresh token available")
		return None

	# Request a new access token scoped for Graph API
	token_url = connected_app.token_uri
	client_id = connected_app.client_id
	client_secret = connected_app.get_password("client_secret")

	data = {
		"client_id": client_id,
		"client_secret": client_secret,
		"refresh_token": refresh_token,
		"grant_type": "refresh_token",
		"scope": f"{GRAPH_SCOPE} offline_access",
	}

	response = requests.post(token_url, data=data, timeout=30)

	if response.status_code != 200:
		error = response.json().get("error_description", response.text[:300])
		frappe.logger("email_graph").error(f"Token refresh for Graph failed: {error}")
		return None

	token_data = response.json()

	# Update the refresh token if a new one was issued
	new_refresh = token_data.get("refresh_token")
	if new_refresh and new_refresh != refresh_token:
		token_cache.refresh_token = new_refresh
		token_cache.save(ignore_permissions=True)
		frappe.db.commit()

	return token_data.get("access_token")

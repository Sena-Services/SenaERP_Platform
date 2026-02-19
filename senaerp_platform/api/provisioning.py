# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

import frappe
import subprocess
import re
from frappe import _
from frappe.utils import now


@frappe.whitelist()
def provision_customer_site(subdomain, email=None, company_name=None):
	"""
	Provision a new customer site by calling the onboard-customer.sh script

	Args:
		subdomain (str): The subdomain for the new site (e.g., 'acme' for acme.senaerp.com)
		email (str, optional): Email address to send credentials to
		company_name (str, optional): Company name for the provisioned site

	Returns:
		dict: Site provisioning details including URL and credentials
	"""
	# Validate subdomain
	if not subdomain:
		frappe.throw(_("Subdomain is required"))

	# Clean subdomain: lowercase, alphanumeric and hyphens only
	subdomain = subdomain.lower().strip()
	if not re.match(r'^[a-z0-9-]+$', subdomain):
		frappe.throw(_("Subdomain can only contain lowercase letters, numbers, and hyphens"))

	if len(subdomain) < 3:
		frappe.throw(_("Subdomain must be at least 3 characters"))

	if len(subdomain) > 63:
		frappe.throw(_("Subdomain must be less than 63 characters"))

	# Check if site already exists
	site_name = f"{subdomain}.senaerp.com"
	site_path = f"/home/SenaERP/Application/bench/sites/{site_name}"

	import os
	if os.path.exists(site_path):
		frappe.throw(_(f"Site {site_name} already exists"))

	frappe.logger().info(f"Starting provisioning for subdomain: {subdomain}")

	try:
		# Execute onboarding script directly (Frappe already runs as sentra user)
		script_path = "/home/SenaERP/Application/bench/onboard-customer.sh"

		result = subprocess.run(
			[script_path, subdomain, company_name or subdomain],
			capture_output=True,
			text=True,
			timeout=300,  # 5 minute timeout
			cwd="/home/SenaERP/Application/bench"
		)

		if result.returncode != 0:
			error_msg = result.stderr or result.stdout
			frappe.logger().error(f"Provisioning failed for {subdomain}: {error_msg}")
			frappe.throw(_(f"Provisioning failed: {error_msg}"))

		# Parse output for credentials
		output = result.stdout
		frappe.logger().info(f"Provisioning completed for {subdomain}")

		# Extract admin password from output
		admin_password = None
		for line in output.split('\n'):
			if 'Password:' in line:
				admin_password = line.split('Password:')[-1].strip()
				break

		site_url = f"https://{site_name}"

		# Create or update Provisioned Site record
		doc_name = company_name or subdomain
		if frappe.db.exists("Provisioned Site", doc_name):
			provisioned_site = frappe.get_doc("Provisioned Site", doc_name)
			provisioned_site.update({
				"email": email or "admin@example.com",
				"site_url": site_url,
				"administrator_password": admin_password,
				"status": "Active",
				"provisioned_on": now()
			})
			provisioned_site.save(ignore_permissions=True)
		else:
			provisioned_site = frappe.get_doc({
				"doctype": "Provisioned Site",
				"company_name": doc_name,
				"email": email or "admin@example.com",
				"site_url": site_url,
				"administrator_password": admin_password,
				"status": "Active",
				"provisioned_on": now()
			})
			provisioned_site.insert(ignore_permissions=True)
		frappe.db.commit()

		frappe.logger().info(f"Provisioned Site record created: {provisioned_site.name}")

		# Send credentials email via Graph API (frappe.sendmail hook)
		email_sent = False
		email_error = None
		if email and admin_password:
			try:
				display_name = company_name or subdomain
				frappe.sendmail(
					recipients=[email],
					subject="Welcome to SenaERP - Your Site is Ready!",
					message=_build_provisioning_email(display_name, site_url, admin_password),
					now=True,
				)

				provisioned_site.email_sent = True
				provisioned_site.email_sent_on = now()
				provisioned_site.save(ignore_permissions=True)
				frappe.db.commit()

				email_sent = True
				frappe.logger().info(f"Provisioning email sent to {email}")

			except Exception as email_ex:
				email_error = str(email_ex)
				frappe.logger().error(f"Failed to send provisioning email: {email_error}")
		else:
			frappe.logger().warning(f"Email not sent - email: {email}, password: {'Yes' if admin_password else 'No'}")

		return {
			"success": True,
			"site_url": site_url,
			"site_name": site_name,
			"admin_password": admin_password,
			"provisioned_site_name": provisioned_site.name,
			"email_sent": email_sent,
			"email_error": email_error
		}

	except subprocess.TimeoutExpired:
		frappe.logger().error(f"Provisioning timeout for {subdomain}")
		frappe.throw(_("Provisioning timeout. The process took longer than 5 minutes."))
	except Exception as e:
		frappe.logger().error(f"Provisioning exception for {subdomain}: {str(e)}")
		frappe.throw(_(f"Provisioning failed: {str(e)}"))


def _build_provisioning_email(company_name, site_url, admin_password):
	return f"""
<h2>Welcome to SenaERP!</h2>
<p>Hi {company_name},</p>
<p>Your SenaERP site is ready. Here are your login credentials:</p>
<table style="border-collapse:collapse;margin:20px 0">
<tr><td style="padding:8px 16px;font-weight:600;color:#6b7280">Site URL</td>
<td style="padding:8px 16px"><a href="{site_url}">{site_url}</a></td></tr>
<tr><td style="padding:8px 16px;font-weight:600;color:#6b7280">Username</td>
<td style="padding:8px 16px"><code>Administrator</code></td></tr>
<tr><td style="padding:8px 16px;font-weight:600;color:#6b7280">Password</td>
<td style="padding:8px 16px"><code>{admin_password}</code></td></tr>
</table>
<p><a href="{site_url}" style="display:inline-block;background:#667eea;color:white;
padding:12px 28px;text-decoration:none;border-radius:6px;font-weight:600">
Access Your Site</a></p>
<p><strong>Please change your password after your first login.</strong></p>
<p>Best regards,<br>The SenaERP Team</p>
"""

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


@frappe.whitelist()
def deprovision_customer_site(site_name: str):
	"""
	Fully remove a tenant site by calling deprovision-site.sh on the Application bench.

	Args:
		site_name: The Provisioned Site document name (company_name)

	Returns:
		dict with success status
	"""
	if not site_name:
		frappe.throw(_("Site name is required"))

	if not frappe.db.exists("Provisioned Site", site_name):
		frappe.throw(_(f"Provisioned Site '{site_name}' not found"))

	doc = frappe.get_doc("Provisioned Site", site_name)
	site_url = doc.site_url or ""

	# Extract subdomain from site_url (https://xyz.senaerp.com -> xyz)
	subdomain = site_url.replace("https://", "").replace("http://", "").replace(".senaerp.com", "").strip("/")
	if not subdomain:
		frappe.throw(_("Could not determine subdomain from site URL"))

	frappe.logger().info(f"Starting deprovisioning for site: {subdomain}.senaerp.com")

	try:
		script_path = "/home/SenaERP/Application/bench/deprovision-site.sh"

		result = subprocess.run(
			[script_path, subdomain],
			capture_output=True,
			text=True,
			timeout=120,
			cwd="/home/SenaERP/Application/bench"
		)

		if result.returncode != 0:
			error_msg = result.stderr or result.stdout
			frappe.logger().error(f"Deprovisioning failed for {subdomain}: {error_msg}")
			frappe.throw(_(f"Deprovisioning failed: {error_msg}"))

		frappe.logger().info(f"Site {subdomain}.senaerp.com dropped successfully")

		# Delete the Provisioned Site document
		frappe.delete_doc("Provisioned Site", site_name, force=True)
		frappe.db.commit()

		return {"success": True, "site_name": f"{subdomain}.senaerp.com"}

	except subprocess.TimeoutExpired:
		frappe.logger().error(f"Deprovisioning timeout for {subdomain}")
		frappe.throw(_("Deprovisioning timed out after 2 minutes."))
	except frappe.ValidationError:
		raise
	except Exception as e:
		frappe.logger().error(f"Deprovisioning exception for {subdomain}: {str(e)}")
		frappe.throw(_(f"Deprovisioning failed: {str(e)}"))


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

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
			[script_path, subdomain],
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

		# Create Provisioned Site record
		provisioned_site = frappe.get_doc({
			"doctype": "Provisioned Site",
			"company_name": company_name or subdomain,
			"email": email or "admin@example.com",
			"site_url": site_url,
			"administrator_password": admin_password,
			"status": "Active",
			"provisioned_on": now()
		})
		provisioned_site.insert(ignore_permissions=True)
		frappe.db.commit()

		frappe.logger().info(f"Provisioned Site record created: {provisioned_site.name}")

		# Send email if email is provided
		email_sent = False
		email_error = None
		if email and admin_password:
			try:
				from senaerp_platform.utils.email_sender import send_provisioning_email

				email_response = send_provisioning_email(
					email=email,
					company_name=company_name or subdomain,
					site_url=site_url,
					admin_password=admin_password
				)

				# Update Provisioned Site with email sent status
				provisioned_site.email_sent = True
				provisioned_site.email_sent_on = now()
				provisioned_site.save(ignore_permissions=True)
				frappe.db.commit()

				email_sent = True
				frappe.logger().info(f"Provisioning email sent to {email}")

			except Exception as email_ex:
				email_error = str(email_ex)
				frappe.logger().error(f"Failed to send provisioning email: {email_error}")
				# Don't fail the entire provisioning if email fails
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

# Copyright (c) 2026, Sena and contributors
# For license information, please see license.txt

"""
Accept API
Handles accepting waitlist entries:
- Pitch Deck: sends email with PDF
- Product: enqueues provisioning (shell script on Application bench)
"""

import json
import os
import re
import subprocess

import frappe
from frappe import _
from frappe.utils import now


@frappe.whitelist()
def accept_pitch_deck(waitlist_name):
	"""Send the pitch deck PDF to a waitlist entry and mark as Contacted."""
	doc = frappe.get_doc("Waitlist", waitlist_name)

	if doc.access_type != "Pitch Deck":
		frappe.throw(_("This entry is not a Pitch Deck request"))

	settings = frappe.get_single("Platform Settings")

	if not settings.pitch_deck_file:
		frappe.throw(_("No pitch deck file configured. Upload one in Platform Settings."))

	subject = settings.pitch_deck_email_subject or "SenaERP Pitch Deck"
	body = (settings.pitch_deck_email_body or "").replace(
		"{name}", doc.full_name or ""
	).replace(
		"{company}", doc.company_name or ""
	)

	frappe.sendmail(
		recipients=[doc.email],
		subject=subject,
		message=body,
		attachments=[{"file_url": settings.pitch_deck_file}],
		now=True,
	)

	doc.status = "Contacted"
	doc.save(ignore_permissions=True)
	frappe.db.commit()

	return {"success": True, "message": _("Pitch deck sent to {0}").format(doc.email)}


@frappe.whitelist()
def accept_product(waitlist_name):
	"""
	Start async provisioning for a Product waitlist entry.
	Creates records, then enqueues a background job that runs provision-site.sh.
	"""
	doc = frappe.get_doc("Waitlist", waitlist_name)

	if doc.access_type != "Product":
		frappe.throw(_("This entry is not a Product request"))

	if not doc.company_name:
		frappe.throw(_("Company name is required for provisioning"))

	# Generate subdomain
	subdomain = re.sub(r"[^a-z0-9]", "-", doc.company_name.lower())
	subdomain = re.sub(r"-+", "-", subdomain).strip("-")
	if len(subdomain) < 3:
		frappe.throw(_("Company name is too short to generate a valid subdomain"))
	subdomain = subdomain[:63]

	site_url = f"https://{subdomain}.senaerp.com"
	if frappe.db.exists("Provisioned Site", {"site_url": site_url}):
		frappe.throw(_("A site for {0} already exists").format(subdomain))

	# Verify the provisioning script exists
	app_bench_path = frappe.conf.get("app_bench_path", "/home/SenaERP/Application/bench")
	script_path = os.path.join(app_bench_path, "provision-site.sh")
	if not os.path.isfile(script_path):
		frappe.throw(_("Provisioning script not found at {0}").format(script_path))

	# Create records
	ps = frappe.get_doc({
		"doctype": "Provisioned Site",
		"company_name": doc.company_name,
		"email": doc.email,
		"site_url": site_url,
		"status": "Provisioning",
	})
	ps.insert(ignore_permissions=True)

	doc.status = "Provisioning"
	doc.save(ignore_permissions=True)
	frappe.db.commit()

	# Enqueue
	frappe.enqueue(
		"senaerp_platform.api.accept.run_provisioning",
		queue="long",
		timeout=600,
		subdomain=subdomain,
		email=doc.email,
		company_name=doc.company_name,
		waitlist_name=doc.name,
		provisioned_site_name=ps.name,
	)

	return {"success": True, "message": _("Provisioning started for {0}").format(doc.company_name)}


def run_provisioning(subdomain, email, company_name, waitlist_name, provisioned_site_name):
	"""Background job: calls provision-site.sh <subdomain>, updates records."""
	app_bench_path = frappe.conf.get("app_bench_path", "/home/SenaERP/Application/bench")
	script_path = os.path.join(app_bench_path, "provision-site.sh")
	site_url = f"https://{subdomain}.senaerp.com"

	try:
		result = subprocess.run(
			[script_path, subdomain],
			capture_output=True,
			text=True,
			timeout=600,
		)

		# Script writes JSON to stdout, logs to stderr
		try:
			output = json.loads(result.stdout.strip())
		except (json.JSONDecodeError, ValueError):
			output = {"status": "failed", "error": result.stderr.strip() or result.stdout.strip()}

		if result.returncode != 0 or output.get("status") != "success":
			error_msg = output.get("error") or result.stderr.strip() or "Unknown error"
			raise Exception(error_msg)

		admin_password = output.get("admin_password", "")

		# Success — update records
		ps = frappe.get_doc("Provisioned Site", provisioned_site_name)
		ps.status = "Active"
		# Avoid plaintext credential storage at rest.
		ps.administrator_password = ""
		ps.provisioned_on = now()
		ps.save(ignore_permissions=True)

		wl = frappe.get_doc("Waitlist", waitlist_name)
		wl.status = "Onboarded"
		wl.save(ignore_permissions=True)
		frappe.db.commit()

		# Send welcome email (failure here should not mark the site as failed).
		email_sent = False
		try:
			frappe.sendmail(
				recipients=[email],
				subject="Welcome to SenaERP - Your Site is Ready!",
				message=_build_welcome_email(company_name, site_url, admin_password),
				now=True,
			)
			email_sent = True
		except Exception as mail_err:
			frappe.logger("provisioning").error(
				f"Provisioned {subdomain}.senaerp.com but failed to send welcome email: {mail_err}"
			)

		ps.email_sent = 1 if email_sent else 0
		ps.email_sent_on = now() if email_sent else None
		ps.save(ignore_permissions=True)
		frappe.db.commit()

		frappe.logger("provisioning").info(f"Provisioned {subdomain}.senaerp.com")

	except Exception as e:
		frappe.logger("provisioning").error(f"Provisioning failed for {subdomain}: {e}")
		try:
			ps = frappe.get_doc("Provisioned Site", provisioned_site_name)
			ps.status = "Failed"
			ps.provisioning_error = str(e)
			ps.save(ignore_permissions=True)

			wl = frappe.get_doc("Waitlist", waitlist_name)
			wl.status = "Failed"
			wl.save(ignore_permissions=True)
			frappe.db.commit()
		except Exception as update_err:
			frappe.logger("provisioning").error(f"Failed to update record: {update_err}")


def _build_welcome_email(company_name, site_url, admin_password):
	return f"""
<p>Hi {company_name},</p>

<p>Your SenaERP site is now ready and accessible.</p>

<table style="border-collapse:collapse;margin:16px 0;">
<tr><td style="padding:8px 16px;font-weight:bold;">Site URL</td><td style="padding:8px 16px;"><a href="{site_url}">{site_url}</a></td></tr>
<tr><td style="padding:8px 16px;font-weight:bold;">Username</td><td style="padding:8px 16px;font-family:monospace;">Administrator</td></tr>
<tr><td style="padding:8px 16px;font-weight:bold;">Password</td><td style="padding:8px 16px;font-family:monospace;">{admin_password}</td></tr>
</table>

<p>Please change your password after your first login.</p>

<p>Best regards,<br>The SenaERP Team</p>
"""

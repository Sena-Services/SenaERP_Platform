# Copyright (c) 2026, Sena and contributors
# For license information, please see license.txt

"""
Accept API
Handles accepting waitlist entries — sends pitch deck email for Pitch Deck requests.
"""

import frappe
from frappe import _


@frappe.whitelist()
def accept_pitch_deck(waitlist_name):
	"""
	Send the pitch deck PDF to a waitlist entry and mark as Contacted.

	Args:
		waitlist_name (str): Name of the Waitlist document (e.g. WAIT-00001)

	Returns:
		dict: success status and message
	"""
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

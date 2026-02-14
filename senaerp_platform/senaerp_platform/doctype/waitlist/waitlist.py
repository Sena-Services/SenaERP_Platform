# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from frappe.utils import now_datetime


class Waitlist(Document):
	"""Waitlist Document

	Email notifications are handled by the Frappe Notification "Waitlist Entry"
	which triggers on new documents and sends via the configured Email Account.
	"""

	def before_insert(self):
		if not self.submitted_on:
			self.submitted_on = now_datetime()

# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class Waitlist(Document):
	"""Waitlist Document"""

	def before_insert(self):
		"""Set submitted timestamp before inserting"""
		if not self.submitted_on:
			self.submitted_on = now_datetime()

# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LoginToken(Document):
	def before_insert(self):
		"""Set created_at timestamp before inserting"""
		if not self.created_at:
			self.created_at = frappe.utils.now()

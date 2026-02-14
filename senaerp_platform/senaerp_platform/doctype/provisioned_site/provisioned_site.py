# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ProvisionedSite(Document):
	def before_insert(self):
		"""Set provisioned_on timestamp before inserting"""
		if not self.provisioned_on:
			self.provisioned_on = frappe.utils.now()

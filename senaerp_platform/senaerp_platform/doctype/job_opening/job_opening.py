# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today


class JobOpening(Document):
	"""Job Opening Document"""

	def before_insert(self):
		"""Set posted date before inserting"""
		if not self.posted_date:
			self.posted_date = today()

	def autoname(self):
		"""Set name from title"""
		self.name = self.title

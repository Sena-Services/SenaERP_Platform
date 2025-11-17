# Copyright (c) 2025, Sena and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WebsiteEnvironment(Document):
	def validate(self):
		"""Validate the environment document before saving"""
		# Ensure environment_id is URL-friendly (lowercase, hyphens)
		if self.environment_id:
			self.environment_id = self.environment_id.lower().strip()
			# Replace spaces with hyphens
			self.environment_id = self.environment_id.replace(" ", "-")

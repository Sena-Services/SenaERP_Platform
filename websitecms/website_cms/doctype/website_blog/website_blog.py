# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import os


class WebsiteBlog(Document):
	"""Website Blog Document"""

	def autoname(self):
		"""Set name from title"""
		self.name = self.title

	def before_save(self):
		"""Set route and handle attachment before saving"""
		if not self.route:
			self.route = f"blog/{frappe.scrub(self.title)}"

		# Ensure attachment is public (move from private to public if needed)
		self._ensure_attachment_is_public()

	def _ensure_attachment_is_public(self):
		"""Move attachment from private to public folder if needed"""
		if not self.attachment:
			return

		# Check if attachment is in private folder
		if self.attachment.startswith("/private/files/"):
			try:
				# Get filename
				filename = os.path.basename(self.attachment)

				# Get site paths
				site_path = frappe.get_site_path()
				private_path = os.path.join(site_path, "private", "files", filename)
				public_path = os.path.join(site_path, "public", "files", filename)

				# Copy file to public folder
				if os.path.exists(private_path):
					import shutil
					os.makedirs(os.path.dirname(public_path), exist_ok=True)
					shutil.copy2(private_path, public_path)

					# Update attachment path
					self.attachment = f"/files/{filename}"

					frappe.logger().info(f"Moved attachment to public: {filename}")

			except Exception as e:
				frappe.logger().error(f"Error moving attachment to public: {str(e)}")

	def get_context(self, context):
		"""Build page context for web view"""
		context.no_cache = 0
		context.show_sidebar = False
		return context


@frappe.whitelist(allow_guest=True)
def get_published_blogs(limit=10):
	"""Get published blog posts - accessible to guests"""
	try:
		blogs = frappe.get_all(
			"Website Blog",
			filters={"published": 1},
			fields=["name", "title", "description", "image", "video_url", "blog_id", "published_date", "route"],
			order_by="published_date desc",
			limit=limit
		)

		return {"success": True, "data": blogs}
	except Exception as e:
		frappe.log_error(f"Error fetching blogs: {str(e)}")
		return {"success": False, "error": str(e)}

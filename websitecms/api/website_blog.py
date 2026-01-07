# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

"""
Website Blog API
APIs for managing and retrieving blog posts for the marketing website
"""

import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def get_published_blogs(limit=10, fields=None):
	"""
	Get list of published blog posts

	Args:
		limit (int): Maximum number of blogs to return (default: 10)
		fields (list): List of fields to return (optional)

	Returns:
		dict: Success status and blog data

	Example:
		GET/POST /api/method/sena_backend.api.website_blog.get_published_blogs
		Payload: {"limit": 5}
	"""
	try:
		# Default fields to return
		if not fields:
			fields = [
				"name",
				"title",
				"description",
				"attachment",
				"blog_id",
				"published_date",
				"route",
				"content"
			]

		# Validate limit
		limit = int(limit) if limit else 10
		if limit > 100:
			limit = 100  # Cap at 100 to prevent excessive data transfer

		# Fetch published blogs
		blogs = frappe.get_all(
			"Website Blog",
			filters={"published": 1},
			fields=fields,
			order_by="published_date desc",
			limit=limit
		)

		return {
			"success": True,
			"data": blogs,
			"count": len(blogs)
		}

	except Exception as e:
		frappe.log_error(f"Error fetching published blogs: {str(e)}", "Website Blog API Error")
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to fetch blog posts")
		}


@frappe.whitelist(allow_guest=True)
def get_blog_by_id(blog_id=None, name=None):
	"""
	Get a single blog post by blog_id or name

	Args:
		blog_id (str): Blog ID field value
		name (str): Blog document name

	Returns:
		dict: Success status and blog data

	Example:
		GET/POST /api/method/sena_backend.api.website_blog.get_blog_by_id
		Payload: {"blog_id": "ai-first-erp"}
	"""
	try:
		if not blog_id and not name:
			return {
				"success": False,
				"error": "Either blog_id or name must be provided"
			}

		blog = None

		# Try fetching by blog_id first (if provided and not empty)
		if blog_id:
			blog = frappe.get_all(
				"Website Blog",
				filters={"published": 1, "blog_id": blog_id},
				fields=["*"],
				limit=1
			)

		# If not found by blog_id, try by name
		if not blog and name:
			blog = frappe.get_all(
				"Website Blog",
				filters={"published": 1, "name": name},
				fields=["*"],
				limit=1
			)

		# If still not found and blog_id was provided, try using blog_id as name
		# (in case blog_id field is empty but name matches the identifier)
		if not blog and blog_id:
			blog = frappe.get_all(
				"Website Blog",
				filters={"published": 1, "name": blog_id},
				fields=["*"],
				limit=1
			)

		if not blog:
			return {
				"success": False,
				"error": "Blog post not found",
				"message": _("The requested blog post does not exist or is not published")
			}

		return {
			"success": True,
			"data": blog[0]
		}

	except Exception as e:
		frappe.log_error(f"Error fetching blog by ID: {str(e)}", "Website Blog API Error")
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to fetch blog post")
		}


@frappe.whitelist(allow_guest=True)
def get_blog_count():
	"""
	Get count of published blog posts

	Returns:
		dict: Success status and count

	Example:
		GET/POST /api/method/sena_backend.api.website_blog.get_blog_count
	"""
	try:
		count = frappe.db.count("Website Blog", filters={"published": 1})

		return {
			"success": True,
			"count": count
		}

	except Exception as e:
		frappe.log_error(f"Error getting blog count: {str(e)}", "Website Blog API Error")
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to get blog count")
		}


@frappe.whitelist()
def create_blog(title, description=None, content=None, blog_id=None, attachment=None, published=0):
	"""
	Create a new blog post (requires authentication)

	Args:
		title (str): Blog title (required)
		description (str): Short description
		content (str): Full blog content (HTML)
		blog_id (str): Custom blog ID
		attachment (str): File attachment URL
		published (int): Published status (0 or 1)

	Returns:
		dict: Success status and created blog data

	Example:
		POST /api/method/sena_backend.api.website_blog.create_blog
		Payload: {
			"title": "My New Blog",
			"description": "A brief description",
			"content": "<p>Full content here</p>",
			"attachment": "/files/my-image.jpg",
			"published": 1
		}
	"""
	try:
		# Check permissions
		if not frappe.has_permission("Website Blog", "create"):
			frappe.throw(_("You don't have permission to create blog posts"))

		# Create blog document
		blog = frappe.get_doc({
			"doctype": "Website Blog",
			"title": title,
			"description": description,
			"content": content,
			"blog_id": blog_id,
			"attachment": attachment,
			"published": int(published)
		})

		blog.insert()
		frappe.db.commit()

		return {
			"success": True,
			"data": blog.as_dict(),
			"message": _("Blog post created successfully")
		}

	except Exception as e:
		frappe.log_error(f"Error creating blog: {str(e)}", "Website Blog API Error")
		frappe.db.rollback()
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to create blog post")
		}


@frappe.whitelist()
def update_blog(name, **kwargs):
	"""
	Update an existing blog post (requires authentication)

	Args:
		name (str): Blog document name (required)
		**kwargs: Fields to update

	Returns:
		dict: Success status and updated blog data

	Example:
		POST /api/method/sena_backend.api.website_blog.update_blog
		Payload: {
			"name": "My Blog Title",
			"published": 1,
			"description": "Updated description"
		}
	"""
	try:
		# Check if blog exists
		if not frappe.db.exists("Website Blog", name):
			return {
				"success": False,
				"error": "Blog post not found"
			}

		# Check permissions
		if not frappe.has_permission("Website Blog", "write", name):
			frappe.throw(_("You don't have permission to update this blog post"))

		# Get and update blog
		blog = frappe.get_doc("Website Blog", name)

		# Update allowed fields
		allowed_fields = ["title", "description", "content", "blog_id", "attachment", "published", "published_date", "route"]
		for field, value in kwargs.items():
			if field in allowed_fields:
				blog.set(field, value)

		blog.save()
		frappe.db.commit()

		return {
			"success": True,
			"data": blog.as_dict(),
			"message": _("Blog post updated successfully")
		}

	except Exception as e:
		frappe.log_error(f"Error updating blog: {str(e)}", "Website Blog API Error")
		frappe.db.rollback()
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to update blog post")
		}

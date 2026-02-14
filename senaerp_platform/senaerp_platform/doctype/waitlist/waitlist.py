# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

FROM_EMAIL = "noreply@senaerp.com"
NOTIFICATION_EMAIL = "it@sena.services"
CC_EMAIL = "shelton013@gmail.com"


class Waitlist(Document):
	"""Waitlist Document"""

	def before_insert(self):
		"""Set submitted timestamp before inserting"""
		if not self.submitted_on:
			self.submitted_on = now_datetime()

	def after_insert(self):
		"""Send email notification after new waitlist entry is created"""
		self.send_waitlist_notification()

	def send_waitlist_notification(self):
		"""Send email notification via local Postfix on localhost:25"""
		try:
			subject = f"New Waitlist Entry: {self.full_name}"

			html_message = f"""
<h3>New Waitlist Submission</h3>

<p>A new user has joined the waitlist:</p>

<table style="border-collapse: collapse; width: 100%; max-width: 500px;">
	<tr>
		<td style="padding: 8px; border: 1px solid #ddd;"><strong>Name</strong></td>
		<td style="padding: 8px; border: 1px solid #ddd;">{self.full_name}</td>
	</tr>
	<tr>
		<td style="padding: 8px; border: 1px solid #ddd;"><strong>Email</strong></td>
		<td style="padding: 8px; border: 1px solid #ddd;"><a href="mailto:{self.email}">{self.email}</a></td>
	</tr>
	<tr>
		<td style="padding: 8px; border: 1px solid #ddd;"><strong>Company</strong></td>
		<td style="padding: 8px; border: 1px solid #ddd;">{self.company_name or "N/A"}</td>
	</tr>
	<tr>
		<td style="padding: 8px; border: 1px solid #ddd;"><strong>Phone</strong></td>
		<td style="padding: 8px; border: 1px solid #ddd;">{self.phone or "N/A"}</td>
	</tr>
	<tr>
		<td style="padding: 8px; border: 1px solid #ddd;"><strong>Submitted On</strong></td>
		<td style="padding: 8px; border: 1px solid #ddd;">{self.submitted_on}</td>
	</tr>
	<tr>
		<td style="padding: 8px; border: 1px solid #ddd;"><strong>Reference</strong></td>
		<td style="padding: 8px; border: 1px solid #ddd;">{self.name}</td>
	</tr>
</table>

<p style="margin-top: 20px;">
	<a href="{frappe.utils.get_url()}/app/waitlist/{self.name}"
	   style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">
		View in System
	</a>
</p>
"""

			msg = MIMEMultipart("alternative")
			msg["Subject"] = subject
			msg["From"] = f"SenaERP <{FROM_EMAIL}>"
			msg["To"] = NOTIFICATION_EMAIL
			msg["Cc"] = CC_EMAIL
			msg.attach(MIMEText(html_message, "html"))

			all_recipients = [NOTIFICATION_EMAIL, CC_EMAIL]

			with smtplib.SMTP("localhost", 25) as server:
				server.sendmail(FROM_EMAIL, all_recipients, msg.as_string())

			frappe.logger().info(f"Waitlist notification sent for {self.name} to {NOTIFICATION_EMAIL}")

		except Exception as e:
			frappe.log_error(
				title="Waitlist Email Notification Failed",
				message=f"Failed to send notification for {self.name}: {str(e)}"
			)

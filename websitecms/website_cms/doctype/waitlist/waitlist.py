# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail SMTP Configuration
GMAIL_EMAIL = "noreplysenaerp@gmail.com"
GMAIL_APP_PASSWORD = "vpru egom fvhj fmho"
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
		"""Send email notification via Gmail SMTP"""
		try:
			print(f"📧 [Waitlist] Starting email notification for {self.name}")
			print(f"📧 [Waitlist] From: {GMAIL_EMAIL}")
			print(f"📧 [Waitlist] To: {NOTIFICATION_EMAIL}, CC: {CC_EMAIL}")

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

			# Create email message
			print(f"📧 [Waitlist] Creating email message...")
			msg = MIMEMultipart("alternative")
			msg["Subject"] = subject
			msg["From"] = GMAIL_EMAIL
			msg["To"] = NOTIFICATION_EMAIL
			msg["Cc"] = CC_EMAIL

			# Attach HTML content
			msg.attach(MIMEText(html_message, "html"))
			print(f"📧 [Waitlist] Email message created successfully")

			# Send via Gmail SMTP (include CC in recipients)
			all_recipients = [NOTIFICATION_EMAIL, CC_EMAIL]
			print(f"📧 [Waitlist] Connecting to Gmail SMTP server...")

			with smtplib.SMTP("smtp.gmail.com", 587) as server:
				print(f"📧 [Waitlist] Connected. Starting TLS...")
				server.starttls()
				print(f"📧 [Waitlist] TLS started. Logging in...")
				server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
				print(f"📧 [Waitlist] Logged in successfully. Sending email...")
				server.sendmail(GMAIL_EMAIL, all_recipients, msg.as_string())
				print(f"✅ [Waitlist] Email sent successfully to {all_recipients}")

			frappe.logger().info(f"Waitlist notification sent for {self.name} to {NOTIFICATION_EMAIL}")

		except smtplib.SMTPAuthenticationError as e:
			print(f"❌ [Waitlist] SMTP Authentication Failed: {str(e)}")
			print(f"❌ [Waitlist] Check your Gmail email and app password")
			frappe.log_error(
				title="Waitlist Email - Authentication Failed",
				message=f"Gmail authentication failed for {self.name}: {str(e)}"
			)
		except smtplib.SMTPException as e:
			print(f"❌ [Waitlist] SMTP Error: {str(e)}")
			frappe.log_error(
				title="Waitlist Email - SMTP Error",
				message=f"SMTP error for {self.name}: {str(e)}"
			)
		except Exception as e:
			print(f"❌ [Waitlist] Unexpected error: {str(e)}")
			import traceback
			print(f"❌ [Waitlist] Traceback: {traceback.format_exc()}")
			frappe.log_error(
				title="Waitlist Email Notification Failed",
				message=f"Failed to send notification for {self.name}: {str(e)}"
			)

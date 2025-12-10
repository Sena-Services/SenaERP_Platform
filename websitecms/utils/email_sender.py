# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

import frappe
from postmarker.core import PostmarkClient


def get_postmark_client():
	"""Get Postmark client with API token from site config"""
	api_token = frappe.conf.get('postmark_api_token')

	if not api_token:
		frappe.throw("Postmark API token not configured. Please add 'postmark_api_token' to site_config.json")

	return PostmarkClient(server_token=api_token)


def send_provisioning_email(email, company_name, site_url, admin_password):
	"""
	Send provisioning credentials email via Postmark

	Args:
		email (str): Recipient email address
		company_name (str): Company name
		site_url (str): Full site URL (e.g., https://acme.senaerp.com)
		admin_password (str): Administrator password

	Returns:
		dict: Email send response
	"""
	try:
		client = get_postmark_client()

		# Get sender email from site config, fallback to default
		from_email = frappe.conf.get('postmark_from_email', 'noreply@senaerp.com')

		# Email subject
		subject = f"Welcome to SenaERP - Your Site is Ready!"

		# HTML email body
		html_body = f"""
		<!DOCTYPE html>
		<html>
		<head>
			<style>
				body {{
					font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
					line-height: 1.6;
					color: #333;
					max-width: 600px;
					margin: 0 auto;
					padding: 20px;
				}}
				.header {{
					background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
					color: white;
					padding: 30px;
					text-align: center;
					border-radius: 10px 10px 0 0;
				}}
				.content {{
					background: #f9fafb;
					padding: 30px;
					border-radius: 0 0 10px 10px;
				}}
				.credentials-box {{
					background: white;
					border: 2px solid #e5e7eb;
					border-radius: 8px;
					padding: 20px;
					margin: 20px 0;
				}}
				.credential-item {{
					margin: 15px 0;
				}}
				.credential-label {{
					font-weight: 600;
					color: #6b7280;
					font-size: 14px;
					text-transform: uppercase;
					letter-spacing: 0.5px;
				}}
				.credential-value {{
					font-size: 16px;
					color: #111827;
					margin-top: 5px;
					font-family: 'Courier New', monospace;
					background: #f3f4f6;
					padding: 8px 12px;
					border-radius: 4px;
					display: inline-block;
				}}
				.button {{
					display: inline-block;
					background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
					color: white;
					padding: 14px 32px;
					text-decoration: none;
					border-radius: 6px;
					margin: 20px 0;
					font-weight: 600;
				}}
				.footer {{
					text-align: center;
					color: #6b7280;
					font-size: 14px;
					margin-top: 30px;
					padding-top: 20px;
					border-top: 1px solid #e5e7eb;
				}}
			</style>
		</head>
		<body>
			<div class="header">
				<h1 style="margin: 0;">🎉 Welcome to SenaERP!</h1>
				<p style="margin: 10px 0 0 0; opacity: 0.9;">Your site has been successfully provisioned</p>
			</div>

			<div class="content">
				<p>Hi {company_name},</p>

				<p>Great news! Your SenaERP site is now ready and accessible. Below are your login credentials:</p>

				<div class="credentials-box">
					<div class="credential-item">
						<div class="credential-label">Site URL</div>
						<div class="credential-value">{site_url}</div>
					</div>

					<div class="credential-item">
						<div class="credential-label">Username</div>
						<div class="credential-value">Administrator</div>
					</div>

					<div class="credential-item">
						<div class="credential-label">Password</div>
						<div class="credential-value">{admin_password}</div>
					</div>
				</div>

				<p style="text-align: center;">
					<a href="{site_url}" class="button">Access Your Site →</a>
				</p>

				<p><strong>Important Security Notes:</strong></p>
				<ul>
					<li>Please change your password after your first login</li>
					<li>Store these credentials securely</li>
					<li>Do not share your password with anyone</li>
				</ul>

				<p>If you have any questions or need assistance, please don't hesitate to reach out to our support team.</p>

				<p>Best regards,<br>The SenaERP Team</p>
			</div>

			<div class="footer">
				<p>This email was sent from SenaERP provisioning system</p>
				<p>&copy; 2025 SenaERP. All rights reserved.</p>
			</div>
		</body>
		</html>
		"""

		# Plain text version
		text_body = f"""
Welcome to SenaERP!

Hi {company_name},

Your SenaERP site has been successfully provisioned and is ready to use.

Login Credentials:
------------------
Site URL: {site_url}
Username: Administrator
Password: {admin_password}

IMPORTANT: Please change your password after your first login.

Access your site: {site_url}

If you have any questions, please contact our support team.

Best regards,
The SenaERP Team
		"""

		# Send email via Postmark
		response = client.emails.send(
			From=from_email,
			To=email,
			Subject=subject,
			HtmlBody=html_body,
			TextBody=text_body,
			MessageStream='outbound'
		)

		frappe.logger().info(f"Provisioning email sent to {email} - Message ID: {response['MessageID']}")

		return {
			"success": True,
			"message_id": response.get('MessageID'),
			"to": response.get('To'),
			"submitted_at": response.get('SubmittedAt')
		}

	except Exception as e:
		frappe.logger().error(f"Failed to send provisioning email to {email}: {str(e)}")
		raise

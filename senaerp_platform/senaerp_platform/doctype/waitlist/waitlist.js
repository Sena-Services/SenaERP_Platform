// Copyright (c) 2025, Sentra and contributors
// For license information, please see license.txt

frappe.ui.form.on('Waitlist', {
	refresh: function(frm) {
		if (!frm.is_new() && frm.doc.status === 'Pending') {
			frm.add_custom_button(__('Accept'), function() {
				if (frm.doc.access_type === 'Pitch Deck') {
					accept_pitch_deck(frm);
				} else {
					provision_site(frm);
				}
			});
		}
	}
});

function accept_pitch_deck(frm) {
	frappe.confirm(
		__('Send pitch deck to <b>{0}</b> ({1})?', [frm.doc.full_name, frm.doc.email]),
		function() {
			frappe.call({
				method: 'senaerp_platform.api.accept.accept_pitch_deck',
				args: { waitlist_name: frm.doc.name },
				freeze: true,
				freeze_message: __('Sending pitch deck...'),
				callback: function(r) {
					if (r.message && r.message.success) {
						frm.reload_doc();
						frappe.msgprint({
							title: __('Pitch Deck Sent'),
							message: r.message.message,
							indicator: 'green'
						});
					}
				}
			});
		}
	);
}

function provision_site(frm) {
	// Use company_name as subdomain
	if (!frm.doc.company_name) {
		frappe.msgprint({
			title: __('Missing Company Name'),
			message: __('Company name is required for provisioning'),
			indicator: 'red'
		});
		return;
	}

	// Clean company name to create valid subdomain
	let subdomain = frm.doc.company_name.toLowerCase()
		.replace(/[^a-z0-9]/g, '-')
		.replace(/-+/g, '-')
		.replace(/^-|-$/g, '')
		.substring(0, 63);

	frappe.confirm(
		__('Provision site for {0}?<br><br>Subdomain: <b>{1}.senaerp.com</b><br>Email: <b>{2}</b>',
			[frm.doc.company_name, subdomain, frm.doc.email]),
		function() {
			// Call provisioning API
			frappe.call({
				method: 'senaerp_platform.api.provisioning.provision_customer_site',
				args: {
					subdomain: subdomain,
					email: frm.doc.email,
					company_name: frm.doc.company_name
				},
				freeze: true,
				freeze_message: __('Provisioning site... This may take 3-5 minutes'),
				callback: function(r) {
					if (r.message && r.message.success) {
						// Update Waitlist status and show success
						update_waitlist_status(frm, r.message);
					}
				}
			});
		}
	);
}

function update_waitlist_status(frm, provisioning_data) {
	// Update Waitlist status to Onboarded
	frappe.call({
		method: 'frappe.client.set_value',
		args: {
			doctype: 'Waitlist',
			name: frm.doc.name,
			fieldname: 'status',
			value: 'Onboarded'
		},
		callback: function() {
			frm.reload_doc();

			// Build success message
			let message = __('Site URL: {0}<br>Admin Email: Administrator<br>Password: {1}',
				[provisioning_data.site_url, provisioning_data.admin_password]);

			// Add email status
			if (provisioning_data.email_sent) {
				message += '<br><br>✅ ' + __('Credentials email sent to {0}', [frm.doc.email]);
			} else if (provisioning_data.email_error) {
				message += '<br><br>⚠️ ' + __('Email failed: {0}', [provisioning_data.email_error]);
			} else {
				message += '<br><br>ℹ️ ' + __('Email not sent (no email provided)');
			}

			// Show success message
			frappe.msgprint({
				title: __('Site Provisioned Successfully'),
				message: message,
				indicator: 'green',
				primary_action: {
					label: __('Open Site'),
					action: function() {
						window.open(provisioning_data.site_url, '_blank');
					}
				}
			});
		}
	});
}

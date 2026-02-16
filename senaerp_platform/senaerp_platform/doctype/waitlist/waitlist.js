// Copyright (c) 2025, Sentra and contributors
// For license information, please see license.txt

frappe.ui.form.on('Waitlist', {
	refresh: function(frm) {
		if (!frm.is_new() && frm.doc.status === 'Pending') {
			frm.add_custom_button(__('Accept'), function() {
				if (frm.doc.access_type === 'Pitch Deck') {
					accept_pitch_deck(frm);
				} else {
					accept_product(frm);
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

function accept_product(frm) {
	if (!frm.doc.company_name) {
		frappe.msgprint({
			title: __('Missing Company Name'),
			message: __('Company name is required for provisioning'),
			indicator: 'red'
		});
		return;
	}

	let subdomain = frm.doc.company_name.toLowerCase()
		.replace(/[^a-z0-9]/g, '-')
		.replace(/-+/g, '-')
		.replace(/^-|-$/g, '')
		.substring(0, 63);

	frappe.confirm(
		__('Provision site for {0}?<br><br>Subdomain: <b>{1}.senaerp.com</b><br>Email: <b>{2}</b>',
			[frm.doc.company_name, subdomain, frm.doc.email]),
		function() {
			frappe.call({
				method: 'senaerp_platform.api.accept.accept_product',
				args: { waitlist_name: frm.doc.name },
				freeze: true,
				freeze_message: __('Starting provisioning...'),
				callback: function(r) {
					if (r.message && r.message.success) {
						frm.reload_doc();
						frappe.show_alert({
							message: r.message.message,
							indicator: 'blue'
						}, 5);
					}
				}
			});
		}
	);
}

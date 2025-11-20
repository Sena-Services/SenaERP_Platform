// Copyright (c) 2025, Sentra and contributors
// For license information, please see license.txt

frappe.ui.form.on('Waitlist', {
	refresh: function(frm) {
		// Add Provision button
		if (!frm.is_new()) {
			frm.add_custom_button(__('Provision'), function() {
				frappe.msgprint(__('Provision functionality will be implemented here'));
				// TODO: Add site provisioning logic
			});
		}
	}
});

// Copyright (c) 2025, Sentra and contributors
// For license information, please see license.txt

frappe.ui.form.on('Provisioned Site', {
	refresh(frm) {
		if (frm.is_new()) return;

		frm.add_custom_button(__('Delete Site'), function () {
			const site_url = frm.doc.site_url || '';
			const subdomain = site_url
				.replace('https://', '')
				.replace('http://', '')
				.replace('.senaerp.com', '');

			frappe.confirm(
				__('Permanently delete <b>{0}</b>?<br><br>This will drop the database and remove all site files. This cannot be undone.', [subdomain + '.senaerp.com']),
				function () {
					frappe.call({
						method: 'senaerp_platform.api.provisioning.deprovision_customer_site',
						args: { site_name: frm.doc.name },
						freeze: true,
						freeze_message: __('Deleting site... This may take a minute.'),
						callback(r) {
							if (r.message && r.message.success) {
								frappe.msgprint({
									title: __('Site Deleted'),
									message: __('Site <b>{0}</b> has been fully removed.', [r.message.site_name]),
									indicator: 'green'
								});
								frappe.set_route('List', 'Provisioned Site');
							}
						}
					});
				}
			);
		}, null, 'btn-danger');
	}
});

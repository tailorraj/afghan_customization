// Copyright (c) 2023, Raaj Tailor and contributors
// For license information, please see license.txt

frappe.ui.form.on('Asset Transfer', {
	refresh: function(frm) {
		frm.events.add_custom_buttons(frm);
	},

	add_custom_buttons: function(frm) {
		if (frm.doc.docstatus == 0) {
				frm.add_custom_button(__('Asset Request'), function () {
					if (!frm.doc.transfer_created_by) {
						frappe.throw({
							title: __("Mandatory"),
							message: __("Please Select a User")
						});
					}
					erpnext.utils.map_current_doc({
						method: "afghan_customization.afghan_customization.doctype.asset_request_form.asset_request_form.make_asset_transfer",
						source_doctype: "Asset Request Form",
						target: frm,
						setters: {
							requested_by: frm.doc.transfer_created_by,
						},
						get_query_filters: {
							docstatus: 1,
						}
					})
				}, __("Get Items From"));
		}
	}
});


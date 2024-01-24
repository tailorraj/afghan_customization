// Copyright (c) 2023, Raaj Tailor and contributors
// For license information, please see license.txt

frappe.ui.form.on('Asset Disposal', {
	refresh: function(frm) {

		if(frm.doc.docstatus === 1 && frm.doc.workflow_state !== 'Rejected'){
			frm.add_custom_button(__("Scrap Asset"), function() {
				frappe.confirm(__("Do you really want to scrap this asset?"), function () {
					frappe.call({
						method: "erpnext.assets.doctype.asset.depreciation.scrap_asset",
						args: {
							"asset_name": frm.doc.asset_name
						},
						callback: function(r) {
							// cur_frm.reload_doc();
						}
					})
				})
			});
		}

		frm.set_query('asset_name', () => {
			return {
				filters: {
					status: ['in', ['Submitted','Partially Depreciated']]
				}
			}
		})

	},
	assign:function(frm){

		if(!frm.doc.name){
			frappe.msgprint("Please Save The Document First!")
			return
		}
		
		if(!frm.doc.created_by || !frm.doc.manager){
			frappe.msgprint("Required Created By and Manager Field Data");
			return
		}
		
		frappe.call({
			method: 'afghan_customization.afghan_customization.doctype.asset_disposal.asset_disposal.create_todo',
			args: {
				'self': frm.doc
			},
			freeze: true,
			callback: (r) => {
				console.log(r.message)
			},
			
		})
		
	},
	asset_name:function(frm){
		if(frm.doc.asset_name){
			frappe.db.get_doc('Asset', frm.doc.asset_name)
			.then(doc => {
				console.log(doc)
				frm.set_value('item_code',doc.item_code)
				frm.set_value('asset_tag_no',doc.asset_tag_no)
				frm.set_value('location',doc.location),
				frm.set_value('model',doc.model)
				frm.set_value('make',doc.make)
				frm.set_value('capacity',doc.capacity)
				frm.refresh_field('asset_tag_no','location','make','model','capacity','item_code')
			})
		}
	}
});

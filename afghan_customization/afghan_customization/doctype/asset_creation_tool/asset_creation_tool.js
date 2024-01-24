// Copyright (c) 2023, Raaj Tailor and contributors
// For license information, please see license.txt

frappe.ui.form.on('Asset Creation Tool', {
	refresh: function(frm) {
		frm.add_custom_button('Fetch Assets', () => {
			if(frm.doc.purchase_receipt){

				frappe.call({
					method: 'afghan_customization.afghan_customization.doctype.asset_creation_tool.asset_creation_tool.fetch_assets_from_asset',
					args: {
						'purchase_receipt':frm.doc.purchase_receipt,
					},
					// freeze the screen until the request is completed
					freeze: true,
					callback: (r) => {
						if(r.message.length > 0){
							let count = r.message.length
							frm.set_value('total_qty',count)
							refresh_field('total_qty')
							cur_frm.clear_table("asset_item")
							for (var data of r.message){
								var new_row = frm.add_child("asset_item");
								new_row.asset_id = data.name
							}
							refresh_field("asset_item")
							frm.save()
						}
					}
				})

			}
			else{
				frappe.msgprint("Please Set The Perchase Receipt Data To Perform Action")
			}
			
			
		})
		  frm.add_custom_button('Assign Tag', () => {
			if(frm.doc.initial_tag_no && frm.doc.initiator && frm.doc.total_qty){

				frappe.call({
					method: 'afghan_customization.afghan_customization.doctype.asset_creation_tool.asset_creation_tool.generate_event_tags',
					args: {
						'initial_tag_no':frm.doc.initial_tag_no,
						'initiator':frm.doc.initiator,
						'total_qty':frm.doc.total_qty
					},
					// freeze the screen until the request is completed
					freeze: true,
					callback: (r) => {
						console.log(r.message)
						if(r.message.length > 0){
							// cur_frm.clear_table("asset_item")
							var items = frm.doc.asset_item
	
							if (Object.keys(items).length === r.message.length) {
								// Loop through the dictionary and update the 'name' key with the corresponding list item
								Object.keys(items).forEach((key, index) => {
									items[key].asset_tag_no = r.message[index];
								});
							}
							// for (var data of r.message){
							// 	console.log(data)
							// 	var new_row = frm.add_child("asset_item");
							// 	new_row.asset_tag_no = data
							// }
							frm.refresh_field("asset_item")
							frm.dirty();
							frm.save()
						}
					}
				})

			}
			else{
				frappe.msgprint("Please fill in the required fields before assigning tags.")
			}
			
			
		  }, 'Tag Creation');

		  frm.add_custom_button('Generate Tag', () => {
			frappe.call({
				method: 'afghan_customization.afghan_customization.doctype.asset_creation_tool.asset_creation_tool.create_tag',
				args: {
					'self':frm.doc,
				},
				// freeze the screen until the request is completed
				freeze: true,
				callback: (r) => {
					console.log(r.message)
					
				}
			})
		  }, 'Tag Creation');

	}
});



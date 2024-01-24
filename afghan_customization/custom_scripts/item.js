frappe.ui.form.on('Item', {
	refresh(frm) {
		// your code here
	},
    capex_item_type(frm){
	    if(frm.doc.capex_item_type === 'Goods'){
	        frm.set_value('is_asset_tag_required',1);
	        refresh_field('is_asset_tag_required');
	        
	    }
	},
    fetch_make_model:function(frm,cdt,cdn){
        frappe.call({
            method: 'afghan_customization.afghan_customization.doctype_triggers.item.item.fetch_make_model_data',
            args: {
                'item_name': frm.doc.name
            },
            // freeze the screen until the request is completed
            freeze: true,
            callback: (r) => {
                console.log(r.message)
                if(r.message.length>0){
                    frm.clear_table("custom_item_details"); 
                    for (var i in r.message) {
                        let row = frm.add_child('custom_item_details')
                        row.make = r.message[i].name
                        row.model = r.message[i].model
                        row.capacity = r.message[i].capacity
                    }
                    refresh_field('custom_item_details')
                    frm.save()
                }
                else{
                    frappe.msgprint("No Records Found For This Item: " + frm.doc.name);
                }
            }
        })
    }
});
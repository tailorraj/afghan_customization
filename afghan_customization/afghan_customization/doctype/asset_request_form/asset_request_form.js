// Copyright (c) 2023, Raaj Tailor and contributors
// For license information, please see license.txt

frappe.ui.form.on('Asset Request Form', {
	refresh: function(frm) {

		frm.set_query("asset_tag", "item_request", function(doc, cdt, cdn) {
            console.log("here")
            var d =locals[cdt][cdn]
            
            return {
                query: "afghan_customization.afghan_customization.doctype.asset_request_form.asset_request_form.asset_tag_filter",
                filters:{"item_code": d.item} 
            };
            
        });
		frm.set_query("make", "item_request", function(doc, cdt, cdn) {
            var d =locals[cdt][cdn]
            
            return {
                query: "afghan_customization.afghan_customization.doctype.asset_request_form.asset_request_form.item_make_filter",
                filters:{"item": d.item} 
            };
            
        });

	},
	onload:function(frm){
		frm.set_value("requested_by",frappe.session.user)
		frm.refresh_field('requested_by')
	},
	assign:function(frm){
		// frappe.msgprint("assign button")
		if(frm.doc.name && frm.doc.hod){
			frappe.call({
				method: 'afghan_customization.afghan_customization.doctype.asset_request_form.asset_request_form.create_todo',
				args: {
					'self': frm.doc
				},
				freeze: true,
				callback: (r) => {
					console.log(r.message)
				},
				
			})
		}
		else{
			frappe.msgprint("Required HOD Field Data")
		}
	}
});

frappe.ui.form.on('AWCC Request Item', {
	refresh(frm) {
		// your code here
	},
	
})

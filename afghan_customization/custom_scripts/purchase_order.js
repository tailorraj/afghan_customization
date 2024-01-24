frappe.ui.form.on('Purchase Order', {
    refresh(frm) {
        // your code here
        frm.set_query("make", "items", function(doc, cdt, cdn) {
            
            var d =locals[cdt][cdn]
            
            return {
                query: "afghan_customization.afghan_customization.doctype_triggers.purchase_order.purchase_order.filter_make",
                filters:{"item": d.item_code} 
            };
            
        });

        if(frm.doc.docstatus === 1){
            frm.add_custom_button(__("Create Job Completion Certificate"), ()=> {
                frappe.model.open_mapped_doc({
                    method: "afghan_customization.afghan_customization.doctype_triggers.purchase_order.purchase_order.create_jcc",
                    frm: cur_frm
                })
            });

        }

    }
	
})


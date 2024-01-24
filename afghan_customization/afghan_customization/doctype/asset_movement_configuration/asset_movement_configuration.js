// Copyright (c) 2023, Raaj Tailor and contributors
// For license information, please see license.txt

frappe.ui.form.on('Asset Movement Configuration', {
	refresh: function(frm) {
		frm.set_query("asset", "asset_item", function(doc, cdt, cdn) {
            var d =locals[cdt][cdn]
            
            return {
				query: "afghan_customization.afghan_customization.doctype.asset_movement_configuration.asset_movement_configuration.asset_list_filter",
                filters:{"item": d.item,"make":d.make,"model":d.model,"capacity":d.capacity} 
            };
            
        });

        frm.set_query("asset_tag", "asset_item", function(doc, cdt, cdn) {
            var d =locals[cdt][cdn]
            
            return {
				query: "afghan_customization.afghan_customization.doctype.asset_movement_configuration.asset_movement_configuration.asset_tag_filter",
                filters:{"asset_id": d.asset} 
            };
            
        });
	},
    validate: function(frm){
        
        frm.doc.asset_item.forEach(function(row){
            row.target_location = frm.doc.location
        })
    }
});


frappe.ui.form.on('Asset Movement Configuration Item', {
	refresh: function(frm) {
		
	},
    asset: async function(frm,cdt,cdn){
        var row =locals[cdt][cdn];
        var location_value = await frappe.db.get_value('Asset',row.asset,'location')
        
        frappe.model.set_value(cdt,cdn,'from_location',location_value.message.location)

        refresh_field('asset_item')
    }
});

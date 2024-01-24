frappe.ui.form.on('Stock Entry', {
	refresh(frm) {
		// your code here
	}
});

frappe.ui.form.on('Stock Entry Detail', {
	refresh(frm) {
		// your code here
	},
	fetch_msisdn:function(frm,cdt,cdn){
	    let row = locals[cdt][cdn];
        frappe.call({
            method: 'afghan_customization.afghan_customization.doctype_triggers.stock_entry.stock_entry.get_msisdn_value',
            args: {
                'serials': row.serial_no
            },
            callback:(r) => {
                // on success
                console.log(r.message);
                for(var i in r.message){
                    const serial = r.message[i].serial_name.split("\n");
                    // console.log(serial);
                    const msisdn = r.message[i].msisdn.split("\n");
                    // console.log(msisdn);
                    var html = "<table class='table-bordered'>" +
                    "<thead>" +
							"<tr>" +
								"<th>ICCID NUMBERS</th>" +
								"<th>MSISDN NAME</th>" +
							"</tr>" +
						"</thead>" +
						"<tbody>";
						for(var j in serial){
							html += "<tr>" + 
							"<td>" + serial[j] + "</td>" +
							"<td>" + parseFloat(msisdn[j]) + "</td>" +
							"</tr>";
						}
						html += "</tbody>" +
						"</table>";
						frappe.model.set_value(cdt,cdn,'msisdn',html);
						frm.refresh_field('items');
                }
            }
        });
	}
});
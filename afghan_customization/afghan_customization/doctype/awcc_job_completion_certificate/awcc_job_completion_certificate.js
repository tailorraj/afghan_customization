// Copyright (c) 2023, Raaj Tailor and contributors
// For license information, please see license.txt

frappe.ui.form.on('AWCC Job Completion Certificate', {
	refresh: function(frm) {

	},
	assign:function(frm){
		if(frm.doc.name && frm.doc.hod_approval){
			frappe.call({
				method: 'afghan_customization.afghan_customization.doctype.awcc_job_completion_certificate.awcc_job_completion_certificate.create_todo',
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

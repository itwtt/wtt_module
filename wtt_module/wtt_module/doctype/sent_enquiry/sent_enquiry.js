// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sent Enquiry', {
	club_items:function(frm){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.sent_enquiry.sent_enquiry.club_items",
			args:{
				doc:frm.doc.name
			},
			callback(r){
				frm.reload_doc()
			}
		})
	}
});

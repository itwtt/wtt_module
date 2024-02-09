// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Follow Up', {
	get_follow_up: function(frm) {
		frappe.call({
			method:"wtt_module.wtt_module.doctype.customer_follow_up.customer_follow_up.get_lead",
			args:{
				obj:frm.doc.type
			},
			callback(r){
				msgprint(JSON.stringify(r.message))
			}
		})

	}
});

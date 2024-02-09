// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cash Request', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1)
		{
		if(frappe.session.user == 'venkat@wttindia.com' || frappe.session.user == 'sarnita@wttindia.com' || frappe.session.user == 'karthi@wtt1401.com' || frappe.session.user == 'Administrator' || frappe.session.user == 'nithyanandan@wttindia.com')
		{
			frm.add_custom_button(__('Given'), () => {
			// frm.set_value("cash_status","Given");
			frappe.call({
				method:"wtt_module.wtt_module.doctype.cash_request.cash_request.update_given",
				args:{
					ref_name:frm.doc.name
				},
				callback(r) {
					frm.reload()
					frappe.msgprint("Updated")
				}
			})
			});
			frm.add_custom_button(__('Partially Given'), () => {
			// frm.set_value("cash_status","Partially Given");
			frappe.call({
				method:"wtt_module.wtt_module.doctype.cash_request.cash_request.update_par_given",
				args:{
					ref_name:frm.doc.name
				},
				callback(r) {
					frm.reload()
					frappe.msgprint("Updated")
				}
			})
			});
		}
		}
	}
});

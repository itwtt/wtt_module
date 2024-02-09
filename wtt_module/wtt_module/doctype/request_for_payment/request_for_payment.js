// Copyright (c) 2021, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Request for Payment', {
	refresh: function(frm) {
		frm.add_custom_button(__('Purchase Invoice'),
			function() {
				erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.request_for_payment.request_for_payment.make_request_payment",
					source_doctype: "Purchase Invoice",
					target: frm,
					setters: {
						company: frm.doc.company
					},
					get_query_filters: {
						status: ["=", "Overdue"],
						company: frm.doc.company
					}
				})
		}, __("Get Items From"));
	},
	party:function(frm){
		if(frm.doc.party_type=='Farm Employee'){
			frappe.call({
				"method":"wtt_module.wtt_module.doctype.request_for_payment.request_for_payment.farmemp",
				args:{
					"nn":frm.doc.party
				},
				callback:function(r){
					frm.set_value("employee_name",r.message)
				}
			})
		}
	},
	validate:function(frm){
		if(frappe.session.user!='venkat@wttindia.com'){
		frappe.call({
			"method":"wtt_module.wtt_module.doctype.request_for_payment.request_for_payment.set_emp",
			args:{
				'arr':frappe.session.user
			},
			callback: function(r) {	
				frm.set_value("employee",r.message)
			}
		});
		}
	}
});

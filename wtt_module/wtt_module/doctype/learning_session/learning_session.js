// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Learning Session', {
	setup:function(frm,cdt,cdn){
		frm.set_query("created_by", function() {
		return {
			filters: [
				["Employee","status","=", "Active"],
				]
			}
		})

	},
	created_by:function(frm,cdt,cdn){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.learning_session.learning_session.set_dept",
			args:{
				emp:frm.doc.created_by
			},
			callback(r){
				frm.set_value("department",r.message[0])
			}
		})
	}
	// refresh: function(frm) {

	// }
});

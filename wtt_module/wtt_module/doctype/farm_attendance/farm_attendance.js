// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Farm Attendance', {
	setup: function(frm) {
		frm.set_query("employee", function() {
			return {
				filters: [
					["Farm Employee","status","=", "Active"]
				]
			}
		});
	}
	// status:function(frm){
	// 	frm.set_value("attendance_status",frm.doc.status)
	// }
});

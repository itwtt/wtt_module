// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Checkin Request', {
	refresh: function(frm) {
		frm.add_custom_button("Update Attendance",function(){
			frappe.call({
				method:"update_attendance",
				doc:frm.doc
			})
		})
	}
});

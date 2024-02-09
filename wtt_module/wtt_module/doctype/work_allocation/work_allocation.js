// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Work Allocation', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Task Table', {
	from_time: function(frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn);
	},
	to_time: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		var time_diff = (moment(child.to_time).diff(moment(child.from_time),"seconds")) / ( 60 * 60 * 24);
		var std_working_hours = 0;
		if(frm._setting_hours) return;
		var hours = moment(child.to_time).diff(moment(child.from_time), "seconds") / 3600;
		std_working_hours = time_diff * frappe.working_hours;

		if (std_working_hours < hours && std_working_hours > 0) {
			frappe.model.set_value(cdt, cdn, "hours", std_working_hours);
		} else {
			frappe.model.set_value(cdt, cdn, "hours", hours);
		}
	},
	hours: function(frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn);
	}
});
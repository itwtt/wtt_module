// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Manual Request', {
	from_time: function(frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn);
	},

	to_time: function(frm, cdt, cdn) {
		var time_diff = (moment(frm.doc.to_time).diff(moment(frm.doc.from_time),"seconds")) / ( 60 * 60 * 24);
		var std_working_hours = 0;

		if(frm._setting_hours) return;

		var hours = moment(frm.doc.to_time).diff(moment(frm.doc.from_time), "seconds") / 3600;
		std_working_hours = time_diff * frappe.working_hours;

		if (std_working_hours < hours && std_working_hours > 0) {
			frm.set_value("hours", std_working_hours);
		} else {
			frm.set_value("hours", hours);
		}
	},
	hours: function(frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn);
	}
});


var calculate_end_time = function(frm, cdt, cdn) {
	if(!frm.doc.from_time) {
		// if from_time value is not available then set the current datetime
		frm.set_value("from_time", frappe.datetime.get_datetime_as_string());
	}

	let d = moment(frm.doc.from_time);
	if(frm.doc.hours) {
		var time_diff = (moment(frm.doc.to_time).diff(moment(frm.doc.from_time),"seconds")) / (60 * 60 * 24);
		var std_working_hours = 0;
		var hours = moment(frm.doc.to_time).diff(moment(frm.doc.from_time), "seconds") / 3600;

		std_working_hours = time_diff * frappe.working_hours;

		if (std_working_hours < hours && std_working_hours > 0) {
			frm.set_value("hours", std_working_hours);
			frm.set_value("to_time", d.add(hours, "hours").format(frappe.defaultDatetimeFormat));
		} else {
			d.add(frm.doc.hours, "hours");
			frm._setting_hours = true;
			frm.set_value("to_time",
				d.format(frappe.defaultDatetimeFormat)).then(() => {
				frm._setting_hours = false;
			});
		}
	}
};
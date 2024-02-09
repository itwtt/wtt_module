frappe.ui.form.on('Daily Activity', {
	refresh: (frm) =>{
	frm.add_custom_button('Get filter', () => {
	frappe.call({
            "method": "wtt_module.wtt_module.doctype.daily_activity.daily_activity.get_pending",
            callback: function (r) {
            	
            }
        });
	});
	},
	setup: (frm) => {
		if(!frm.doc.date) {
			frm.set_value("date",frappe.datetime.nowdate());
		}
	},
	onload: function(frm) {
		frm.set_query("project", function() {
			return {
				filters: [
					["Project","status", "!=", "Open"],
					["Project","status", "!=", "Cancelled"],
					["Project","status", "!=", "Completed"]	
				]
			};
		});
	frm.set_query("name_of_designer", function() {
			return {
				filters: [
					["Employee","department", "=", "Design - WTT"]
				]
			};
		});
	}
});

frappe.ui.form.on("Daily Activity Table", {
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
		calculate_time_and_amount(frm);
	}
});

var calculate_end_time = function(frm, cdt, cdn) {
	let child = locals[cdt][cdn];

	if(!child.from_time) {
		// if from_time value is not available then set the current datetime
		frappe.model.set_value(cdt, cdn, "from_time", frappe.datetime.get_datetime_as_string());
	}

	let d = moment(child.from_time);
	if(child.hours) {
		var time_diff = (moment(child.to_time).diff(moment(child.from_time),"seconds")) / (60 * 60 * 24);
		var std_working_hours = 0;
		var hours = moment(child.to_time).diff(moment(child.from_time), "seconds") / 3600;

		std_working_hours = time_diff * frappe.working_hours;

		if (std_working_hours < hours && std_working_hours > 0) {
			frappe.model.set_value(cdt, cdn, "hours", std_working_hours);
			frappe.model.set_value(cdt, cdn, "to_time", d.add(hours, "hours").format(frappe.defaultDatetimeFormat));
		} else {
			d.add(child.hours, "hours");
			frm._setting_hours = true;
			frappe.model.set_value(cdt, cdn, "to_time",
				d.format(frappe.defaultDatetimeFormat)).then(() => {
				frm._setting_hours = false;
			});
		}
	}
};

var calculate_time_and_amount = function(frm) {
var temp = frm.doc.activity;
var i,sum=0
for(i=0;i<temp.length;i++)
{
sum+=temp[i].hours;
}
frm.set_value("total_hours",sum);
};

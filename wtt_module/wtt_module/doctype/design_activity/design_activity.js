// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Design Activity', {
	// refresh: function(frm) {

	// }
	setup: function(frm,cdt,cdn) {
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status","=", "Active"],
					["Employee","department","in","Design - WTT,Proposal - WTT"]
				]
			}

		});
		frm.set_query("project", "activities", function() {
		    return {
				filters: [
					// ["Project","status", "!=", "Open"],
					["Project","status", "!=", "Cancelled"],
					["Project","status", "!=", "Completed"]
				]
			};
		});
		
	},
	preview:function(frm,cdt,cdn){
		frm.set_df_property('hide_table', 'hidden', 0);
		frm.set_df_property('preview', 'hidden', 1);
		var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
		htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>S.NO</th><th style='width:5%'>PROJECT</th><th style='width:5%'>DEPARTMENT</th><th style='text-align:center;width:5%'>SYSTEM</th><th style='width:5%'>TYPE OF DESIGN</th><th style='width:5%'>FROM TIME</th><th style='width:5%'>TO TIME</th><th style='width:5%'>HOURS</th></tr>"
		$.each(frm.doc.activities || [], function(i, v) {
			htvalue+='<tr style="text-align:center;"><td align="center">'+v.idx+'.</td><td align="center">'+v.project+'<br></td><td align="center">'+v.department+'</td><td>'+v.system+'</td><td>'+v.type_of_design+'</td><td>'+v.from_time+'</td><td>'+v.to_time+'</td><td>'+v.hours+'</td></tr>'
		});
		$(frm.fields_dict['html'].wrapper).html(htvalue)
	},
	hide_table:function(frm,cdt,cdn){
		frm.set_df_property('hide_table', 'hidden', 1);
		frm.set_df_property('preview', 'hidden', 0);
		$(frm.fields_dict['html'].wrapper).html("")
	},
	refresh:function(frm,cdt,cdn){
		frm.set_df_property('hide_table', 'hidden', 1);
		frm.set_df_property('preview', 'hidden', 0);
		$(frm.fields_dict['html'].wrapper).html("")
	}

});
frappe.ui.form.on("Design Activity Table", {
	
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
	},
	
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
var temp = frm.doc.activities;
var i,sum=0
for(i=0;i<temp.length;i++)
{
sum+=temp[i].hours;
}
frm.set_value("total_hours",sum);
};
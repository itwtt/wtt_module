// Copyright (c) 2016, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Tracking report"] = {
	"filters": [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
		},
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "Link",
			options: "Project",
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.defaults.get_user_default("year_start_date"),
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.defaults.get_user_default("year_end_date"),
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
       	if(value=="Pending")
       	{
       		value = '<b style="color: red;">'+value+'</b>';
       	}
       	else if(value=="To Bill")
       	{
       		value = '<b style="color: green;">'+value+'</b>';
       	}
       	else if(value=="To Receive and Bill")
       	{
       		value = '<b style="color: #20B2AA;">'+value+'</b>';
       	}
       	else if(value=="Submitted")
       	{
       		value = '<b style="color: orange;">'+value+'</b>';
       	}
       	else if(value=="Draft")
       	{
       		value = '<b style="color:cornflowerblue;">'+value+'</b>';
       	}
       	return value
    }
};

// Copyright (c) 2016, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Material Tracking"] = {
	"filters": [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
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
			default: frappe.datetime.get_today(),
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
       	if(value=="Pending" || value=="Stopped")
       	{
       		value = '<b style="color: red;">'+value+'</b>';
       	}
       	else if(value=="Received")
       	{
       		value = '<b style="color: green;">'+value+'</b>';
       	}
       	else if(value=="Ordered")
       	{
       		value = '<b style="color: #20B2AA;">'+value+'</b>';
       	}
       	else if(value=="Partially Ordered")
       	{
       		value = '<b style="color: orange;">'+value+'</b>';
       	}
       	else if(value=="To Received and Bill")
       	{
       		value = '<b style="color: #F7CB73;">'+value+'</b>';
       	}
       	else if(value=="To Bill")
       	{
       		value = '<b style="color: #077E8C;">'+value+'</b>';
       	}
       	else if(value=="Partially Received")
       	{
       		value = '<b style="color: lightgreen;">'+value+'</b>';
       	}
       	else if(value=="Draft")
       	{
       		value = '<b style="color:cornflowerblue;">'+value+'</b>';
       	}
       	else if(value=="Submitted")
       	{
       		value = '<b style="color:#FFD700;">'+value+'</b>';
       	}
       	return value
    },
    get_datatable_options(options) {
        return Object.assign(options, {
            checkboxColumn: true
        });
    }
};

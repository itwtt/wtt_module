// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Rest Eligible Leaves"] = {
	"filters": [
		{
			"fieldname":"month",
			"label": __("Month"),
			"fieldtype": "Select",
			"width": "80",
			"options": ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		},
		{
			"fieldname":"purpose",
			"label": __("List Of"),
			"fieldtype": "Select",
			"width": "80",
			"options": ["Not applied for leave","Uninformed Leave"]
		},
		{
			"fieldname":"leavetype",
			"label": __("Leave Type"),
			"fieldtype": "Select",
			"width": "80",
			"options": ['','Eligible Leave','Leave Without Pay','Sick Leave','Emergency Leave']
		},
		{
			"fieldname":"department",
			"label": __("Department"),
			"fieldtype": "Link",
			"width": "80",
			"options":"Department"
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
       	if(value=="Punch Missed")
       	{
       		value = '<b style="color: random;">'+value+'</b>';
       	}
       	
       	return value
    }
};

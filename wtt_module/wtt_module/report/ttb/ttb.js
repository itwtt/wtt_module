// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["TTB"] = {
	"filters": [
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options":"Employee",
			"width": "80",
			"hidden":1
		},
		{
			"fieldname":"year",
			"label": __("Year"),
			"fieldtype": "Int",
			"width": "80",
			"default":"2023"
			// "hidden":1
		},
		{
			"fieldname":"month",
			"label": __("Month"),
			"fieldtype": "Select",
			"options":["January","February","March","April","May","June","July","August","September","October","November","December"],
			"default":"January",
			"width": "80"
		},
		// {
		// 	"fieldtype":"Check",
		// 	"label":"Overall Average",
		// 	"fieldname":"avg"
		// },
		{
			"fieldtype":"Check",
			"label":"Pending Employees",
			"fieldname":"pending_emp"
		},
	]
};



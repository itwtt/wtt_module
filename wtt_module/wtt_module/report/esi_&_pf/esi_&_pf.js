// Copyright (c) 2016, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["ESI & PF"] = {
	"filters": [
		{
			"label":"Month",
			"fieldname":"month",
			"fieldtype":"Select",
			"options":["January","February","March","April","May","June","July","August","September","October","November","December"],
			"default":"January"
		},
		{
			"label":"Year",
			"fieldname":"year",
			"fieldtype":"Int",
			"default":"2023"
		},
		{
			"label":"Branch",
			"fieldname":"branch",
			"fieldtype":"Link",
			"options":"Branch"
		}
	]
};

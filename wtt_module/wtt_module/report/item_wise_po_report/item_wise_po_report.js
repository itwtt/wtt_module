// Copyright (c) 2016, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item Wise PO report"] = {
	"filters": [
	{
		"fieldname":"from_date",
		"label": __("From Date"),
		"fieldtype": "Date",
		"default": new Date(new Date().getFullYear(),new Date().getMonth()-1,1),
	},
	{
		"fieldname":"to_date",
		"label": __("To Date"),
		"fieldtype": "Date",
		"default":new Date(new Date().getFullYear(),new Date().getMonth(),0),
	},
	{
		"label":"Project",
		"fieldname":"project",
		"fieldtype":"Link",
		"options":"Project",
		"width":100
	},
	{
		"label":"Workflow",
		"fieldname":"workflow",
		"fieldtype":"Link",
		"options":"Workflow State",
		"default":"Approved",
		"width":100
	}
	]
};

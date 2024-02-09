// Copyright (c) 2016, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Balance Eligible Leave"] = {
	"filters": [
	{
		"label":"Employee",
		"fieldtype":"Link",
		"fieldname":"employee",
		"options":"Employee",
		"width":100
	},
	{
		"label":"From Date",
		"fieldtype":"Date",
		"fieldname":"from_date",
		"default":new Date(new Date().getFullYear(),new Date().getMonth()-1,1),
		"width":100
	},
	{
		"label":"To Date",
		"fieldtype":"Date",
		"fieldname":"to_date",
		"default":new Date(new Date().getFullYear(),new Date().getMonth(),0),
		"width":100
	}
	]
};

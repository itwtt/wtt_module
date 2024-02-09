// Copyright (c) 2016, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PO not in PR"] = {
	"filters": [
	{
		"label":"Project",
		"fieldtype":"Link",
		"fieldname":"project",
		"options":"Project"
	},
	{
		"label":"Start Date",
		"fieldtype":"Date",
		"fieldname":"start_date"
	},
	{
		"label":"End Date",
		"fieldtype":"Date",
		"fieldname":"end_date"
	}
]
};

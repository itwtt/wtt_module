// Copyright (c) 2024, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Approved MR List"] = {
	"filters": [
		{
			"label":"Material Request",
			"fieldname":"mr_no",
			"fieldtype":"Link",
			"options":"Material Request"
		},
		{
			"label":"Project",
			"fieldname":"project",
			"fieldtype":"Link",
			"options":"Project"
		},
		{
			"label":"Group By",
			"fieldname":"group_by",
			"fieldtype":"Select",
			"options":["","MR Wise","Item Wise"],
			"default":"MR Wise"
		}
	]
};

// Copyright (c) 2016, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["MR, PO, Project"] = {
	"filters": [
	{
		"label":"Project",
		"fieldname":"project",
		"fieldtype":"Link",
		"options":"Project",
		"reqd":1
	},
	{
		"label":"Material Request",
		"fieldname":"mr",
		"fieldtype":"Link",
		"options":"Material Request"
	}
	]
};

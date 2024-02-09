// Copyright (c) 2016, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["MR not in PO"] = {
	"filters": [
	{
		"label":"Material Request",
		"fieldtype":"Link",
		"fieldname":"mr_no",
		"options":"Material Request"
	},
	{
		"label":"Item Group",
		"fieldtype":"Link",
		"fieldname":"item_group",
		"options":"Item Group"
	}
	]
};

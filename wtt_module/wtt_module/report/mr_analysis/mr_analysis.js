// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["MR Analysis"] = {
	"filters": [
	{
		"label":"Project",
		"fieldname":"project",
		"fieldtype":"Link",
		"options":"Project",
		"default":"WTT-0450",
		"reqd":1
	},
	{
		"label":"Unlinked",
		"fieldtype":"Check",
		"fieldname":"unlinked",
		"default":"1"
	},
	{
		"label":"Club",
		"fieldtype":"Check",
		"fieldname":"club",
		"default":"1"
	}


	]
};

// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["MR Details"] = {
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
		"label":"Group by",
		"fieldname":"group_by",
		"fieldtype":"Select",
		"options":["Description","Item Group"],
		"reqd":1
	}
	]
};

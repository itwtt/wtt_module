// Copyright (c) 2024, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Leave Status"] = {
	"filters": [
		{
			"label":"Employee",
			"fieldname":"employee",
			"fieldtype":"Link",
			"options":"Employee"
		},
		{
			"label":"Leave Type",
			"fieldname":"leave_type",
			"fieldtype":"Select",
			"options":["","Sick Leave","Casual Leave"],
			"default":"Casual Leave"
		}
	]
};

// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Basic Salary Report"] = {
	"filters": [
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options":"Employee",
			"width": "100px"
		},
		{
		    "fieldname": "from_date",
		    "label": __("From"),
		    "fieldtype": "Date",
		    "default": new Date(new Date().getFullYear() - 1, 0, 1),
		    "reqd": 1,
		    "width": "100px"
		},
		{
		    "fieldname": "to_date",
		    "label": __("To"),
		    "fieldtype": "Date",
		    "default": new Date(new Date().getFullYear() - 1, 11, 31),
		    "reqd": 1,
		    "width": "100px"
		},
		{
			"fieldname":"branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Branch",
			"width": "80px"
		}
	]
};

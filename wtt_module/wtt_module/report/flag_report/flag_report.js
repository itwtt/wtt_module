// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Flag Report"] = {
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
		  "label": "From",
		  "fieldtype": "Date",
		  "default": new Date(new Date().getFullYear(), new Date().getMonth() - 1, 1),
		  "reqd": 1,
		  "width": "100px"
		},
		{
		  "fieldname": "to_date",
		  "label": "To",
		  "fieldtype": "Date",
		  "default": new Date(new Date().getFullYear(), new Date().getMonth(), 0),
		  "reqd": 1,
		  "width": "100px"
		}
	]
};

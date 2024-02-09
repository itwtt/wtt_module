// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Credit Debit Report"] = {
	"filters": [
		{
			"label":"Entry Type",
			"fieldname":"en_type",
			"fieldtype":"Select",
			"options":["","Journal Entry","Bank Entry","Cash Entry"],
			"default":"Cash Entry"
		},
		{
		    "fieldname": "from_date",
		    "label": __("From"),
		    "fieldtype": "Date",
		    "default": new Date(new Date().getFullYear() - 1, 3, 1), // April 1st of the last fiscal year
		    "reqd": 1,
		    "width": "100px"
		},
		{
		    "fieldname": "to_date",
		    "label": __("To"),
		    "fieldtype": "Date",
		    "default": new Date(new Date().getFullYear(), 3, 0), // March 31st of the current year
		    "reqd": 1,
		    "width": "100px"
		}
	]
};

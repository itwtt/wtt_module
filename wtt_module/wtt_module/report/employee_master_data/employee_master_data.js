// Copyright (c) 2016, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Master Data"] = {
	"filters": [
		{
			"fieldname":"emp",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options":"Employee"
		},
		{
			"fieldname":"dept",
			"label": __("Department"),
			"fieldtype": "Link",
			"options":"Department"
		},
		{
			"fieldname":"branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options":"Branch"
		}
	]
};

// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PMS"] = {
	"filters": [
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options":"Employee",
			"width": "80",
			"hidden":1
		},
		{
			"fieldname":"year",
			"label": __("Year"),
			"fieldtype": "Int",
			"width": "80",
			"default":"2023"
			// "hidden":1
		},
		{
			"fieldname":"category",
			"label": __("category"),
			"fieldtype": "Select",
			"options":["Target","Technical","Behavioural"],
			"default":"Technical",
			"width": "80"
		},
	],
	onload: function(report) {
		report.page.add_inner_button(__("Breakup Score"), function() {
			var filters = report.get_values();
			frappe.set_route('query-report', 'TTB');
		});
	}
};



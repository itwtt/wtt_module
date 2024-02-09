// Copyright (c) 2024, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Activity"] = {
	"filters": [
		{
		"fieldname": "emp",
		"label": __("Employee"),
		"fieldtype": "Link",
		"options": "Employee"
		},
		{
			"fieldname": "dept",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department"
		},
		{
			"fieldname": "date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default":frappe.datetime.add_days(frappe.datetime.get_today(), -1)
		}
	]
};

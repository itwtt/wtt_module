// Copyright (c) 2016, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly Checkin"] = {
	"filters": [
		{
			"fieldname":"emp",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options":"Employee"
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default":new Date(new Date().getFullYear(),new Date().getMonth(),1)
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": new Date(new Date().getFullYear(),new Date().getMonth()+1,0)
		}

	]
};

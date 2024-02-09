// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Combined Leave"] = {
	"filters": [
		{
			"label":"Day",
			"fieldname":"day_name",
			"fieldtype":"Select",
			"options":["Saturday","Monday","Both"],
			"default":"Both"
		},
		{
			"label":"Total",
			"fieldname":"total",
			"fieldtype":"Check",
			"default":1
		},
		// {
		// 	"label":"Count",
		// 	"fieldname":"count",
		// 	"fieldtype":"Int"
		// }
	]
};

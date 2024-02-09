// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Missing Task"] = {
	"filters": [
	{
		"label":"From Date",
		"fieldname":"from_date",
		"fieldtype":"Date",
		"default":'2023-02-14'
	},
	{
		"label":"TO Date",
		"fieldname":"to_date",
		"fieldtype":"Date",
		"default":new Date()
	}
	]
};

// // Copyright (c) 2022, wtt_module and contributors
// // For license information, please see license.txt
// /* eslint-disable */

frappe.query_reports["Follow Up"] = {
	"filters": [
	{
		"label":"Date",
		"fieldtype":"Date",
		"fieldname":"date"
	},
	{
		"label":"Organization",
		"fieldtype":"Data",
		"fieldname":"organization"
	},
	{
		"label":"Next Follow Up Date",
		"fieldtype":"Date",
		"fieldname":"next_follow_up_date"
	},
	{
		"label":"Reports for",
		"fieldtype":"Select",
		"fieldname":"reports_for",
		"options":["--Select--","trading@wttindia.com","raghul@wttindia.com"]
	}

	]
};


// frappe.query_reports["Follow Up"] = {
// 	"filters": [
// 	{
// 		"label":"From Date",
// 		"fieldtype":"Date",
// 		"fieldname":"from_date",
// 		"default": frappe.datetime.get_today()
// 	},
// 	{
// 		"label":"To Date",
// 		"fieldtype":"Date",
// 		"fieldname":"to_date",
// 		"default": frappe.datetime.get_today()
// 	}
// 	]
// };

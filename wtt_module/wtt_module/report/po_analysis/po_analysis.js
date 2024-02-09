// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PO Analysis"] = {
	"filters": [
	{
		"label":"GROUP BY",
		"fieldname":"group_by",
		"fieldtype":"Select",
		"options":["Supplier","Purchase Order"]
	},
	{
		"label":"FROM DATE",
		"fieldtype":"Date",
		"fieldname":"from_date",
		"default":frappe.defaults.get_user_default("year_start_date")
	},
	{
		"label":"TO DATE",
		"fieldtype":"Date",
		"fieldname":"to_date",
		"default":frappe.defaults.get_user_default("year_end_date")
	},
	{
		"label":"Based on Project",
		"fieldtype":"Check",
		"fieldname":"project"
	},
	{
		"label":"Project",
		"fieldtype":"Link",
		"fieldname":"project_name",
		"options":"Project"
	}

	]
};

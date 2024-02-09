// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Cost Supplier Wise"] = {
	"filters": [
		{
		"label":"Project",
		"fieldtype":"Link",
		"fieldname":"project_name",
		"options":"Project"
		},
		{
		"label":"Report Type",
		"fieldtype":"Select",
		"fieldname":"report_type",
		"options":["--Select--","Supplier Wise","PO Wise"],
		"default":"PO Wise"
		}
	]
};

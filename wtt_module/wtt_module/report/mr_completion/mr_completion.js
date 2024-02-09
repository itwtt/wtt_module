// Copyright (c) 2024, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["MR Completion"] = {
	"filters": [
		{
			"label":"Material Request",
			"fieldname":"mr_no",
			"fieldtype":"Link",
			"options":"Material Request",
			"get_query": function() {
				return {
					filters: {
						"docstatus": 1
					}
				};
			}
		},
		{
			"label":"Project",
			"fieldname":"project",
			"fieldtype":"Link",
			"options":"Project",
			"get_query": function() {
				return {
					filters: {
						"status": "On going"
					}
				};
			}
		},
		{
			"label":"Group By",
			"fieldname":"group_by",
			"fieldtype":"Select",
			"options":["","MR Wise","Item Wise"],
			"default":"MR Wise"
		},
		{
			"label":"Status",
			"fieldname":"status",
			"fieldtype":"Select",
			"options":["","Pending","Partially Ordered","Ordered","Partially Received","Received"],
			"default":"MR Wise"
		},
		{
			"label":"Not Ordered",
			"fieldname":"not_ordered",
			"fieldtype":"Check"
		}
	]
};

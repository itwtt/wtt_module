// Copyright (c) 2024, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Purchase Lead Time"] = {
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
		}
	]
};

// Copyright (c) 2024, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Available Items"] = {
	"filters": [
		{
			"label":"Project",
			"fieldname":"project",
			"fieldtype":"Link",
			"options":"Project",
			"default":"WTT-0450",
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

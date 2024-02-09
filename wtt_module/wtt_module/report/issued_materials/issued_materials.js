// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Issued Materials"] = {
	"filters": [
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "Link",
			options: "Project",
			default:"WTT-0357"
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: ['','Issued','Not Issued']
		}
	]
};

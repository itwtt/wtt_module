// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Material Tracking"] = {
	"filters": [
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "Link",
			options: "Project",
			default:"WTT-0357"
		},
		{
			fieldname: "material_request",
			label: __("Material Request"),
			fieldtype: "Link",
			options: "Material Request",
		}
	]
};

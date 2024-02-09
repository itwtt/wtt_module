// Copyright (c) 2024, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Leave Balance"] = {
	"filters": [
			{
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
			"get_query": function() {
				return {
					filters: {
						"status": "Active"
					}
				};
			}
		},
		{
			fieldname: "department",
			label: __("Department"),
			fieldtype: "Link",
			options: "Department"
		},
		{
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Link",
			options: "Branch"
		}
	],
	 onload: function() {
	 	frappe.query_report.page.add_inner_button(__("Allocate"), function() {
	 		var selected_rows = [];
	 		var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			for(i in v)
			{
	 		if(frappe.query_report.data[parseInt(v[i])].employee!=undefined)
	 	 	{
		 		selected_rows.push({
		 			"employee":frappe.query_report.data[parseInt(v[i])].employee,
		 			"total_earn":frappe.query_report.data[parseInt(v[i])].total_earn,
		 			"total_sick":frappe.query_report.data[parseInt(v[i])].total_sick,
		 			"experience":frappe.query_report.data[parseInt(v[i])].experience,
		 			"after_six":frappe.query_report.data[parseInt(v[i])].after_six
		 		})

	 		}
	 		}
			frappe.call({
	 			"method":"wtt_module.wtt_module.report.leave_balance.leave_balance.function",
	 			args:{
	 				"rows":selected_rows
				}
	 		})
	 	});
	},
	get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true
		});
	}
};

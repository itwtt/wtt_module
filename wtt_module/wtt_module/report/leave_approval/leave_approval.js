// Copyright (c) 2016, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Leave approval"] = {
	"filters": [
		{
			"fieldname":"emp",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options":"Employee"
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default":new Date(new Date().getFullYear(),new Date().getMonth()+1,1)
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": new Date(new Date().getFullYear(),new Date().getMonth()+2,0)
		}
	],
	onload: function() {
		frappe.query_report.page.add_inner_button(__("Approve"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			for(i in v)
			{
			if(frappe.query_report.data[parseInt(v[i])].name!=undefined)
		 	{
		 		//alert(frappe.query_report.data[parseInt(v[i])].name)
			frappe.call({
				"method":"wtt_module.wtt_module.report.leave_approval.leave_approval.function",
				args:{
					"lr_name":frappe.query_report.data[parseInt(v[i])].lr_name
				}
			})
			}
			}		
		});
		// frappe.query_report.page.add_inner_button("Reject", ()=>{debugger;})
		
		frappe.query_report.page.add_inner_button(__("Reject"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			for(i in v)
			{
			if(frappe.query_report.data[parseInt(v[i])].name!=undefined)
		 	{
		 		//alert(frappe.query_report.data[parseInt(v[i])].name)
			frappe.call({
				"method":"wtt_module.wtt_module.report.leave_approval.leave_approval.func",
				args:{
					"lt_name":frappe.query_report.data[parseInt(v[i])].name
				}
			})
			}
			}		
		});
	},
	get_datatable_options(options) {
        return Object.assign(options, {
            checkboxColumn: true
        });
    }
};

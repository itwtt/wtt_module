// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Expense"] = {
	"filters": [
		{
			"fieldname":"account",
			"label": __("Account"),
			"fieldtype": "Link",
			"options":"Account"
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default":new Date("2022-04-01")
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": new Date("2023-03-31")
		}
	],
	
	onload: function() {
		frappe.query_report.page.add_inner_button(__("Approve"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			for(i in v)
			{
			if(frappe.query_report.data[parseInt(v[i])].ref!=undefined)
		 	{
		 		// alert(frappe.query_report.data[parseInt(v[i])].ref)
			frappe.call({
				"method":"wtt_module.wtt_module.report.expense.expense.function",
				args:{
					"lr_name":frappe.query_report.data[parseInt(v[i])].ref
				},
				callback: function(r) {
						msgprint("Approved")
						report.refresh();
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
			if(frappe.query_report.data[parseInt(v[i])].ref!=undefined)
		 	{
		 		//alert(frappe.query_report.data[parseInt(v[i])].name)
			frappe.call({
				"method":"wtt_module.wtt_module.report.expense.expense.func",
				args:{
					"lt_name":frappe.query_report.data[parseInt(v[i])].ref
				},
				callback: function(r) {
					msgprint("Rejected")
						report.refresh();
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

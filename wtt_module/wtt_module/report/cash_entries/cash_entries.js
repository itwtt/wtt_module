// Copyright (c) 2016, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cash Entries"] = {
"filters": [
		{
			"fieldname":"payment_type",
			"label": __("Payment Type"),
			"fieldtype": "Select",
			"options":["--Select--","Pay","Receive"],
			"default":"--Select--"
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options":"Company",
			"default":"WTT INTERNATIONAL PVT LTD"
		}
	],

	
	onload: function() {
		frappe.query_report.page.add_inner_button(__("Approve"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			for(i in v)
			{
			if(frappe.query_report.data[parseInt(v[i])].journal_entry!=undefined)
		 	{
			frappe.call({
				"method":"wtt_module.wtt_module.report.cash_entries.cash_entries.function",
				args:{
					"lr_name":frappe.query_report.data[parseInt(v[i])].journal_entry
				}
			})
			}
			}		
		});		
		frappe.query_report.page.add_inner_button(__("Cancel"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			for(i in v)
			{
			if(frappe.query_report.data[parseInt(v[i])].journal_entry!=undefined)
		 	{
			frappe.call({
				"method":"wtt_module.wtt_module.report.cash_entries.cash_entries.func",
				args:{
					"lt_name":frappe.query_report.data[parseInt(v[i])].journal_entry
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


// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Salary Approval"] = {
	"filters": [
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options":"Employee",
			"width": "100px"
		},
		{
			"fieldname":"from_date",
			"label": __("From"),
			"fieldtype": "Date",
			"default": new Date(new Date().getFullYear(),new Date().getMonth()-1,1),
			"reqd": 1,
			"width": "100px"
		},
		{
			"fieldname":"to_date",
			"label": __("To"),
			"fieldtype": "Date",
			"default": new Date(new Date().getFullYear(),new Date().getMonth(),0),
			"reqd": 1,
			"width": "100px"
		},
		{
			"fieldname": "currency",
			"fieldtype": "Link",
			"options": "Currency",
			"label": __("Currency"),
			"default": erpnext.get_currency(frappe.defaults.get_default("Company")),
			"width": "50px"
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"width": "100px",
			"reqd": 1
		},
		{
			"fieldname":"branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Branch",
			"width": "80px"
		},
		{
			"fieldname":"docstatus",
			"label":__("Document Status"),
			"fieldtype":"Select",
			"options":["Draft", "Submitted", "Cancelled"],
			"default": "Draft",
			"width": "100px"
		},
		{
			"fieldname":"workflow_state",
			"label":__("Workflow status"),
			"fieldtype":"Select",
			"options":["","Verified by HR", "Verified by GM", "Rejected"],
			"width": "100px"
		}
	],
	onload: function() {
		if(frappe.session.user=='venkat@wttindia.com')
		{
			var year_filter = frappe.query_report.get_filter('workflow_state');
			year_filter.df.options = ["","Verified by HR", "Verified by GM", "Rejected"];
			year_filter.df.default = "Verified by GM";
			year_filter.refresh();
			year_filter.set_input(year_filter.df.default);
		}
		else
		{
			filt=""
		}
		frappe.query_report.page.add_inner_button(__("Approve"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			for(i in v)
			{
		 	//alert(frappe.query_report.data[v[i]].salary_slip)
			frappe.call({
				"method":"wtt_module.wtt_module.report.salary_approval.salary_approval.function",
				args:{
					"name":frappe.query_report.data[v[i]].salary_slip
				},
				callback(r){
					msgprint("Approved")
				}
			})
			
			}
			// var selected_rows = [];
			// $('.dt-scrollable').find(":input[type=checkbox]").each((idx, row) => {
			// 	if(row.checked){
			// 		frappe.call({
			// 			"method":"wtt_module.wtt_module.report.salary_detail_report.salary_detail_report.function",
			// 			args:{
			// 				"name":frappe.query_report.data[idx].employee
			// 			}
			// 		})
			// 	}
			// });
		});
		frappe.query_report.page.add_inner_button(__("Reject"), function() {

			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			for(i in v)
			{
			frappe.call({
				"method":"wtt_module.wtt_module.report.salary_approval.salary_approval.func",
				args:{
					"name":frappe.query_report.data[v[i]].salary_slip
				},
				callback(r){
					msgprint("Rejected")
				}
			})
			}
		});
		if(frappe.session.user=='Administrator'){
		frappe.query_report.page.add_inner_button(__("Statement"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			var nn = frappe.query_report.data[v[0]].salary_slip
			frappe.call({
				"method":"wtt_module.wtt_module.report.salary_approval.salary_approval.create_statement",
				args:{
					"name":nn
				}
			})
			
			
		},("Create"));
		frappe.query_report.page.add_inner_button(__("Mail"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			for(i in v)
			{
				// alert(frappe.query_report.data[v[0]].salary_slip)
			frappe.call({
				"method":"wtt_module.wtt_module.report.salary_approval.salary_approval.email",
				args:{
					"nn":frappe.query_report.data[v[i]].salary_slip
				}
			})
			}
		},("Create"));

		frappe.query_report.page.add_inner_button(__("Draft"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			for(i in v)
			{
			frappe.call({
				"method":"wtt_module.wtt_module.report.salary_approval.salary_approval.draft",
				args:{
					"nn":frappe.query_report.data[v[i]].salary_slip
				}
			})
			}
		},("Create"));
		}

		if(frappe.session.user=='praveen@wtt1301.com' || frappe.session.user=='Administrator'){
		frappe.query_report.page.add_inner_button(__("Get Ot and Additionals"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			for(i in v)
			{
			frappe.call({
				"method":"wtt_module.wtt_module.report.salary_approval.salary_approval.additionals",
				args:{
					"name":frappe.query_report.data[v[i]].salary_slip
				}
			})
			}
			
		});
		}
	},
	get_datatable_options(options) {
        return Object.assign(options, {
            checkboxColumn: true
        });
    }
};

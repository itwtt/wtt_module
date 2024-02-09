// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Farm Attendance"] = {
	"filters": [
	{
		"fieldname":"from_date",
		"label": __("From Date"),
		"fieldtype": "Date",
		"width": "80",
		"reqd": 1,
		"default":new Date(new Date().getFullYear(), new Date().getMonth()-1, 1)
	},
	{
		"fieldname":"to_date",
		"label": __("To Date"),
		"fieldtype": "Date",
		"width": "80",
		"reqd": 1,
		"default":new Date(new Date().getFullYear(), new Date().getMonth(), 0)
	}
	],
	onload:function(){
		if(frappe.session.user=='Administrator'){
		frappe.query_report.page.add_inner_button(__("Approve"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			for(i in v)
			{
			
			frappe.call({
				"method":"wtt_module.wtt_module.report.farm_attendance.farm_attendance.function",
				args:{
					"emp":frappe.query_report.data[v[i]].employee,
					"emp_name":frappe.query_report.data[v[i]].employee_name,
					"posting_date":frappe.query_report.data[v[i]].posting_date
				}
			})
			
			
			}
			
		});
		frappe.query_report.page.add_inner_button(__("Additionals"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			for(i in v)
			{
			
			frappe.call({
				"method":"wtt_module.wtt_module.report.farm_attendance.farm_attendance.additionals",
				args:{
					"emp":frappe.query_report.data[v[i]].employee,
					"posting_date":frappe.query_report.data[v[i]].posting_date
				},
				callback: function(r) {
				var d = new frappe.ui.Dialog({
				'fields': [
				{'fieldtype': 'Link','label': 'Employee Code', 'fieldname': 'employee','options':'Farm Employee','default':frappe.query_report.data[parseInt(v[i])].employee},
				{"fieldtype": "Data", "label":"Employee Name", "fieldname": "employee_name","default":r.message[0].employee_name},
				{"fieldtype": "Data", "label":"Payment Days", "fieldname": "payment_days","default":r.message[0].payment_days},
				{"fieldtype": "Data", "label":"Salary", "fieldname": "total","default":r.message[0].total},				
				],
				primary_action: function(values){
					frappe.call({
					"method":"wtt_module.wtt_module.report.farm_attendance.farm_attendance.update_salary",
					args:{
						"employee":values.employee,
						"employee_name":values.employee_name,
						"payment_days":values.payment_days,
						"salary":values.total
					},
					callback: function(r) {
						
					}
					});
			
				}
				});
				
				d.show();
				d.fields_dict.payment_days.refresh(); 
				d.fields_dict.payment_days.$input.on("change", function(event){
    			var sqi = this.value;
				var employee = frappe.query_report.data[parseInt(v[i])].employee
				var posting_date = frappe.query_report.data[parseInt(v[i])].posting_date
				frappe.call({
				"method":"wtt_module.wtt_module.report.farm_attendance.farm_attendance.fun_make",
				args:{
					"sqi":sqi,
					"employee":employee,
					"posting_date":posting_date
				},
				callback: function(r) {
					
				}
				});
				});
				}
			})
			
			
			}
			
		});
		}
		frappe.query_report.page.add_inner_button(__("Create Salary Slip"), function() {


			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			for(i in v)
			{
			frappe.call({
				"method":"wtt_module.wtt_module.report.farm_attendance.farm_attendance.create_salary_slip",
				args:{
					"emp":frappe.query_report.data[v[i]].employee,
					"emp_name":frappe.query_report.data[v[i]].employee_name,
					"present":frappe.query_report.data[v[i]].present,
					"absent":frappe.query_report.data[v[i]].absent,
					"half_day":frappe.query_report.data[v[i]].half_day,
					"payment_days":frappe.query_report.data[v[i]].payment_days,
					"salary":frappe.query_report.data[v[i]].salary,
					"posting_date":frappe.query_report.data[v[i]].posting_date,
					"approval_leave":frappe.query_report.data[v[i]].approval_leave,
					"rounded":frappe.query_report.data[v[i]].rounded
				},
				callback(r){
					msgprint("Done")
				}
			})
			}	
			
		});
		
	},
	get_datatable_options(options) {
        return Object.assign(options, {
            checkboxColumn: true
        });
    }
};

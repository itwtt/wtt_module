// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Grievance', {
	setup: function(frm) {
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status","=", "Active"]
				]
			}
		});
		frm.set_query("investigated_by", function() {
			return {
				filters: [
					["Employee","status","=", "Active"],
					["Employee","department","in", ["Human Resources - WTT","MD - WTT"]]
				]
			}
		});
		frm.set_query("resolved_by", function() {
			return {
				filters: [
					["Employee","status","=", "Active"]
					// ["Employee","designation","in", ["HR MANAGER","GENERAL MANAGER - Admin - WTT","HR TRAINEE","HR EXECUTIVE"]]
				]
			}
		});
		if(frm.doc.to=="Company"){
			if(frm.doc.employee_name!=frappe.session.user_fullname){
				if(frappe.user_roles.includes ("HR Manager") || frappe.user_roles.includes ("HR User")){
					frm.set_df_property("description","hidden",1);
				}
			}
		}
	},
	refresh: function(frm) {
		if(frm.doc.to=="Company"){
			if(frm.doc.employee_name!=frappe.session.user_fullname){
				if(frappe.user_roles.includes ("HR Manager") || frappe.user_roles.includes ("HR User")){
					frm.set_df_property("description","hidden",1);
				}
			}
		}
	},
	to: function(frm) {
		if(frm.doc.to=="Company"){
			if(frm.doc.employee_name!=frappe.session.user_fullname){
				if(frappe.user_roles.includes ("HR Manager") || frappe.user_roles.includes ("HR User")){
					frm.set_df_property("description","hidden",1);
				}
			}
		}
	}
});

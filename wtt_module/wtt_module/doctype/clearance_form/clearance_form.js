// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Clearance Form', {
	setup:function(frm){
		frm.set_query("employee_id", function() {
			return {
				filters: [
					["Employee","Status","=", "Active"],

				]
			}

		});	
		frm.set_query("cleared_by1", function() {
			return {
				filters: [
					["Employee","Status","=", "Active"],
					["Employee","Department","=",frm.doc.department],
					["Employee","user_id","=", frappe.session.user]
				]
			}

		});
		frm.set_query("cleared_by2", function() {
			return {
				filters: [
					["Employee","Status","=", "Active"],
					["Employee","Department","=","Admin - WTT"]
				]
			}

		});
		frm.set_query("cleared_by3", function() {
			return {
				filters: [
					["Employee","Status","=", "Active"],
					["Employee","Department","=","It - WTT"]
				]
			}

		});
		frm.set_query("cleared_by4", function() {
			return {
				filters: [
					["Employee","Status","=", "Active"],
					["Employee","Department","=","Accounts - WTT"]
				]
			}

		});
		frm.set_query("cleared_by5", function() {
			return {
				filters: [
					["Employee","Status","=", "Active"]
					// ["Employee","Department","=","Human Resources - WTT"],
				]
			}

		});
		frm.set_query("cleared_by6", function() {
			return {
				filters: [
					["Employee","Status","=", "Active"],
					["Employee","Department","=","STORE - WTT"]
					
				]
			}

		});
	},
	refresh:function(frm){
		if(frappe.user_roles.includes ("Agriculture Manager") || frappe.session.user==frm.doc.user_id || frappe.user_roles.includes ("HR Manager")){
			frm.set_df_property("admin1","read_only",0);
			frm.set_df_property("admin2","read_only",0);
			frm.set_df_property("admin3","read_only",0);
			frm.set_df_property("admin4","read_only",0);
			frm.set_df_property("admin5","read_only",0);
			frm.set_df_property("admin6","read_only",0);
			frm.set_df_property("admin7","read_only",0);
			frm.set_df_property("admin8","read_only",0);
			frm.set_df_property("cleared_by2","read_only",0);
			frm.set_df_property("remarks2","read_only",0);
		}
		if(frappe.user_roles.includes ("Support Team") || frappe.session.user==frm.doc.user_id || frappe.user_roles.includes ("HR Manager")){
			frm.set_df_property("it1","read_only",0);
			frm.set_df_property("it2","read_only",0);
			frm.set_df_property("it3","read_only",0);
			frm.set_df_property("it4","read_only",0);
			frm.set_df_property("it5","read_only",0);
			frm.set_df_property("it6","read_only",0);
			frm.set_df_property("cleared_by3","read_only",0);
			frm.set_df_property("remarks3","read_only",0);
		}
		if(frappe.user_roles.includes ("Accounts Manager") || frappe.session.user==frm.doc.user_id || frappe.user_roles.includes ("HR Manager")){
			frm.set_df_property("accounts1","read_only",0);
			frm.set_df_property("accounts2","read_only",0);
			frm.set_df_property("accounts3","read_only",0);
			frm.set_df_property("accounts4","read_only",0);
			frm.set_df_property("accounts5","read_only",0);
			frm.set_df_property("accounts6","read_only",0);
			frm.set_df_property("accounts7","read_only",0);
			frm.set_df_property("accounts8","read_only",0);
			frm.set_df_property("cleared_by4","read_only",0);
			frm.set_df_property("remarks4","read_only",0);
		}
		if(frappe.user_roles.includes ("HR Manager") || frappe.session.user==frm.doc.user_id || frappe.user_roles.includes ("HR Manager")){
			frm.set_df_property("hr1","read_only",0);
			frm.set_df_property("hr2","read_only",0);
			frm.set_df_property("hr3","read_only",0);
			frm.set_df_property("hr4","read_only",0);
			frm.set_df_property("hr5","read_only",0);
			frm.set_df_property("hr6","read_only",0);
			frm.set_df_property("hr7","read_only",0);
			frm.set_df_property("hr8","read_only",0);
			frm.set_df_property("cleared_by5","read_only",0);
			frm.set_df_property("remarks5","read_only",0);
		}
		if(frappe.user_roles.includes ("Stock Manager") || frappe.session.user==frm.doc.user_id || frappe.user_roles.includes ("HR Manager")){
			frm.set_df_property("store1","read_only",0);
			frm.set_df_property("cleared_by6","read_only",0);
			frm.set_df_property("remarks6","read_only",0);
		}
		if(frappe.user_roles.includes ("HOD") || frappe.user_roles.includes ("HR Manager")){
			frm.set_df_property("hod1","read_only",0);
			frm.set_df_property("hod2","read_only",0);
			frm.set_df_property("hod3","read_only",0);
			frm.set_df_property("hod4","read_only",0);
			frm.set_df_property("hod5","read_only",0);
			frm.set_df_property("hod6","read_only",0);
			frm.set_df_property("cleared_by1","read_only",0);
			frm.set_df_property("remarks1","read_only",0);
		}
	}
});

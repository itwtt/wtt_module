// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('NOC', {
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
					["Employee","Department","=",frm.doc.department]
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
					["Employee","Status","=", "Active"],
					["Employee","Department","=","Human Resources - WTT"]
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
	}

	// refresh: function(frm) {

	// }
});

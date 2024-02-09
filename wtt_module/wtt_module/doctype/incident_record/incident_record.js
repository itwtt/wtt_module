// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Incident Record', {
	setup: function(frm) {
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status","=", "Active"]
				]
			}
		});
		frm.set_query("against_employee", function() {
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
		
	}
});

// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Queries', {
	onload: function(frm) {
		frm.set_query("project", function() {
			return {
				filters: [
					["Project","status", "!=", "Open"],
					["Project","status", "!=", "Cancelled"],
					["Project","status", "!=", "Completed"],
					["Project","status", "!=", "Closed"],
					["Project","status", "!=", "On Hold"]
					
				]
			};
		});
	},
	validate: function(frm) {
		
	}
});

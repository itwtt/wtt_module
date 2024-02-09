// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Cast', {
	setup: function(frm) {
		frm.set_query("project", function() {
			return {
				filters: [
					["Project","status","=", 'On going']
				]
			}

		});
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status","=", 'Active']
				]
			}

		});
	}
});

// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Suggestion', {
	setup: function(frm) {
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status","=", "Active"]
				]
			}
		});
	}
	// refresh: function(frm) {

	// }
});

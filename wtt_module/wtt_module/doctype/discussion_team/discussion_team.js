// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Discussion Team', {
	setup: function(frm,cdt,cdn) {
		frm.set_query("lead", function() {
			return {
				filters: [
					["Lead","status","=", "Converted"]
				]
			}

		});
		
	},
	// refresh: function(frm) {

	// }
});

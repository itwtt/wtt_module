// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Discussion Points', {
	// refresh: function(frm) {

	// }
	setup: function(frm,cdt,cdn) {
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status","=", 'Active']
				]
			}

		});
		frm.set_query("department", "discussion_points", function(frm) {
			return {
				filters: {'company': 'W.t.t technology Services India Pvt Ltd'}
			};
		});
		
	},
});

// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Team', {
	// refresh: function(frm) {

	// }
	setup:function(frm,cdt,cdn){
		frm.set_query("employee", "members", function() {
	    return {
			filters: [
				["Employee","status", "=", "Active"],
				["Employee","branch", "=", "WORKSHOP"]
			]
		};
	});
	}
});

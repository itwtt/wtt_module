// Copyright (c) 2024, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Invoice Request', {
	refresh: function(frm) {
		frm.set_query("wtt_coordinator", function() {
			return {
				filters: [
					["Employee","status","=", "Active"]
				]
			}
		});

		frm.set_query("project", function() {
			return {
				filters: [
					["Project","status","=", "On going"]
				]
			}
		});
	}
});

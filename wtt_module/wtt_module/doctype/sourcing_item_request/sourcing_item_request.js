// Copyright (c) 2024, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sourcing Item Request', {
	refresh: function(frm) {
		frm.set_query("raised_by", function() {
			return {
				filters: [
					["Employee","status","=", 'Active']
				]
			}

		});
	}
});

// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Details', {
	refresh: function(frm) {
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Onduty Request'), () => frm.events.get_onduty(frm),
				__("Get From Onduty"));
		}
	}
});

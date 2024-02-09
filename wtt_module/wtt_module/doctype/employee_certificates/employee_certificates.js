// Copyright (c) 2021, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Certificates', {
	refresh: function(frm) {
		frm.set_df_property("certificates","allow_on_submit",1)
	}
		
});
frappe.ui.form.on('Certificates', {
	refresh: function(frm,cdt,cdn) {
		var d = locals[cdt][cdn];
		d.set_df_property('attachment', 'allow_on_submit', 1)
	}
});

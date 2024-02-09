// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Feedback Form', {
	// refresh: function(frm) {

	// }
	validate:function(frm){
		alert(frm.doc.f1)
	}
});

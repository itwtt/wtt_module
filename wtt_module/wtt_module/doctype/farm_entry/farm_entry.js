// Copyright (c) 2021, wtt_custom and contributors
// For license information, please see license.txt

frappe.ui.form.on('Farm Entry', {
	name1: function(frm,cdt,cdn){
		fil(frm, cdt, cdn);
	}
});

var fil = function(frm, cdt, cdn) {
	frappe.show_alert({
    message:__("Hi, you have a new message "+frm.doc.name1+""),
    indicator:'green'
	}, 10);
}

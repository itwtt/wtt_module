// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Analysis', {
	end_date: function(frm) {
		var daydiff=new Date(frm.doc.end_date)-new Date(frm.doc.start_date);
		frm.set_value("days",daydiff / (1000 * 60 * 60 * 24));
		frm.set_value("hours",(daydiff / (1000 * 60 * 60 * 24))*8);
		frm.refresh_field("days");
		frm.refresh_field("hours");
	},
	start_date: function(frm) {
		if(frm.doc.end_date!=undefined){
			var daydiff=new Date(frm.doc.end_date)-new Date(frm.doc.start_date);
			frm.set_value("days",daydiff / (1000 * 60 * 60 * 24));
			frm.set_value("hours",(daydiff / (1000 * 60 * 60 * 24))*8);
			frm.refresh_field("days");
			frm.refresh_field("hours");			
		}
	}
});

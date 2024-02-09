// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('National Holiday List', {
	// refresh: function(frm) {

	// }
	validate:function(frm){
		var total_holi=0;
		$.each(frm.doc.holidays || [], function(i,d){
			total_holi=total_holi+1
		});
		frm.set_value('total_holidays',total_holi)
	}
});

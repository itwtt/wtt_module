// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('PO Reference Document', {
	// refresh: function(frm) {

	// }
	setup:function(frm){
		frm.set_query("purchase_order", function() {
			return {
				filters: {
					"docstatus": ["=", 1],
					"currency":["!=","INR"]
				}
			}
		});
	}
});

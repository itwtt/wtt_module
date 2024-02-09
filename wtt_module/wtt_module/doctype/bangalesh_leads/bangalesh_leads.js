// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bangalesh leads', {
	// refresh: function(frm) {

	// }
	send_message:function(frm){
		frappe.call({
				method:"wtt_module.wtt_module.doctype.itma_data.itma_data.send_bakrid_wish",
				args:{
					status:"success"
				},
				callback(r){
					
				}
			});
	}
});

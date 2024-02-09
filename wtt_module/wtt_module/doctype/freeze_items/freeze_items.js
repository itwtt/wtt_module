// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Freeze Items', {
	setup:function(frm,cdt,cdn){
		frm.set_query("mr", function() {
			return {
				filters: [
					["Material Request","docstatus","=", 1]
				]
			}

		});
	},
	get_items:function(frm,cdt,cdn){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.freeze_items.freeze_items.freeze",
			args:{
				"mr":frm.doc.mr,
				"project":frm.doc.project
			},
			callback(r){
				var ar=[]
				for(var i=0;i<r.message.length;i++){
					ar.push(r.message[i])
				}
				frm.set_value("items",ar);
			}
		})
	}
	// refresh: function(frm) {

	// }
});

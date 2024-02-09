// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('PMS Modification', {
	// refresh: function(frm) {

	// }
	employee:function(frm){
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.pms_modification.pms_modification.update_technical',
			args: { 
				emp:frm.doc.employee
			},
			callback(r) {
				frm.clear_table("criteria")
				for(var i=0;i<r.message.length;i++)
				{
					var child = frm.add_child("criteria");
					frappe.model.set_value(child.doctype, child.name, "type", r.message[i].perfor);
					frappe.model.set_value(child.doctype, child.name, "criteria", r.message[i].techcri);
					frm.refresh_field("criteria");
				}
			}
		});
	}
});

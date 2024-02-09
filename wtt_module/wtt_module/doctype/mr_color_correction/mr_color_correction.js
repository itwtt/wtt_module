// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('MR Color Correction', {
	click:function(frm){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.mr_color_correction.mr_color_correction.mr_color",
			args:{
				mr:"test"
			},
			callback:function(r){
				// alert("done")
				console.log(r.message)
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("table");
				if(r.message[i].mr!=undefined){
					frappe.model.set_value(child.doctype, child.name, "mr", r.message[i].mr);
					frappe.model.set_value(child.doctype, child.name, "item_code", r.message[i].item_code);
					frappe.model.set_value(child.doctype, child.name, "description", r.message[i].description);
					frappe.model.set_value(child.doctype, child.name, "mr_qty", r.message[i].mr_qty);
					frappe.model.set_value(child.doctype, child.name, "completed_qty", r.message[i].completed_qty);
					frappe.model.set_value(child.doctype, child.name, "po_qty", r.message[i].po_qty);
					frappe.model.set_value(child.doctype, child.name, "mr_name", r.message[i].mr_name);
				}
				else if(r.message[i].po!=undefined){
					frappe.model.set_value(child.doctype, child.name, "po", r.message[i].po);
					frappe.model.set_value(child.doctype, child.name, "item_code", r.message[i].item_code);
					frappe.model.set_value(child.doctype, child.name, "description", r.message[i].description);
					frappe.model.set_value(child.doctype, child.name, "mr_qty", r.message[i].mr_qty);
					frappe.model.set_value(child.doctype, child.name, "completed_qty", r.message[i].completed_qty);
					frappe.model.set_value(child.doctype, child.name, "po_qty", r.message[i].po_qty);
					frappe.model.set_value(child.doctype, child.name, "po_name", r.message[i].po_name);
				}
				


				frm.refresh_field("table");
				}

			}
		})
	},
	update_completed_qty:function(frm,cdt,cdn){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.mr_color_correction.mr_color_correction.update_completed_qty_mr",
			args:{
				ar:frm.doc.table
			}
		})
	}
});

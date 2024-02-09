// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Downgrade MR', {
		onload:function(frm){
		frm.set_query("mr", function() {
			return {
				filters: [
					["Material Request","docstatus", "=", 1]
				]
			};
		});
	},
	get_items:function(frm){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.downgrade_mr.downgrade_mr.get_mr",
			args:{
				"mr":frm.doc.mr
			},
			callback(r){
				var ar=[]
				for(var i=0;i<r.message.length;i++){
					ar.push(r.message[i])
				}
				frm.set_value("items",ar);
			}
		})
	},
	refresh:function(frm)
	{
		frm.fields_dict['items'].grid.add_custom_button('Move for Delete', () => {
			var arr=[]
			var arr2=[]
			$.each(frm.doc.deleted_items, function (index, source_row) {
				arr2.push(source_row.mr_ref)
			});
			$.each(frm.doc.items, function (index, source_row) {
			    if(source_row.__checked==true)
			    {   
			    	if(source_row.mr_ref)
			    	{
			    		if(arr2.includes(source_row.mr_ref)){
			    		console.log("yes")
				    	}
				    	else{
				    		var child = frm.add_child("deleted_items");
							frappe.model.set_value(child.doctype, child.name, "item_code", source_row.item_code);
							frappe.model.set_value(child.doctype, child.name, "description", source_row.description);
							frappe.model.set_value(child.doctype, child.name, "technical_description", source_row.technical_description);
							frappe.model.set_value(child.doctype, child.name, "qty", source_row.qty);
							frappe.model.set_value(child.doctype, child.name, "uom", source_row.uom);
							frappe.model.set_value(child.doctype, child.name, "project", source_row.project);
							frappe.model.set_value(child.doctype, child.name, "mr_ref", source_row.mr_ref);
							frm.refresh_field("deleted_items");
				    	}
			    	}
			    }
			});
		}).addClass('btn-danger');	
	}
});

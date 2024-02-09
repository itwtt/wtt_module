// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Freight Advance', {
	validate:function(frm){	
		var total_amount=0;
		$.each(frm.doc.freight_table, function (i,d) {
			total_amount+=d.final_amount
		});
		frm.set_value("total_amount",total_amount);
		frm.refresh_field("total_amount");

		frm.clear_table("consolidate_table")
		frm.refresh_field("consolidate_table");
		var array=[]
		$.each(frm.doc.freight_table, function (index, source_row) {
	        	array.push({
	        		"amount":source_row.amount,
	        		"transport":source_row.transport,
	        		"account_head":source_row.account_head,
	        		"final_amount":source_row.final_amount
	        	})
			});
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.freight_advance.freight_advance.update_items',
			args: { 
				gok:array
			},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("consolidate_table");
				frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].transport);
				frappe.model.set_value(child.doctype, child.name, "total", r.message[i].amount);
				frappe.model.set_value(child.doctype, child.name, "account_head", r.message[i].account_head);
				frappe.model.set_value(child.doctype, child.name, "advance_amount", r.message[i].final_amount);
				frm.refresh_field("consolidate_table");
				}
			}
			});
	},
	onload:function(frm){
		frm.set_query("order_no", function() {
			return {
				filters: [
					["Purchase Order","workflow_state", "!=", "Cancelled"],
					["Purchase Order","workflow_state", "!=", "Rejected"]	
				]
			};
		});
	},
	refresh:function(frm){
	// 	frm.fields_dict['freight_table'].grid.add_custom_button('Add items', () => {	
	// 	var array=[]
	// 	$.each(frm.doc.freight_table, function (index, source_row) {
	//         if(source_row.__checked==true)
	//         {
	//         	array.push({
	//         		"amount":source_row.amount,
	//         		"transport":source_row.transport,
	//         		"account_head":source_row.account_head,
	//         		"final_amount":source_row.final_amount
	//         	})
	//         }
	// });
	// frappe.call({
	// 		method: 'wtt_module.wtt_module.doctype.freight_advance.freight_advance.update_items',
	// 		args: { 
	// 			gok:array
	// 		},
	// 		callback(r) {
	// 			for(var i=0;i<r.message.length;i++)
	// 			{
	// 			var child = frm.add_child("consolidate_table");
	// 			frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].transport);
	// 			frappe.model.set_value(child.doctype, child.name, "total", r.message[i].amount);
	// 			frappe.model.set_value(child.doctype, child.name, "account_head", r.message[i].account_head);
	// 			frappe.model.set_value(child.doctype, child.name, "advance_amount", r.message[i].final_amount);
	// 			frm.refresh_field("consolidate_table");
	// 			}
	// 		}
	// 		});
	// });
	},
	get_po:function(frm){
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.freight_advance.freight_advance.update_status',
			args: { go:frm.doc.order_no},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("freight_table");
				frappe.model.set_value(child.doctype, child.name, "order_no", r.message[i].name);
				frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
				frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
				frm.refresh_field("freight_table");
				}
			}
		});
	}
	// refresh: function(frm) {

	// }
});

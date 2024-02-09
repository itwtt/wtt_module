// Copyright (c) 2021, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Consolidate', {
	status:function(frm) {
		frm.clear_table("overdue_table")
		frm.refresh_field("overdue_table");
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.payment_consolidate.payment_consolidate.update_status',
			args: { go:frm.doc.status},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("overdue_table");
				frappe.model.set_value(child.doctype, child.name, "invoice_no", r.message[i].name);
				frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
				frappe.model.set_value(child.doctype, child.name, "status", r.message[i].status);
				frappe.model.set_value(child.doctype, child.name, "age", r.message[i].age);
				frappe.model.set_value(child.doctype, child.name, "credit_amount", r.message[i].credit_amount);
				frappe.model.set_value(child.doctype, child.name, "outstanding_amount", r.message[i].outstanding_amount);
				frm.refresh_field("overdue_table");
				}
			}
		});
	},
	validate:function(frm){
		var total_amount=0;
		$.each(frm.doc.final_table, function (i,d) {
			total_amount+=d.outstanding_amount
		});
		frm.set_value("total_amount",total_amount);
		frm.refresh_field("total_amount");

	frm.clear_table("consolidate_table")
	frm.refresh_field("consolidate_table");
	var array=[]
	$.each(frm.doc.final_table, function (index, source_row) {	
    	array.push({
    		"supplier":source_row.supplier,
    		"credit_amount":source_row.credit_amount,
    		"outstanding_amount":source_row.outstanding_amount
    	})
	});
	frappe.call({
			method: 'wtt_module.wtt_module.doctype.payment_consolidate.payment_consolidate.update_items',
			args: { gok:array},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("consolidate_table");
				frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
				frappe.model.set_value(child.doctype, child.name, "credit_amount", r.message[i].credit_amount);
				frappe.model.set_value(child.doctype, child.name, "total", r.message[i].total);
				frm.refresh_field("consolidate_table");
				}
			}
			});
	},
	refresh:function(frm){
	frm.fields_dict['overdue_table'].grid.add_custom_button('Add items', () => {
	var ar=[]
	$.each(frm.doc.overdue_table, function (index, source_row) {
	        if(source_row.__checked==true)
	        {
	        var childTable = cur_frm.add_child("final_table");
			childTable.invoice_no=source_row.invoice_no
			childTable.supplier=source_row.supplier
			childTable.age=source_row.age
			childTable.credit_amount=source_row.credit_amount
			childTable.outstanding_amount=source_row.outstanding_amount
			frm.refresh_fields("final_table");

	        	// ar.push({
	        	// 	"invoice_no":source_row.invoice_no,
	        	// 	"supplier":source_row.supplier,
	        	// 	"age":source_row.age,
	        	// 	"credit_amount":source_row.credit_amount,
	        	// 	"outstanding_amount":source_row.outstanding_amount
	        	// })
	        }
	});
	//frm.set_value('final_table',ar)
	});
	}
});

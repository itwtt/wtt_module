// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Advance Payment', {
	refresh:function(frm){
	frm.get_field("advance_consolidate_table").grid.setup_download;
	frm.fields_dict['search_table'].grid.add_custom_button('Add items', () => {	
	var arr=[]
	$.each(frm.doc.search_table, function (index, source_row) {
		    if(source_row.__checked==true)
		    {
		    	arr.push({
		    		"order_no":source_row.order_no,
		    		"supplier":source_row.supplier,
		    		"age":source_row.age,
		    		"advance":source_row.advance,
		    		"amount":source_row.amount
		    	})
		    }
	});
	frappe.call({
		method: 'wtt_module.wtt_module.doctype.advance_payment.advance_payment.searched_item',
		args: { 
			gok:arr
		},
		callback(r) {
			for(var i=0;i<r.message.length;i++)
			{
			var child = frm.add_child("advance_table");
			frappe.model.set_value(child.doctype, child.name, "order_no", r.message[i].order_no);
			frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
			frappe.model.set_value(child.doctype, child.name, "age", r.message[i].age);
			frappe.model.set_value(child.doctype, child.name, "advance", r.message[i].advance);
			frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
			frm.refresh_field("advance_table");
			}
		}
	});
	});
	},
	validate:function(frm){
		var total_amount=0;
		$.each(frm.doc.advance_table, function (i,d) {
			total_amount+=d.final_amount
		});
		frm.set_value("total_amount",total_amount);
		frm.refresh_field("total_amount");

	frm.clear_table("advance_consolidate_table")
	frm.refresh_field("advance_consolidate_table");
	var array=[]
	$.each(frm.doc.advance_table, function (index, source_row) {	
    	array.push({
    		"supplier":source_row.supplier,
    		"amount":source_row.amount,
    		"final_amount":source_row.final_amount
    	})
	});
	frappe.call({
		method: 'wtt_module.wtt_module.doctype.advance_payment.advance_payment.consolidate',
		args: { 
			gok:array
		},
		callback(r) {
			for(var i=0;i<r.message.length;i++)
			{	
			var child = frm.add_child("advance_consolidate_table");
			frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
			frappe.model.set_value(child.doctype, child.name, "total", r.message[i].amount);
			frappe.model.set_value(child.doctype, child.name, "advance_amount", r.message[i].final_amount);
			frm.refresh_field("advance_consolidate_table");
			}
		}
		});
	},
	get_items: function(frm) {
		frm.clear_table("advance_table")
		frm.refresh_field("advance_table");
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.advance_payment.advance_payment.update_status',
			args: { go:"success"},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("advance_table");
				frappe.model.set_value(child.doctype, child.name, "order_no", r.message[i].name);
				frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
				frappe.model.set_value(child.doctype, child.name, "age", r.message[i].age);
				frappe.model.set_value(child.doctype, child.name, "advance", r.message[i].advance);
				frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
				frm.refresh_field("advance_table");
				}
			}
		});
	},
	onload:function(frm){
		frm.set_query("po", function() {
			return {
				filters: [
					["Purchase Order","workflow_state", "!=", "Cancelled"],
					["Purchase Order","workflow_state", "!=", "Rejected"]
					
				]
			};
		});
	},
	clear:function(frm){
		frm.clear_table("search_table")
		frm.refresh_field("search_table");
	},
	search: function(frm) {
		if(frm.doc.supplier==undefined && frm.doc.po==undefined){
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.advance_payment.advance_payment.search_all',
			args: { go:"done"},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("search_table");
				frappe.model.set_value(child.doctype, child.name, "order_no", r.message[i].name);
				frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
				frappe.model.set_value(child.doctype, child.name, "age", r.message[i].age);
				frappe.model.set_value(child.doctype, child.name, "advance", r.message[i].advance);
				frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
				frappe.model.set_value(child.doctype, child.name, "paid_advance", r.message[i].total_advance);
				frm.refresh_field("search_table");
				}
			}
		});
		}
		else if(frm.doc.po==undefined){
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.advance_payment.advance_payment.search_po1',
			args: { go:frm.doc.supplier},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("search_table");
				frappe.model.set_value(child.doctype, child.name, "order_no", r.message[i].name);
				frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
				frappe.model.set_value(child.doctype, child.name, "age", r.message[i].age);
				frappe.model.set_value(child.doctype, child.name, "advance", r.message[i].advance);
				frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
				frappe.model.set_value(child.doctype, child.name, "paid_advance", r.message[i].total_advance);
				frm.refresh_field("search_table");
				}
			}
		});
		}
		else if(frm.doc.supplier==undefined){
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.advance_payment.advance_payment.search_po2',
			args: { go:frm.doc.po},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("search_table");
				frappe.model.set_value(child.doctype, child.name, "order_no", r.message[i].name);
				frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
				frappe.model.set_value(child.doctype, child.name, "age", r.message[i].age);
				frappe.model.set_value(child.doctype, child.name, "advance", r.message[i].advance);
				frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
				frappe.model.set_value(child.doctype, child.name, "paid_advance", r.message[i].total_advance);
				frm.refresh_field("search_table");
				}
			}
		});	
		}
		else if(frm.doc.supplier!=undefined && frm.doc.po!=undefined){
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.advance_payment.advance_payment.search_po',
			args: { go:frm.doc.supplier,run:frm.doc.po},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("search_table");
				frappe.model.set_value(child.doctype, child.name, "order_no", r.message[i].name);
				frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
				frappe.model.set_value(child.doctype, child.name, "age", r.message[i].age);
				frappe.model.set_value(child.doctype, child.name, "advance", r.message[i].advance);
				frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
				frappe.model.set_value(child.doctype, child.name, "paid_advance", r.message[i].total_advance);
				frm.refresh_field("search_table");
				}
			}
		});
		}

	},
});
frappe.ui.form.on('Advance Table', {
	percentage:function(frm,cdt,cdn){
		calculate_priority1(frm, cdt, cdn);
	}
});
var calculate_priority1 = function(frm, cdt, cdn) {
	
	var child = locals[cdt][cdn];
	if(child.percentage>100){
	frappe.model.set_value(cdt, cdn, "percentage",100)
	}
	frappe.model.set_value(cdt, cdn, "final_amount",((child.percentage/100)*child.amount));
};









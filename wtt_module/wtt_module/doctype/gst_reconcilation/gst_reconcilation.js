// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('GST reconcilation', {
	get_data:function(frm){
		frappe.call({
			method:"get_journal",
			doc:frm.doc,
			callback(r){
				for(var i=0;i<r.message.length;i++){
					var child=frm.add_child("journal_table");
					frappe.model.set_value(child.doctype, child.name, "journal_number", r.message[i].name);
					frappe.model.set_value(child.doctype, child.name, "payment_type", r.message[i].payment_type);
					frappe.model.set_value(child.doctype, child.name, "invoice_date", r.message[i].posting_date);
					frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].pay_to_recd_from);
					frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].total_debit);
					frappe.model.set_value(child.doctype, child.name, "remarks", r.message[i].remark);
					frm.refresh_field("journal_table");
				}
			}
		});
		frappe.call({
			method:"wtt_module.wtt_module.doctype.gst_reconcilation.gst_reconcilation.all_data",
			args:{
				fr_date:frm.doc.fr_date,
				to_date:frm.doc.to_date
			},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{     
				var child = frm.add_child("gst_table");
				frappe.model.set_value(child.doctype, child.name, "invoice_no", r.message[i].invoice_no);
				frappe.model.set_value(child.doctype, child.name, "supplier_dc", r.message[i].supplier_dc);
				frappe.model.set_value(child.doctype, child.name, "invoice_date", r.message[i].invoice_data);
				frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
				frappe.model.set_value(child.doctype, child.name, "tax_id", r.message[i].tax_id);
				frappe.model.set_value(child.doctype, child.name, "account_name", r.message[i].account_name);
				frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
				frappe.model.set_value(child.doctype, child.name, "grand_total", r.message[i].grand_total);
				frappe.model.set_value(child.doctype, child.name, "taxable_value", r.message[i].taxable_value);
				frm.refresh_field("gst_table");
				}
			}
		})		
	},
	reconcile:function(frm){
		frappe.call({
			method:"get_reconcile",
			doc:frm.doc,
			callback(r){
				
				for(var i=0;i<r.message.length;i++){
					var child=frm.add_child("to_reconcil");
					frappe.model.set_value(child.doctype, child.name, "invoice_no", r.message[i].invoice_no);
					frappe.model.set_value(child.doctype, child.name, "supplier_dc", r.message[i].supplier_dc);
					frappe.model.set_value(child.doctype, child.name, "invoice_date", r.message[i].invoice_date);
					frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
					frappe.model.set_value(child.doctype, child.name, "tax_id", r.message[i].tax_id);
					frappe.model.set_value(child.doctype, child.name, "account_name", r.message[i].account_name);
					frappe.model.set_value(child.doctype, child.name, "amount_in_erp", r.message[i].amount_in_erp);
					frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
					frappe.model.set_value(child.doctype, child.name, "grand_total", r.message[i].invoice_amount);
					frappe.model.set_value(child.doctype, child.name, "taxable_value", r.message[i].taxable_value);
					frm.refresh_field("to_reconcil");
				}
			}
		})
	},
	get_value:function(frm){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.gst_reconcilation.gst_reconcilation.get_excel",
			args:{
				excel_link:frm.doc.excel_attach
			},
			callback(r){
				var a=r.message
				var b = a.replace(/'/g, '"');
				var c=JSON.parse(b)
				for(var i=0;i<c.length;i++)
				{
					var child = frm.add_child("upload");
					frappe.model.set_value(child.doctype, child.name, "supplier_dc", c[i].col2);
					frappe.model.set_value(child.doctype, child.name, "invoice_date", c[i].col4);
					frappe.model.set_value(child.doctype, child.name, "supplier", c[i].col1);
					frappe.model.set_value(child.doctype, child.name, "tax_id", c[i].col0);
					frappe.model.set_value(child.doctype, child.name, "amount", c[i].col10);
					frappe.model.set_value(child.doctype, child.name, "tax_amount", c[i].col5);
					frappe.model.set_value(child.doctype, child.name, "invoice_amount", c[i].col9);
					frappe.model.set_value(child.doctype, child.name, "tax_rate", c[i].col8);
					frappe.model.set_value(child.doctype, child.name, "tax_name", c[i].col22);
					frappe.model.set_value(child.doctype, child.name, "cgst", c[i].col11);
					frappe.model.set_value(child.doctype, child.name, "sgst", c[i].col12);
				}
				frm.refresh_field("upload")
			}
		});
	}
});


frappe.ui.form.on("GST Upload Table", {
	cgst: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		if(child.cgst==0)
		{
			frappe.model.set_value(cdt, cdn, "tax_name","IGST");
		}
		else
		{
			frappe.model.set_value(cdt, cdn, "tax_name","GST");
		}
	}
});
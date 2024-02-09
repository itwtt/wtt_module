// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Received Quotation', {
	refresh:function(frm){
		frm.add_custom_button(__('Enquiry Materials'), () => frm.events.get_items_from_mat(frm),
				__("Get Items From"));
	},
	get_items_from_mat:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.received_quotation.received_quotation.make_quote",
					source_doctype: "Materials for Enquiry",
					target: frm,
					date_field: "date",
					setters: {
						
					},
					get_query_filters: {
						docstatus: 1
					}
				});
	},
	before_save: function(frm, cdt, cdn) {
		var temp = frm.doc.enquiry_materials;
		var sum=[]
		$.each(frm.doc.enquiry_materials, function (i, cd) {
			sum.push(cd.amount)		
		})
		var ss=sum.reduce((a, b) => a + b, 0);
		frm.set_value("net_total",ss);		
		frm.set_value("tax_amount",ss*(frm.doc.tax_percentage/100));
		frm.set_value("grand_total",ss+(ss*(frm.doc.tax_percentage/100)));
		frm.refresh_field("net_total");
		frm.refresh_field("tax_percentage");
		frm.refresh_field("grand_total");
	},
});

frappe.ui.form.on('Enquiry Materials', {
	rate: function(frm,cdt,cdn) {
		var child=locals[cdt][cdn];
		frappe.model.set_value(child.doctype,child.name,"amount",child.rate*child.qty);
	},
	qty:function(frm,cdt,cdn){
		var child=locals[cdt][cdn];
		frappe.model.set_value(child.doctype,child.name,"amount",child.rate*child.qty);
	},
	amount:function(frm,cdt,cdn){
		var child=locals[cdt][cdn];
		frappe.model.set_value(child.doctype,child.name,"rate",child.amount/child.qty);
	}
});
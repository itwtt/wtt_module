// Copyright (c) 2021, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Material Movement', {
	setup: function(frm,cdt,cdn) {
		frm.set_query("purchase_order", function() {
			return {
				filters: [
					["Purchase Order","workflow_state","=", "Approved"],
					// ["Purchase Order","naming_series","=", "PO-.YY.-"]
				]
			}

		});
		frm.set_query("receive_person", function() {
			return {
				filters: [
					["Employee","status","=", "Active"],
				]
			}
		});
		frm.set_query("responsible", function() {
			return {
				filters: [
					["Employee","status","=", "Active"],
				]
			}
		});
		frm.set_query("send_by", function() {
			return {
				filters: [
					["DocType","name","in", ("Delivery Note,Sales Invoice,Subcontracting Order,Purchase Receipt")]
				]
			}

		});
		
	},
	refresh: function(frm) {
		var hidebtn = $('*[data-fieldname="items"]');
		hidebtn .find('.grid-add-row').hide();
	},
	validate:function(frm){
		if(frm.doc.inward_outward=="Inward"){
			frm.set_value("party",frm.doc.supplier)
		}
		else if(frm.doc.inward_outward=="Outward"){
			frm.set_value("party",frm.doc.customer)
		}
	}
});

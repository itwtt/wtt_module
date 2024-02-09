// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('QC for DC', {
	refresh: function(frm) {
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Material Request'), () => frm.events.get_items_from_mat(frm),
				__("Get Items From"));

			frm.add_custom_button(__('Purchase Order'), () => frm.events.get_items_from_po(frm),
				__("Get Items From"));
		}
		
	},
	get_items_from_po:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.qc_for_dc.qc_for_dc.make_dnr",
					source_doctype: "Purchase Order",
					target: frm,
					date_field: "schedule_date",
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 1
					}
				});
	},
	
	get_items_from_mat:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.qc_for_dc.qc_for_dc.make_note",
					source_doctype: "Material Request",
					target: frm,
					date_field: "transaction_date",
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 1
						
					}
				});
		},
});

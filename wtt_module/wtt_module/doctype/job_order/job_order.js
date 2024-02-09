
frappe.ui.form.on('Job Order', {
	refresh: function(frm) {
		frm.toggle_reqd('customer', frm.doc.material_request_type=="Customer Provided");
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Stock Entry'), () => frm.events.get_items_from_issue(frm),
				__("Get Items From"));
		}
		
	},
	get_items_from_issue:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.job_order.job_order.make_request",
					source_doctype: "Stock Entry",
					target: frm,
					date_field: "posting_date",
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 1,
						stock_entry_type: 'Material Receipt'
					}
				});
	}
	// supplier:function(frm){
	// 	frappe.call({
	// 		method:'wtt_module.wtt_module.doctype.job_order.job_order.supplier',
	// 		args:{
	// 			nam:frm.doc.name,
	// 			sup:frm.doc.supplier
	// 		}
	// 	})
	// }

});
frappe.ui.form.on("Job Order Table", {
	qty: function(frm, cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "amount", child.qty * child.basic_rate);
	},
	basic_rate: function(frm, cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "amount", child.qty * child.basic_rate);
	}
});

// erpnext.stock.StockEntry = erpnext.stock.StockController.extend({
// 	to_warehouse: function(doc) {
// 		this.set_warehouse_in_children(doc.items, "t_warehouse1", doc.to_warehouse);
// 	},

// 	set_warehouse_in_children: function(child_table, warehouse_field, warehouse) {
// 		let transaction_controller = new erpnext.TransactionController();
// 		transaction_controller.autofill_warehouse(child_table, warehouse_field, warehouse);
// 	}
// });
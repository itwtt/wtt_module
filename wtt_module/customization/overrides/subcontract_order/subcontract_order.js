
{% include 'erpnext/subcontracting/doctype/subcontracting_order/subcontracting_order.js' %};


frappe.ui.form.on('Subcontracting Order', {
	refresh:function(frm){
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Job Order'), () => frm.events.get_items_from_issue(frm),
				__("Get Items From"));
		}
	},
	get_items_from_issue:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.customization.overides.subcontract_order.subcontract_order.make_request",
					source_doctype: "Job Order",
					target: frm,
					date_field: "posting_date",
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 1,
						job_order_type: 'Job Order Request'
					}
				});
	},

});
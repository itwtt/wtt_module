// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('DC Track', {
	refresh:function(frm)
	{
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Material Request'), () => frm.events.get_items_mm(frm),
				__("Get Items From"));
		}
	},
	get_items_mm:function(frm){
		erpnext.utils.map_current_doc({
			method: "wtt_module.wtt_module.doctype.dc_track.dc_track.get_mr",
			source_doctype: "Material Request",
			target: frm,
			setters: {
				schedule_date: undefined,
				status: undefined
			},
			get_query_filters: {
				material_request_type: "Purchase",
				docstatus: 1,
				status: ["!=", "Stopped"],
			},
			allow_child_item_selection: true,
			child_fieldname: "items",
			child_columns: ["idx", "description", "item_code"]
		})
	}
});

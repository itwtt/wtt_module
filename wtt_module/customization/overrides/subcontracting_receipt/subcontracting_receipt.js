// {% include 'erpnext/subcontracting/doctype/subcontracting_receipt/subcontracting_receipt.js' %}

frappe.ui.form.on('Subcontracting Receipt', {
	refresh:function(frm){
		if(frm.doc.docstatus==0){
			frm.add_custom_button(__('Item Inspection'), function() {
				frappe.model.open_mapped_doc({
					method: "wtt_module.customization.overrides.subcontracting_receipt.subcontracting_receipt.make_quality",
					frm: cur_frm,
				});
			}, __('Create'));
		}
	}
});
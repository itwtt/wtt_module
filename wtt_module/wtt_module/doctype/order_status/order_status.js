// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Order Status', {
	// refresh: function(frm) {

	// }
	onload:function(frm){
		frm.set_query("po_no", function() {
			return {
				filters: [
					["Purchase Order","docstatus", "=", 1]
				]
			};
		});
	},
	po_no:function(frm)
	{
		if(frm.doc.po_no)
		{
			frappe.call({
			method:"wtt_module.wtt_module.doctype.order_status.order_status.get_po",
			args:{
				"po_no":frm.doc.po_no
			},
			callback(r){
				var ar=[]
				for(var i=0;i<r.message.length;i++){
					ar.push(r.message[i])
				}
				frm.set_value("order_status_table",ar);
			}
			});
		}
	},
	update_date:function(frm){
		var f_date = frm.doc.shipment_date
		var to_date = frm.doc.expected_reached_date
		$.each(frm.doc.order_status_table || [], function(i, v) {
			v.shipment_date = f_date
			v.expected_reached_date = to_date
		});
		frm.save();
	}
});

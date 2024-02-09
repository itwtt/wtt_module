frappe.ui.form.on('Quotation', {
    advance_paid: function(frm) {
    	frm.set_value("net_total_amount",frm.doc.base_grand_total-frm.doc.advance_paid)
    }
});
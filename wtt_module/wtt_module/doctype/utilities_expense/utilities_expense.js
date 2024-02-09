// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Utilities Expense', {
	validate:function(frm){
		var total_amount=0;
		$.each(frm.doc.utilities_table, function (i,d) {
			total_amount+=d.amount
		});
		frm.set_value("total",total_amount);
	}
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on("Utilities Table", {
	qty: function(frm,cdt, cdn){
		calculate_total(frm, cdt, cdn);
	},
	rate: function(frm, cdt, cdn){
		calculate_total(frm, cdt, cdn);
	}
});
var calculate_total = function(frm, cdt, cdn) {
	var child = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "amount", child.qty * child.rate);
}
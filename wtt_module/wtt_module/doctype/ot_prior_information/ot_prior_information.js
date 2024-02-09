// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('OT Prior Information', {
	validate:function(frm) {
		var idxtotal=0;
		$.each(frm.doc.ot_table, function (i,d) {
			idxtotal=idxtotal+1
		});
		frm.set_value("no_of_persons",idxtotal);

		var total=0;
		$.each(frm.doc.ot_table, function (i,d) {
			total+=d.total_amount
		});
		frm.set_value("grand_total",total);

		var ot_total=0;
		$.each(frm.doc.ot_table, function (i,d) {
			ot_total+=d.working_hours
		});
		frm.set_value("total_working_hours",ot_total);
	},
	onload:function(frm){
		frm.set_query("hod", function() {
			return {
				filters: [
					["Employee","status", "=", "Active"]
				]
			};
		});

		frm.set_query("employee", "ot_table", function() {
		    return {
				filters: [
					["Employee","status", "=", "Active"]
				]
			};
		});
	}
});


frappe.ui.form.on('Overtime table', {
	working_hours: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "onehr", (child.gross/30/8));
		calculate_total(frm, cdt, cdn);
	}
});

var calculate_total = function(frm, cdt, cdn) {
	var child = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "total_amount", child.onehr * child.working_hours);
}
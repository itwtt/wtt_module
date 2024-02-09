// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Duty Payment', {
	validate:function(frm)
	{
		var total_amount=0;
		$.each(frm.doc.duty_table, function (i,d) {
			total_amount+=d.amount
		});
		frm.set_value("total_amount",total_amount);
		frm.refresh_field("total_amount");
	}
});

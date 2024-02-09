// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item Lead Time', {
	setup:function(frm){
		frm.set_query("item_template", function() {
			return {
				filters: [
					["Item","has_variants","=", 1],
				]
			}

		});
	},
	// refresh: function(frm) {

	// }
	get_total_days:function(frm){
		if(frm.doc.lead_time!=undefined && frm.doc.selection!=undefined && frm.doc.ordering!=undefined && frm.doc.delivery_time!=undefined)
		{
			var lead_day=0
			if(frm.doc.selection=="Week")
			{
			lead_day=parseFloat(frm.doc.lead_time)*7	
			}
			else if(frm.doc.selection=="Month")
			{
			lead_day=parseFloat(frm.doc.lead_time)*30
			}
			else if(frm.doc.selection=="Year")
			{
			lead_day=parseFloat(frm.doc.lead_time)*365
			}
			frm.set_value("lead_days",lead_day)
			frm.set_value("total_days",parseFloat(frm.doc.lead_days)+parseFloat(frm.doc.ordering)+parseFloat(frm.doc.delivery_time))
		}
		else
		{
			frappe.throw("Please Enter all the data")
		}
	}
});

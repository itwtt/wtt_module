// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Supplier Lead Time', {
	refresh: function(frm) {
	
	}
});


frappe.ui.form.on("Supplier Lead Table", {
	selection:function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		if(child.total_lead_time!=undefined)
		{
			var lead_day=0;
			if(child.selection=="Week")
			{
			lead_day=parseFloat(child.total_lead_time)*7	
			}
			else if(child.selection=="Month")
			{
			lead_day=parseFloat(child.total_lead_time)*30
			}
			else if(child.selection=="Day")
			{
			lead_day=parseFloat(child.total_lead_time)
			}
			frappe.model.set_value(cdt, cdn, "lead_days", lead_day);
		}
	},
	total_lead_time:function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		if(child.total_lead_time!=undefined)
		{
			var lead_day=0;
			if(child.selection=="Week")
			{
			lead_day=parseFloat(child.total_lead_time)*7	
			}
			else if(child.selection=="Month")
			{
			lead_day=parseFloat(child.total_lead_time)*30
			}
			else if(child.selection=="Day")
			{
			lead_day=parseFloat(child.total_lead_time)
			}
			frappe.model.set_value(cdt, cdn, "lead_days", lead_day);
		}
	}
});
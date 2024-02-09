// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Lab Experiments', {
	refresh: function(frm) {
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status", "=", "Active"]
				]
			};
		});
	},
	resource_type:function(frm){
		if(frm.doc.resource_type == 'Equipment')
		{
			frm.set_value("tentative_date","You get the result within 12 hrs");
			frm.refresh_field("tentative_date");
		}
		else if(frm.doc.resource_type == 'Equipment + Reagents')
		{
			frm.set_value("tentative_date","You get the result within 48 hrs");
			frm.refresh_field("tentative_date");
		}
		else
		{
			frm.set_value("tentative_date","");
			frm.refresh_field("tentative_date");
		}
	}
});

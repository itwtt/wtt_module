// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Joint Task Allocation', {
	setup: function(frm,cdt,cdn) {
		frm.set_query("user", function() {
			return {
				filters: [
					["User","name","=", frappe.session.user]
				]
			}

		});
	},
	
	refresh: function(frm) {
		if(frm.doc.user==undefined && frm.doc.owner){
		if(frappe.session.user=='ps_cmd@wttindia.com')
		{
		frm.set_value("user",'venkat@wttindia.com')	
		}
		else
		{
		frm.set_value("user",frm.doc.owner)
		}
		}
		else if(frm.doc.user==undefined){
		if(frappe.session.user=='ps_cmd@wttindia.com')
		{
		frm.set_value("user",'venkat@wttindia.com')	
		}
		else
		{
		frm.set_value("user",frappe.session.user)
		}
		}
	},
	validate:function(frm,cdt,cdn){
		calculate_total_points(frm,cdt,cdn);
		calculate_gained_points(frm,cdt,cdn);
	},
});
frappe.ui.form.on('Joint Task Allocation', {

});
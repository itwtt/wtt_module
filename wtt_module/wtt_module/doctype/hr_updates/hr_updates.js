// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('HR Updates', {
	setup:function(frm,cddt,cdn){
		frm.set_query("employee", "employees", function() {
	    return {
			filters: [
				["Employee","status", "=", "Active"]
			]
		};
		});
		frm.set_query("employee", "employees2", function() {
	    return {
			filters: [
				["Employee","status", "=", "Active"]
			]
		};
		});
	

	},
	get_employee:function(frm,cdt,cdn){
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.hr_updates.hr_updates.update_employee',
			args: { go:frm.doc.date},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
					for (var j=0;j<r.message[i].length;j++)
					{
						if(r.message[i][j].emp)
						{
							var child = frm.add_child("att_employee");
							frappe.model.set_value(child.doctype, child.name, "employee", r.message[i][j].emp);
							frm.refresh_field("att_employee");
						}
						else
						{
							var child = frm.add_child("late_entries");
							frappe.model.set_value(child.doctype, child.name, "employee", r.message[i][j].lt);
							frappe.model.set_value(child.doctype, child.name, "time", r.message[i][j].tt);
							frm.refresh_field("late_entries");
						}
					}
				}
			}
		});
	}
});

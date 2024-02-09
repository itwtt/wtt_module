// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bonus', {
	// refresh: function(frm) {

	// }
	before_save:function(frm){
		var temp = frm.doc.bonus_table;
		var i,sum=0
		for(i=0;i<temp.length;i++)
		{
		sum+=temp[i].bonus;
		}
		frm.set_value("total_basic",sum);
		frm.refresh_field("total_basic");

		var ho_total=0
		var wo_total=0
		$.each(frm.doc.bonus_table, function (index, v) {
			if(v.branch == 'HEAD OFFICE')
			{
				ho_total+=v.bonus
			}
			else if (v.branch == 'WORKSHOP')
			{
				wo_total+=v.bonus
			}
		});
		frm.set_value("ho",ho_total);
		frm.refresh_field("ho");
		frm.set_value("workshop",wo_total);
		frm.refresh_field("workshop");
	},
	ho_percentage:function(frm)
	{
		$.each(frm.doc.bonus_table, function (index, v) {
			if(v.branch == 'HEAD OFFICE')
			{
				frappe.model.set_value(v.doctype, v.name, "percentage",frm.doc.ho_percentage);
			}
		});
	},
	workshop_percentage:function(frm)
	{
		$.each(frm.doc.bonus_table, function (index, v) {
			if(v.branch == 'WORKSHOP')
			{
				frappe.model.set_value(v.doctype, v.name, "percentage",frm.doc.workshop_percentage);
			}
		});
	},
	get_items:function(frm)
	{
		frm.clear_table("bonus_table")
		frm.refresh_field("bonus_table");
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.bonus.bonus.get_bonus',
			args: { 
				fr_date: frm.doc.from_date,
				to_date: frm.doc.to_date
			 },
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
					var child = frm.add_child("bonus_table");
					frappe.model.set_value(child.doctype, child.name, "employee", r.message[i].employee);
					frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[i].employee_name);
					frappe.model.set_value(child.doctype, child.name, "branch", r.message[i].branch);
					frappe.model.set_value(child.doctype, child.name, "total_amount", r.message[i].total_basic);
					frappe.model.set_value(child.doctype, child.name, "total_days", r.message[i].total_present);
					frappe.model.set_value(child.doctype, child.name, "percentage",8.33);
					frappe.model.set_value(child.doctype, child.name, "bonus", r.message[i].bonus);
					frm.refresh_field("bonus_table");
				}
			}
		})
	}
});


frappe.ui.form.on("Bonus Table", {
	percentage: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "bonus", (child.percentage/100) * child.total_amount);
		calculate_total(frm, cdt, cdn);
	}
});
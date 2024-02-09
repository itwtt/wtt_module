// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Perks', {
	validate:function(frm){
		var total_ot=0;
		var overall=0;
		$.each(frm.doc.salary_table || [], function(i,d){
			total_ot+=flt(d.ot_amount)
		});

		$.each(frm.doc.salary_table || [], function(i,d){
			overall+=flt(d.amount)
		});
		frm.set_value("total_ot_amount",total_ot);
		frm.set_value("total_perks_amount",overall);
	},
	get_employee:function(frm){
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.perks.perks.update_salary',
			args: { 
				fr_date:frm.doc.from_date,
				to_date:frm.doc.to_date
			},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("salary_table");
				frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[i].employee_name);
				frappe.model.set_value(child.doctype, child.name, "rounded_total", r.message[i].rounded_total);
				frappe.model.set_value(child.doctype, child.name, "ot_hrs", r.message[i].ot_hrs);
				frappe.model.set_value(child.doctype, child.name, "salary_1", r.message[i].salary_1);
				frappe.model.set_value(child.doctype, child.name, "ot_amount", r.message[i].ot_amount);
				frappe.model.set_value(child.doctype, child.name, "salary_id", r.message[i].salary_id);
				frm.refresh_field("salary_table");
				}
			}
		});

		// frappe.call({
		// 	method: 'wtt_module.wtt_module.doctype.perks.perks.update_ot',
		// 	args: { 
		// 		fr_date:frm.doc.from_date,
		// 		to_date:frm.doc.to_date
		// 	},
		// 	callback(r) {
		// 		for(var i=0;i<r.message.length;i++)
		// 		{
		// 		var child = frm.add_child("ot_table");
		// 		frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[i].employee_name);
		// 		frappe.model.set_value(child.doctype, child.name, "ot_hrs", r.message[i].ot_hrs);
		// 		frappe.model.set_value(child.doctype, child.name, "salary_1", r.message[i].salary_1);
		// 		frappe.model.set_value(child.doctype, child.name, "ot_amount", r.message[i].ot_amount);
		// 		frm.refresh_field("ot_table");
		// 		}
		// 	}
		// });
	}
});

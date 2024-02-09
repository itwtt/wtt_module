
frappe.ui.form.on('Final Salary Statement', {
	refresh: function(frm) {
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Other Bank'), () => frm.events.get_bank(frm),
				__("Export"));
			frm.add_custom_button(__('Indian Bank'), () => frm.events.get_ib(frm),
				__("Export"));
		}
		
	},
	get_bank:function(frm){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.final_salary_statement.final_salary_statement.create_excel",
			args:{
				doc:frm.doc.salary
			},
			callback: function(r) {	
				for(var i=0;i<r.message.length;i++){
				var file_url=JSON.stringify(r.message[0].url)
				file_url = file_url.replace(/#/g, '%23');
				file_url = file_url.replace(/"/g, '');
				window.open(file_url);
				}
			}
		})
	},
	get_ib:function(frm){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.final_salary_statement.final_salary_statement.create_excel_ib",
			args:{
				doc:frm.doc.salary2
			},
			callback: function(r) {	
				for(var i=0;i<r.message.length;i++){
				var file_url=JSON.stringify(r.message[0].url)
				file_url = file_url.replace(/#/g, '%23');
				file_url = file_url.replace(/"/g, '');
				window.open(file_url);
				}
			}
		})
	},
	validate:function(frm){
		var total_amount=0;
		var total_amount1=0;
		var total_charge=0;
		var total_charge1=0;
		var net=0;
		var net2=0;
		$.each(frm.doc.salary, function (i,d) {
			total_amount+=d.amount
			total_charge+=d.charges
		});

		$.each(frm.doc.salary2, function (i,d) {
			total_amount1+=d.amount
			total_charge1+=d.charges
		});
		frm.set_value("total1",total_amount);
		frm.set_value("total2",total_amount1);
		frm.set_value("charge1",total_charge);
		frm.set_value("charge2",total_charge1);
		frm.set_value("total3",Math.round(total_amount+total_charge));
		frm.set_value("total4",Math.round(total_amount1+total_charge1));
	},
	get_employee:function(frm){
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.final_salary_statement.final_salary_statement.update_salary',
			args: { 
				fr_date:frm.doc.from_date,
				to_date:frm.doc.to_date,
				company:frm.doc.company
			},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
				if(r.message[i].bank_name=='INDIAN BANK'){
				var child = frm.add_child("salary2");
				frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[i].employee_name);
				frappe.model.set_value(child.doctype, child.name, "account_no", r.message[i].account_no);
				frappe.model.set_value(child.doctype, child.name, "ifsc_code", r.message[i].ifsc_code);
				frappe.model.set_value(child.doctype, child.name, "bank_name", r.message[i].bank_name);
				frappe.model.set_value(child.doctype, child.name, "charges", 0);
				frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
				frm.refresh_field("salary2");
				}
				else{
				var child = frm.add_child("salary");
				frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[i].employee_name);
				frappe.model.set_value(child.doctype, child.name, "account_no", r.message[i].account_no);
				frappe.model.set_value(child.doctype, child.name, "ifsc_code", r.message[i].ifsc_code);
				frappe.model.set_value(child.doctype, child.name, "bank_name", r.message[i].bank_name);
				frappe.model.set_value(child.doctype, child.name, "charges", r.message[i].charges);
				frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
				frm.refresh_field("salary");
				}
				}
			}
		});
	},
	get_arrear:function(frm){
		frappe.call({
	        method:"wtt_module.wtt_module.doctype.final_salary_statement.final_salary_statement.get_arrear",
	        args: { 
				fr_date:frm.doc.from_date,
				to_date:frm.doc.to_date,
				company:frm.doc.company
			},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
					if(r.message[i].bank_name=='INDIAN BANK'){
						var child = frm.add_child("salary2");
						frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[i].employee_name);
						frappe.model.set_value(child.doctype, child.name, "account_no", r.message[i].account_no);
						frappe.model.set_value(child.doctype, child.name, "ifsc_code", r.message[i].ifsc_code);
						frappe.model.set_value(child.doctype, child.name, "bank_name", r.message[i].bank_name);
						frappe.model.set_value(child.doctype, child.name, "charges", 0);
						frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
						frm.refresh_field("salary2");
					}
					
					else{
						var child = frm.add_child("salary");
						frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[i].employee_name);
						frappe.model.set_value(child.doctype, child.name, "account_no", r.message[i].account_no);
						frappe.model.set_value(child.doctype, child.name, "ifsc_code", r.message[i].ifsc_code);
						frappe.model.set_value(child.doctype, child.name, "bank_name", r.message[i].bank_name);
						frappe.model.set_value(child.doctype, child.name, "charges", r.message[i].charges);
						frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
						frm.refresh_field("salary");
					}
				}
			}
		});
	}
		
});

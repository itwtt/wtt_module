// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Greetings Message', {
	// refresh: function(frm) {

	// }
	send_message:function(frm){
		message="A warm welcome from the whole team here at WTT INTERNATIONAL PVT LTD, We’re so happy to have you on our team, "+frm.doc.employee_name+".Congratulations and best wishes on your first day\n\n Your Details:\n Name: "+frm.doc.employee_name+"\nDepartment: "+frm.doc.department+"\nDesignation: "+frm.doc.designation+"\nSystem UserId: "+frm.doc.system_user_id+"\nSystem Password: "+frm.doc.system_password+"\nERP Link: "+frm.doc.erp_link+"\nERP Username: "+frm.doc.erp_username+"\nERP Password: "+frm.doc.erp_password+""
	}
});

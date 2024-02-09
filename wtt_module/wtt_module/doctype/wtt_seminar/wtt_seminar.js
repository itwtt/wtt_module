// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('WTT Seminar', {
	// send_mail:function(frm)
	// {
	// 	frappe.call({
	// 			method:"wtt_module.wtt_module.doctype.wtt_seminar.wtt_seminar.send_all_mail",
	// 			args:{
	// 				client_name:frm.doc.client_name,
	// 				email:frm.doc.email
	// 			},
	// 			callback(r){
	// 				frm.set_value("mail_status","sent mail");
	// 				frm.refresh_field("mail_status");
	// 			}
	// 		});
	// },
	// send_whatsapp:function(frm)
	// {
	// 	frappe.call({
	// 			method:"wtt_module.wtt_module.doctype.wtt_seminar.wtt_seminar.send_whatsapp",
	// 			args:{
	// 				client_name:frm.doc.client_name,
					
	// 				:frm.doc.mobile_no
	// 			},
	// 			callback(r){
	// 				frm.set_value("whatsapp_status","sent whatsapp");
	// 				frm.refresh_field("whatsapp_status");
	// 			}
	// 		});
	// }
});

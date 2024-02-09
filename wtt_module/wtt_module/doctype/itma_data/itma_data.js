frappe.ui.form.on('ITMA Data', {
	// refresh: function(frm) {

	// }
	send_whatsapp:function(frm)
	{
			frappe.call({
				method:"wtt_module.wtt_module.doctype.itma_data.itma_data.send_message",
				args:{
					client_name:frm.doc.client_name,
					phone:frm.doc.phone_no
				},
				callback(r){
					frm.set_value("whatsapp_status","sent");
					frm.refresh_field("whatsapp_status");
				}
			});
	},
	send_pic:function(frm)
	{
		// frappe.call({
		// 		method:"wtt_module.wtt_module.doctype.itma_data.itma_data.send_pic",
		// 		args:{
		// 			client_name:frm.doc.client_name,
		// 			phone:frm.doc.phone_no,
		// 			pic:frm.doc.attach
		// 		},
		// 		callback(r){
		// 			frm.set_value("whatsapp_status","sent");
		// 			frm.refresh_field("whatsapp_status");
		// 		}
		// 	});
		frappe.call({
				method:"wtt_module.wtt_module.doctype.itma_data.itma_data.send_bang",
				args:{
					client_name:frm.doc.client_name,
					phone:frm.doc.phone_no,
					pic:frm.doc.attach
				},
				callback(r){
					frm.set_value("whatsapp_status","sent");
					frm.refresh_field("whatsapp_status");
				}
			});
	},
	send_bro:function(frm)
	{
		frappe.call({
				method:"wtt_module.wtt_module.doctype.itma_data.itma_data.send_bro",
				args:{
					client_name:frm.doc.client_name,
					phone:frm.doc.phone_no,
					broucher:frm.doc.broucher
				},
				callback(r){
					frm.set_value("whatsapp_status","sent");
					frm.refresh_field("whatsapp_status");
				}
			});
	},
	send_mail:function(frm)
	{
			frappe.call({
				method:"wtt_module.wtt_module.doctype.itma_data.itma_data.send_mail",
				args:{
					client_name:frm.doc.client_name,
					email:frm.doc.email
				},
				callback(r){
					frm.set_value("mail_status","sent");
					frm.refresh_field("mail_status");
				}
			});
	},
	send_mail_pic:function(frm)
	{
		frappe.call({
				method:"wtt_module.wtt_module.doctype.itma_data.itma_data.send_mail_pic",
				args:{
					client_name:frm.doc.client_name,
					email:frm.doc.email,
					pic:frm.doc.attach
				},
				callback(r){
					frm.set_value("mail_status","sent");
					frm.refresh_field("mail_status");
				}
			});
	},
	broucher_only:function(frm)
	{
		// frappe.call({
		// 		method:"wtt_module.wtt_module.doctype.itma_data.itma_data.broucher_only",
		// 		args:{
		// 			phone:frm.doc.phone_no,
		// 			broucher:frm.doc.broucher
		// 		},
		// 		callback(r){
					
		// 		}
		// 	});
		frappe.call({
				method:"wtt_module.wtt_module.doctype.itma_data.itma_data.bang_broucher_only",
				args:{
					phone:frm.doc.phone_no
				},
				callback(r){
					
				}
			});
	},
	mail_broucher_content:function(frm)
	{
		frappe.call({
				method:"wtt_module.wtt_module.doctype.itma_data.itma_data.mail_broucher_content",
				args:{
					client_name:frm.doc.client_name,
					email:frm.doc.email
				},
				callback(r){
					frm.set_value("mail_status","broucher sent");
					frm.refresh_field("mail_status");
				}
			});
	},
	overall_sent:function(frm)
	{
		frappe.call({
				method:"wtt_module.wtt_module.doctype.itma_data.itma_data.send_all",
				args:{
					status:"success"
				},
				callback(r){
					
				}
			});
	},
	overall_mail:function(frm)
	{
		frappe.call({
				method:"wtt_module.wtt_module.doctype.itma_data.itma_data.send_all_mail",
				args:{
					status:"success"
				},
				callback(r){
					
				}
			});
	},
	bakrid_wish:function(frm)
	{
		frappe.call({
				method:"wtt_module.wtt_module.doctype.itma_data.itma_data.send_bakrid_wish",
				args:{
					status:"success"
				},
				callback(r){
					
				}
			});
	}
});

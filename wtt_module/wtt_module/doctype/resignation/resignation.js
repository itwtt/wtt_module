// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Resignation', {
	refresh: function(frm) {
		
		// frm.add_custom_button("Send",function(){
		// 	frappe.confirm("Are you Sure",
		// 		()=>{
		// 			frm.events.send_mail(frm);
		// 		},
		// 		()=>{
					
		// 		}
		// 	)
		// },("Mail"));
		// frm.add_custom_button("Reply",function(){
		// 	frappe.confirm("Are you Sure",
		// 		()=>{
		// 			frm.events.reply_mail(frm);
		// 		},
		// 		()=>{
					
		// 		}
		// 	)
		// },("Mail"))
	},
	// send_mail: function(frm) {
	// 	if (frm.doc.name) {
	// 		return frappe.call({
	// 			method: 'send_mail',
	// 			doc: frm.doc,
	// 			callback(r){
	// 				frm.set_value("message","");
	// 				frm.refresh_field("message");
	// 				frm.set_value("subject","");
	// 				frm.refresh_field("subject");
	// 				frm.save()
	// 			}
	// 		});
	// 	}
	// },
	// reply_mail: function(frm) {
	// 	if (frm.doc.name) {
	// 		return frappe.call({
	// 			method: 'reply_mail',
	// 			doc: frm.doc,
	// 			callback(r){
	// 				frm.set_value("message","");
	// 				frm.refresh_field("message");
	// 				frm.set_value("subject","");
	// 				frm.refresh_field("subject");
	// 				frm.save()
	// 			}
	// 		});
	// 	}
	// }
});

frappe.ui.form.on('Purchase Invoice', {
expense_head: function(frm) {
	$.each(frm.doc.items || [], function(i, d) {
	d.expense_account= frm.doc.expense_head;
	});
	refresh_field("expense_account");
	},
	refresh: function(frm) {
		if(frm.doc.docstatus===0){
			if(frappe.session.user=='venkat@wttindia.com' || frappe.session.user=='sarnita@wttindia.com' || frappe.session.user=='Administrator'){
				frm.add_custom_button(__('Allow Over Billing'), () => frm.events.function_name(frm));	
			}			
		}
		// if(frappe.session.user=='Administrator'){
		// 	frm.add_custom_button(__('Send Mail'), () => frm.events.mail_pdf(frm));	
		// }	
	},
	function_name:function(frm){
		frappe.confirm('Are you sure you want to proceed?',
	    () => {
	        frappe.call({
			method:"wtt_module.customization.custom.frappe_call.allow_overbilling_invoice",
			args:{
				"user":frm.doc.name
			},
			callback(r){
				location.reload()
			}
			})
	    }, () => {
	       frappe.msgprint({
			    title: __('Error'),
			    indicator: 'red',
			    message: __('Aborted')
			});
	    })
		
	},
	mail_pdf:function(frm){
		frappe.call({
			method:"wtt_module.customization.custom.purchase_invoice.mail_pdf",
			args:{
				"doc":frm.doc.name
			}
			})
	},
	get_not_received_items:function(frm){
		frappe.call({
			method:"get_not_received_items",
			doc:frm.doc,
			callback(r){
				// msgprint(JSON.stringify(r.message))
				for(var i in r.message){
					var child = frm.add_child("items");
					frappe.model.set_value(child.doctype, child.name, "item_name", r.message[i].item_name);
					frappe.model.set_value(child.doctype, child.name, "description", r.message[i].description);
					frappe.model.set_value(child.doctype, child.name, "technical_description", r.message[i].technical_description);
					frappe.model.set_value(child.doctype, child.name, "qty", r.message[i].received_qty);
					frappe.model.set_value(child.doctype, child.name, "uom", r.message[i].uom);
					frappe.model.set_value(child.doctype, child.name, "rate", r.message[i].rate);
					frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
					frappe.model.set_value(child.doctype, child.name, "expense_account", frm.doc.expense_head);
					frappe.model.set_value(child.doctype, child.name, "project", frm.doc.project);
					frappe.model.set_value(child.doctype, child.name, "price_list_rate", frm.doc.price_list_rate);
					frappe.model.set_value(child.doctype, child.name, "discount_percentage", frm.doc.discount_percentage);
					frappe.model.set_value(child.doctype, child.name, "discount_amount", frm.doc.discount_amount);
					frm.refresh_field("items");
					}
			}
		})
	}
});
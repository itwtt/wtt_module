// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Party Name', {
	supplier_save:function(frm)
	{
		if(frm.doc.party_type=='Supplier'){
			var regex = /[A-Z]{5}[0-9]{4}[A-Z]{1}$/;
			var gstinformat = new RegExp('^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9]{1}Z[a-zA-Z0-9]{1}$');

			if(!regex.test(frm.doc.pan)){
				frappe.throw("Invalid PAN")
			}
			else{
			if(gstinformat.test(frm.doc.tax_id)){
				frappe.throw("Invalid Tax ID")
			}
			else{
			frappe.call({
						"method":"wtt_module.wtt_module.doctype.party_name.party_name.update_supplier",
						args:{
							"supplier_name":frm.doc.supplier_name,
							"country":frm.doc.country,
							"tax_id":frm.doc.tax_id,
							"tax_category":frm.doc.tax_category,
							"supplier_group":frm.doc.supplier_group,
							"supplier_type":frm.doc.supplier_type,
							"gst_category":frm.doc.gst_category,
							"pan":frm.doc.pan,
							"iban":frm.doc.iban,
							"bank":frm.doc.bank,
							"ifsc_code":frm.doc.ifsc_code,
							"branch":frm.doc.branch,
							"branch_code":frm.doc.branch_code,
							"bank_account_no":frm.doc.bank_account_no
						},
						callback: function(r) {
							var ar=[{"link_doctype":"Supplier","link_name":r.message,"link_title":r.message}]
							frm.set_value("address_title",r.message);
							frm.set_value("first_name",r.message);
							frm.set_value("address_link",ar);
							frm.set_value("links",ar);
						}
					});
			}
			}
		}
		else{
			var regex = /[A-Z]{5}[0-9]{4}[A-Z]{1}$/;
			var gstinformat = new RegExp('^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9]{1}Z[a-zA-Z0-9]{1}$');
			if(!regex.test(frm.doc.pan)){
				frappe.throw("Invalid PAN")
			}
			else{
			if(!gstinformat.test(frm.doc.tax_id)){
				frappe.throw("Invalid Tax ID")
			}
			else{
			frappe.call({
						"method":"wtt_module.wtt_module.doctype.party_name.party_name.update_customer",
						args:{
							"customer_name":frm.doc.customer_name,
							"territory":frm.doc.territory,
							"type1":frm.doc.type,
							"customer_group":frm.doc.customer_group,
							"tax_id":frm.doc.tax_id,
							"tax_category":frm.doc.tax_category,
							"gst_category":frm.doc.gst_category,
							"pan":frm.doc.pan,
							"iban":frm.doc.iban,
							"bank":frm.doc.bank,
							"ifsc_code":frm.doc.ifsc_code,
							"branch":frm.doc.branch,
							"branch_code":frm.doc.branch_code,
							"bank_account_no":frm.doc.bank_account_no
						},
						callback: function(r) {
							var ar=[{"link_doctype":"Customer","link_name":r.message,"link_title":r.message}]
							frm.set_value("address_title",r.message);
							frm.set_value("first_name",r.message);
							frm.set_value("address_link",ar);
							frm.set_value("links",ar);
						}
					});
			}
			}
		}
	},
	address_save:function(frm)
	{
		var ar=[]
		$.each(frm.doc.address_link, function (index, source_row) {
		ar.push({
			"link_doctype":source_row.link_doctype,
			"link_name":source_row.link_name,
			"link_title":source_row.link_title
		})
		});
		frappe.call({
					"method":"wtt_module.wtt_module.doctype.party_name.party_name.update_address",
					args:{
						"address_title":frm.doc.address_title,
						"address_type":frm.doc.address_type,
						"address_line1":frm.doc.address_line1,
						"address_line2":frm.doc.address_line2,
						"city":frm.doc.city,
						"state":frm.doc.state,
						"address_country":frm.doc.address_country,
						"pincode":frm.doc.pincode,
						"ars":ar
					},
					callback: function(r) {
						console.log('success')
					}
				});
	},
	contact_save:function(frm)
	{
		frappe.call({
					"method":"wtt_module.wtt_module.doctype.party_name.party_name.update_contact",
					args:{
						"first_name":frm.doc.first_name,
						"middle_name":frm.doc.middle_name,
						"last_name":frm.doc.last_name,
						"email_id":frm.doc.email_id,
						"user":frm.doc.user,
						"address":frm.doc.address,
						"status":frm.doc.status,
						"salutation":frm.doc.salutation,
						"designation":frm.doc.designation,
						"gender":frm.doc.gender,
						"phone":frm.doc.phone,
						"mobile_no":frm.doc.mobile_no,
						"company_name":frm.doc.company_name,
						"email_ids":frm.doc.email_ids,
						"contact_nos":frm.doc.contact_nos,
						"links":frm.doc.links
					}
				});
	}
	});
	// frappe.call({
	// 		"method":"frappe.utils.print_format.download_multi_pdf",
	// 		args:{
	// 			"doctype":frm.doc.doctype,
	// 			"name":frm.doc.name
	// 		},
	// 		callback: function(r) {
	// 			console.log('success')
	// 		}
	// 	});
	// var w = window.open(
	// 	frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
	// 		+ "doctype=" + encodeURIComponent(frm.doc.doctype)
	// 		+ "&name=" + encodeURIComponent(frm.doc.name)
	// 		+ (frm.doc.lang_code ? ("&_lang=" + frm.doc.lang_code) : ""))
	// 	);
	// var vv=frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
	// 		+ "doctype=" + encodeURIComponent(frm.doc.doctype)
	// 		+ "&name=" + encodeURIComponent(frm.doc.name)
	// 		+ (frm.doc.lang_code ? ("&_lang=" + frm.doc.lang_code) : ""))
	// alert(vv)	
		// frappe.call({
		// 			"method":"wtt_module.wtt_module.doctype.party_name.party_name.update_contact",
		// 			args:{
		// 				"first_name":frm.doc.first_name,
		// 				"middle_name":frm.doc.middle_name,
		// 				"last_name":frm.doc.last_name,
		// 				"email_id":frm.doc.email_id,
		// 				"address":frm.doc.address,
		// 				"status":frm.doc.status,
		// 				"salutation":frm.doc.salutation,
		// 				"designation":frm.doc.designation,
		// 				"gender":frm.doc.gender,
		// 				"phone":frm.doc.phone,
		// 				"mobile_no":frm.doc.mobile_no,
		// 				"company_name":frm.doc.company_name
		// 			},
		// 			callback: function(r) {
		// 				console.log('success')
		// 			}
		// 		});
	// refresh: function(frm) {

	// }


frappe.ui.form.on('Dynamic Link', {
link_name:function(frm, cdt, cdn){
	var child = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "link_title",child.link_name)
}
});
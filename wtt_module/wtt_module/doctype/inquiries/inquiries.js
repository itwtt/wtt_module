// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext");
cur_frm.email_field = "email_id";

erpnext.LeadController = frappe.ui.form.Controller.extend({
	// setup: function () {
	// 	this.frm.make_methods = {
	// 		'Customer': this.make_customer,
	// 		'Quotation': this.make_quotation,
	// 		'Opportunity': this.make_opportunity
	// 	};

	// 	this.frm.toggle_reqd("lead_name", !this.frm.doc.organization_lead);
	// },

	// onload: function () {
	// 	this.frm.set_query("customer", function (doc, cdt, cdn) {
	// 		return { query: "erpnext.controllers.queries.customer_query" }
	// 	});

	// 	this.frm.set_query("lead_owner", function (doc, cdt, cdn) {
	// 		return { query: "frappe.core.doctype.user.user.user_query" }
	// 	});

	// 	this.frm.set_query("contact_by", function (doc, cdt, cdn) {
	// 		return { query: "frappe.core.doctype.user.user.user_query" }
	// 	});
	// },

	// refresh: function () {
	// 	let doc = this.frm.doc;
	// 	erpnext.toggle_naming_series();
	// 	frappe.dynamic_link = { doc: doc, fieldname: 'name', doctype: 'Inquiries' }

	// 	if (!this.frm.is_new() && doc.__onload && !doc.__onload.is_customer) {
	// 		this.frm.add_custom_button(__("Customer"), this.make_customer, __("Create"));
	// 	}

	// 	if (!this.frm.is_new()) {
	// 		frappe.contacts.render_address_and_contact(this.frm);
	// 	} else {
	// 		frappe.contacts.clear_address_and_contact(this.frm);
	// 	}
	// },

	// make_customer: function () {
	// 	frappe.model.open_mapped_doc({
	// 		method: "erpnext.crm.doctype.lead.lead.make_customer",
	// 		frm: cur_frm
	// 	})
	// },

	// organization_lead: function () {
	// 	this.frm.toggle_reqd("lead_name", !this.frm.doc.organization_lead);
	// 	this.frm.toggle_reqd("company_name", this.frm.doc.organization_lead);
	// },

	// company_name: function () {
	// 	if (this.frm.doc.organization_lead && !this.frm.doc.lead_name) {
	// 		this.frm.set_value("lead_name", this.frm.doc.company_name);
	// 	}
	// },

	// contact_date: function () {
	// 	if (this.frm.doc.contact_date) {
	// 		let d = moment(this.frm.doc.contact_date);
	// 		d.add(1, "day");
	// 		this.frm.set_value("ends_on", d.format(frappe.defaultDatetimeFormat));
	// 	}
	// },
	
	// send_message: function(){
	// 	frappe.call({
	// 		method:"wtt_module.wtt_module.doctype.inquiries.inquiries.send_mail",
	// 		args:{
	// 			sender:this.frm.doc.sender,
	// 			receiver:this.frm.doc.mail_id,
	// 			cc:this.frm.doc.mail_cc,
	// 			subject:this.frm.doc.subject,
	// 			message:this.frm.doc.message
	// 		},
	// 		callback(r){
	// 			msgprint("Message Sending")
	// 		}
	// 	})

	// }
});
$.extend(cur_frm.cscript, new erpnext.LeadController({ frm: cur_frm }));

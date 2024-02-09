// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


cur_frm.add_fetch('contact', 'email_id', 'email_id')

frappe.ui.form.on("Request for Quotation",{
	after_save:function(frm,cdt,cdn){
		frappe.call({
			method:"wtt_module.customization.custom.request_for_quotation.combine_table",
			args:{
				doc:frm.doc.name
			},
			callback(r){
				frm.reload_doc()
			}
		})
	},
	setup: function(frm) {
		frm.get_docfield("items").allow_bulk_edit = 1;
		frm.get_docfield("combined_table").allow_bulk_edit = 1;
		frm.custom_make_buttons = {
			'Supplier Quotation': 'Create'
		}

		frm.fields_dict["suppliers"].grid.get_field("contact").get_query = function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				query: "erpnext.buying.doctype.request_for_quotation.request_for_quotation.get_supplier_contacts",
				filters: {'supplier': d.supplier}
			}
		}
	},

	onload: function(frm) {
		if(!frm.doc.message_for_supplier) {
			frm.set_value("message_for_supplier", __("Please supply the specified items at the best possible rates"))
		}
	},

	refresh: function(frm, cdt, cdn) {
		if (frm.doc.docstatus === 1) {

			frm.add_custom_button(__('Supplier Quotation'),
				function(){ frm.trigger("custom_route_supplier_quotation") }, __("Create"));


			frm.add_custom_button(__("Send Emails to Suppliers"), function() {
				frappe.call({
					method: 'erpnext.buying.doctype.request_for_quotation.request_for_quotation.send_supplier_emails',
					freeze: true,
					args: {
						rfq_name: frm.doc.name
					},
					callback: function(r){
						frm.reload_doc();
					}
				});
			}, __("Tools"));

			frm.add_custom_button(__('Download PDF'), () => {
				var suppliers = [];
				const fields = [{
					fieldtype: 'Link',
					label: __('Select a Supplier'),
					fieldname: 'supplier',
					options: 'Supplier',
					reqd: 1,
					get_query: () => {
						return {
							filters: [
								["Supplier", "name", "in", frm.doc.suppliers.map((row) => {return row.supplier;})]
							]
						}
					}
				}];

				frappe.prompt(fields, data => {
					var child = locals[cdt][cdn]

					var w = window.open(
						frappe.urllib.get_full_url("/api/method/erpnext.buying.doctype.request_for_quotation.request_for_quotation.get_pdf?"
						+"doctype="+encodeURIComponent(frm.doc.doctype)
						+"&name="+encodeURIComponent(frm.doc.name)
						+"&supplier="+encodeURIComponent(data.supplier)
						+"&no_letterhead=0"));
					if(!w) {
						frappe.msgprint(__("Please enable pop-ups")); return;
					}
				},
				'Download PDF for Supplier',
				'Download');
			},
			__("Tools"));

			frm.page.set_inner_btn_group_as_primary(__('Create'));
		}

		frm.add_custom_button(__('Materials to Excel'), () => frm.events.get_items(frm),
			__("Export"));
	},
	get_items:function(frm,cdt,cdn){
		frappe.call({
			method:"wtt_module.customization.custom.request_for_quotation.create_excel",
			args:{
				doc:frm.doc.combined_table,
				rfq:frm.doc.name
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
	custom_route_supplier_quotation:function(frm){
		var doc = frm.doc;
		var dialog = new frappe.ui.Dialog({
			title: __("Create Supplier Quotation"),
			fields: [
				{	"fieldtype": "Select", "label": __("Supplier"),
					"fieldname": "supplier",
					"options": doc.suppliers.map(d => d.supplier),
					"reqd": 1,
					"default": doc.suppliers.length === 1 ? doc.suppliers[0].supplier_name : "" },
			],
			primary_action_label: __("Create"),
			primary_action: (args) => {
				if(!args) return;
				dialog.hide();

				return frappe.call({
					type: "GET",
					method: "wtt_module.customization.custom.request_for_quotation.make_supplier_quotation_from_rfq",
					args: {
						"source_name": doc.name,
						"for_supplier": args.supplier
					},
					freeze: true,
					callback: function(r) {
						if(!r.exc) {
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", r.message.doctype, r.message.name);
						}
					}
				});
			}
		});

		dialog.show()
	},
	make_suppplier_quotation: function(frm) {
		var doc = frm.doc;
		var dialog = new frappe.ui.Dialog({
			title: __("Create Supplier Quotation"),
			fields: [
				{	"fieldtype": "Select", "label": __("Supplier"),
					"fieldname": "supplier",
					"options": doc.suppliers.map(d => d.supplier),
					"reqd": 1,
					"default": doc.suppliers.length === 1 ? doc.suppliers[0].supplier_name : "" },
			],
			primary_action_label: __("Create"),
			primary_action: (args) => {
				if(!args) return;
				dialog.hide();

				return frappe.call({
					type: "GET",
					method: "wtt_module.customization.custom.request_for_quotation.make_supplier_quotation_from_rfq",
					args: {
						"source_name": doc.name,
						"for_supplier": args.supplier
					},
					freeze: true,
					callback: function(r) {
						if(!r.exc) {
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", [r.message.doctype,'request_for_quotation'], [r.message.name,frm.doc.name]);
						}
					}
				});
			}
		});

		dialog.show()
	},

	schedule_date(frm) {
		if(frm.doc.schedule_date){
			frm.doc.items.forEach((item) => {
				item.schedule_date = frm.doc.schedule_date;
			})
		}
		refresh_field("items");
	},
	preview: (frm) => {
		let dialog = new frappe.ui.Dialog({
			title: __('Preview Email'),
			fields: [
				{
					label: __('Supplier'),
					fieldtype: 'Select',
					fieldname: 'supplier',
					options: frm.doc.suppliers.map(row => row.supplier),
					reqd: 1
				},
				{
					fieldtype: 'Column Break',
					fieldname: 'col_break_1',
				},
				{
					label: __('Subject'),
					fieldtype: 'Data',
					fieldname: 'subject',
					read_only: 1,
					depends_on: 'subject'
				},
				{
					fieldtype: 'Section Break',
					fieldname: 'sec_break_1',
					hide_border: 1
				},
				{
					label: __('Email'),
					fieldtype: 'HTML',
					fieldname: 'email_preview'
				},
				{
					fieldtype: 'Section Break',
					fieldname: 'sec_break_2'
				},
				{
					label: __('Note'),
					fieldtype: 'HTML',
					fieldname: 'note'
				}
			]
		});

		dialog.fields_dict['supplier'].df.onchange = () => {
			var supplier = dialog.get_value('supplier');
			frm.call('get_supplier_email_preview', {supplier: supplier}).then(result => {
				dialog.fields_dict.email_preview.$wrapper.empty();
				dialog.fields_dict.email_preview.$wrapper.append(result.message);
			});

		}

		dialog.fields_dict.note.$wrapper.append(`<p class="small text-muted">This is a preview of the email to be sent. A PDF of the document will
			automatically be attached with the email.</p>`);

		dialog.set_value("subject", frm.doc.subject);
		dialog.show();
	}
})
frappe.ui.form.on("Request for Quotation Item", {
	items_add(frm, cdt, cdn) {
		if (frm.doc.schedule_date) {
			frappe.model.set_value(cdt, cdn, 'schedule_date', frm.doc.schedule_date);
		}
	}
});
frappe.ui.form.on("Request for Quotation Supplier",{
	supplier: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn]
		frappe.call({
			method:"erpnext.accounts.party.get_party_details",
			args:{
				party: d.supplier,
				party_type: 'Supplier'
			},
			callback: function(r){
				if(r.message){
					frappe.model.set_value(cdt, cdn, 'contact', r.message.contact_person)
					frappe.model.set_value(cdt, cdn, 'email_id', r.message.contact_email)
				}
			}
		})
	},

})

// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Final bank statement', {
	setup:function(frm){
		frm.set_query("paid_from", function() {
			// frm.events.validate_company(frm);

			var account_types = ["Bank", "Cash"];
			return {
				filters: {
					"account_type": ["in", account_types],
					"is_group": 0,
					"company": frm.doc.company
				}
			}
		});
	},
	before_save:function(frm){
		frappe.call({
			method:"num_to_word",
			doc:frm.doc
		})
	},
	validate:function(frm){
		var total_amount=0;
		var total_charge=0;
		var ib_total_amount=0;
		var ib_total_charge=0;
		var net=0;
		$.each(frm.doc.amount_table, function (i,d) {
			total_amount+=d.amount
			total_charge+=d.charges
		});
		$.each(frm.doc.ib_amount_table, function (i,d) {
			ib_total_amount+=d.amount
			ib_total_charge+=d.charges
		});

		
		frm.set_value("grand_total",total_amount);
		frm.set_value("total_charges",total_charge);
		frm.set_value("net_total",Math.round(total_amount+total_charge));
		frm.set_value("ib_grand_total",ib_total_amount);
		frm.set_value("ib_total_charges",ib_total_charge);
		frm.set_value("ib_net_total",Math.round(ib_total_amount+ib_total_charge));
		
		var adv=[]
		$.each(frm.doc.ib_amount_table, function (a,b) {
			adv.push(b.benificiary_name)
		});

		var addv=[]
		$.each(frm.doc.amount_table, function (k,v) {
			addv.push(v.benificiary_name)
		});

		$.each(frm.doc.statement_advance_table, function (c,d) {
			if(adv.includes(d.supplier))
			{
				frappe.model.set_value(d.doctype, d.name, "cheque_no", frm.doc.ib_cheque);
			}
		});

		$.each(frm.doc.statement_advance_table, function (m,n) {
			if(addv.includes(n.supplier))
			{
				frappe.model.set_value(n.doctype, n.name, "cheque_no", frm.doc.cheque);
			}
		});


		$.each(frm.doc.statement_freight_table, function (c,d) {
			if(adv.includes(d.transport))
			{
				frappe.model.set_value(d.doctype, d.name, "cheque_no", frm.doc.ib_cheque);
			}
		});

		$.each(frm.doc.statement_freight_table, function (m,n) {
			if(addv.includes(n.transport))
			{
				frappe.model.set_value(n.doctype, n.name, "cheque_no", frm.doc.cheque);
			}
		});

		$.each(frm.doc.statement_overdue_table, function (c,d) {
			if(adv.includes(d.supplier))
			{
				frappe.model.set_value(d.doctype, d.name, "cheque_no", frm.doc.ib_cheque);
			}
		});

		$.each(frm.doc.statement_overdue_table, function (m,n) {
			if(addv.includes(n.supplier))
			{
				frappe.model.set_value(n.doctype, n.name, "cheque_no", frm.doc.cheque);
			}
		});

	},
	refresh: function(frm) {
		frm.add_custom_button(__('Other Bank'), () => frm.events.get_bank(frm),
			__("Export"));

		frm.add_custom_button(__('Indian Bank'), () => frm.events.get_ib(frm),
			__("Export"));
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Advance Payment'), () => frm.events.get_advance(frm),
				__("Payment"));

			frm.add_custom_button(__('Freight Advance'), () => frm.events.get_freight(frm),
				__("Payment"));

			frm.add_custom_button(__('Credit Payment'), () => frm.events.get_credit(frm),
				__("Payment"));
			frm.add_custom_button(__('Request for Payment'), () => frm.events.get_purchase_rop(frm),
				__("Payment"));
			// frm.add_custom_button(__('Request for Payment'), () => frm.events.get_rop(frm),
			// 	__("Payment"));
			frm.add_custom_button(__('Landed Cost Voucher'), () => frm.events.get_lcv(frm),
				__("Payment"));
			frm.add_custom_button(__('Salary Arrears'), () => frm.events.get_arrear(frm),
				__("Payment"));
			frm.add_custom_button(__('Logistics Module'), () => frm.events.get_logistics(frm),
				__("Payment"));
			
		}
		if(frappe.session.user=="Administrator"){
			frm.add_custom_button(__('Check'), () => frm.events.function_name(frm));
		}
		
	},
	function_name:function(frm){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.final_bank_statement.final_bank_statement.test_func",
			args:{
				doc:frm.doc.name
			}
			
		})		
	},
	get_bank:function(frm){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.final_bank_statement.final_bank_statement.create_excel",
			args:{
				dds:frm.doc.amount_table
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
			method:"wtt_module.wtt_module.doctype.final_bank_statement.final_bank_statement.create_excel_ib",
			args:{
				doc:frm.doc.ib_amount_table
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
	get_advance:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.final_bank_statement.final_bank_statement.make_advance",
					source_doctype: "Payment Module",
					target: frm,
					setters: {
						company: frm.doc.company
					},
					get_query_filters: {
						docstatus: 1,
						payment_type:'Advance Payment'
					}
				});
	},
	get_freight:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.final_bank_statement.final_bank_statement.make_freight",
					source_doctype: "Payment Module",
					target: frm,
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 1,
						payment_type:'Freight Payment'
					}
				});
	},
	get_credit:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.final_bank_statement.final_bank_statement.make_credit",
					source_doctype: "Payment Module",
					target: frm,
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 1,
						payment_type:'Invoice Payment'
					}
				});
	
	},
	get_rop:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.final_bank_statement.final_bank_statement.make_rop",
					source_doctype: "Request for Payment",
					target: frm,
					setters: {
						party:frm.doc.party,
						company: ""
					},
					get_query_filters: {
						docstatus: 1
					}
				});
	
	},
	get_purchase_rop:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.final_bank_statement.final_bank_statement.make_purchase_rop",
					source_doctype: "Payment Module",
					target: frm,
					setters: {
						party:frm.doc.party,
						company: ""
					},
					get_query_filters: {
						docstatus: 1,
						payment_type:'Request for Payment'
					}
				});
	
	},
	get_lcv:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.final_bank_statement.final_bank_statement.make_lcv",
					source_doctype: "Payment Module",
					target: frm,
					setters: {
						company: frm.doc.company
					},
					get_query_filters: {
						docstatus: 1,
						payment_type:'Landed Cost Voucher'
					}
				});
	},
	get_logistics:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.final_bank_statement.final_bank_statement.make_logistics",
					source_doctype: "Payment Module",
					target: frm,
					setters: {
						company: frm.doc.company
					},
					get_query_filters: {
						docstatus: 1,
						payment_type:'Logistics Payment'
					}
				});
		},
});

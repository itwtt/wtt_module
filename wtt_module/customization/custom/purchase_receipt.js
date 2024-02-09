// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

{% include 'erpnext/stock/doctype/purchase_receipt/purchase_receipt.js' %};

frappe.provide("erpnext.stock");

frappe.ui.form.on("Purchase Receipt", {
	validate:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		var ar=[];
		$.each(frm.doc.items || [], function(i, v) {
			if(v.not_ordered!=1){
				if(frm.doc.naming_series=='PR-.YY.-' || frm.doc.name.slice(0, 2)=="PR"){				
				if(v.material_request==undefined || v.material_request_item==undefined){frappe.throw("Make sure that MR has Linked to "+v.idx)}
				}
				if(v.purchase_order==undefined || v.purchase_order_item==undefined){frappe.throw("Please give PO Link for the Row "+v.idx)}

				if(ar.includes(v.purchase_order_item)){
					frappe.throw("#Row "+(v.idx)+" has already exists")
				}
				else{
					ar.push(v.purchase_order_item)
				}
			}
				
		});

	},
	for_site:function(frm,cdt,cdn){
		if(frm.doc.for_site==1){
			frm.set_df_property("material_movement","hidden",1)
		}
		else{
			frm.set_df_property("material_movement","hidden",0)	
		}
	},

	track_items:function(frm,cdt,cdn){
	 	frm.set_df_property("hide_table","hidden",0);
	 	frm.set_df_property("track_items","hidden",1);
	 	var child = locals[cdt][cdn];
		var ar="";
		var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
		htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%'>S.NO</th><th style='width:4%'>DESCRIPTION</th><th style='width:1%'>MR ROW</th></tr>"
		frappe.call({
			method:"wtt_module.customization.custom.frappe_call.track_items",
			args:{
				"table":frm.doc.items
			},
			callback(r){
				
				for(var i=0;i<r.message.length;i++){
					
					var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
					htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%'>PR ROW</th><th style='width:4%'>DESCRIPTION</th><th style='width:12%'>TECHNICAL DESCRIPTION</th><th style='width:8%'>PR QTY</th><th style='width:5%'>PO QTY</th><th style='width:5%'>PO DETAIL</th><th style='width:8%'>MR QTY</th><th style='width:5%'>MR DETAIL</th></tr>"
					
					$.each(r.message, function(i, v) {
					var result=""
					var c=i+1
					if(v.technical_description!="")
					{
					var gug=[]
					var vis=v.technical_description.split(",")
					var vg='<br>'
					for(var g in vis)
					{
					// gug.push("<td>")
					gug.push(vis[g])
					gug.push(vg)
					}
					result = gug.toString().replace(/,/g, "");
					}
					
					htvalue+='<tr style="text-align:center;"><td align="center">'+c+'</td><td align="center">'+v.description+'<br></td><td align="center">'+result+'<br></td><td align="center">'+v.pr_qty+'</td><td align="center">'+v.po_qty+'</td><td align="center">'+v.po_detail+'</td><td>'+v.mr_qty+'</td><td>'+v.mr_detail+'</td></tr>'
					});
					$(frm.fields_dict['ht'].wrapper).html(htvalue)					
					}
				
			}
		})
	},

	hide_table:function(frm,cdt,cdn){
		frm.set_df_property("hide_table","hidden",1);
	 	frm.set_df_property("track_items","hidden",0);
		$(frm.fields_dict['ht'].wrapper).html("")

	},



	clear_items:function(frm){
		frm.clear_table("items")
		frm.refresh_field("items");
	},

	setup: (frm) => {
		frm.make_methods = {
			'Landed Cost Voucher': () => {
				let lcv = frappe.model.get_new_doc('Landed Cost Voucher');
				lcv.company = frm.doc.company;

				let lcv_receipt = frappe.model.get_new_doc('Landed Cost Purchase Receipt');
				lcv_receipt.receipt_document_type = 'Purchase Receipt';
				lcv_receipt.receipt_document = frm.doc.name;
				lcv_receipt.supplier = frm.doc.supplier;
				lcv_receipt.grand_total = frm.doc.grand_total;
				lcv.purchase_receipts = [lcv_receipt];

				frappe.set_route("Form", lcv.doctype, lcv.name);
			},
		}

		frm.custom_make_buttons = {
			'Stock Entry': 'Return'
			//'Purchase Invoice': 'Purchase Invoice'
		};

		frm.set_query("expense_account", "items", function() {
			return {
				query: "erpnext.controllers.queries.get_expense_account",
				filters: {'company': frm.doc.company }
			}
		});
		frm.set_query("material_movement", function() {
		return {
			filters: [
				["Material Movement","docstatus","=", 1]
			]
		}
		});


		frm.set_query("taxes_and_charges", function() {
			return {
				filters: {'company': frm.doc.company }
			}
		});

	},
	onload: function(frm) {
		erpnext.queries.setup_queries(frm, "Warehouse", function() {
			return erpnext.queries.warehouse(frm.doc);
		});

		erpnext.accounts.dimensions.setup_dimension_filters(frm, frm.doctype);
	},

	refresh: function(frm) {
		if(frappe.session.user=='venkat@wttindia.com' || frappe.session.user=='sarnita@wttindia.com'){
			frm.add_custom_button(__('Allow Ovebilling'), () => frm.events.function_name(frm));	
		}
		$(frm.fields_dict['ht'].wrapper).html("")
		if(frm.doc.company) {
			frm.trigger("toggle_display_account_head");
		}

		if(frm.doc.docstatus==0){
			frm.add_custom_button(__('Item Inspection'), function() {
				frappe.model.open_mapped_doc({
					method: "wtt_module.customization.custom.purchase_receipt.make_quality",
					frm: cur_frm,
				})
			}, __('Create'));
		}
			

		if (frm.doc.docstatus === 1 && frm.doc.is_return === 1 && frm.doc.per_billed !== 100) {
			frm.add_custom_button(__('Debit Note'), function() {
				frappe.model.open_mapped_doc({
					method: "erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_purchase_invoice",
					frm: cur_frm,
				})
			}, __('Create'));
			


			frm.page.set_inner_btn_group_as_primary(__('Create'));
		}

		if (frm.doc.docstatus === 1 && frm.doc.is_internal_supplier && !frm.doc.inter_company_reference) {
			frm.add_custom_button(__('Delivery Note'), function() {
				frappe.model.open_mapped_doc({
					method: 'erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_inter_company_delivery_note',
					frm: cur_frm,
				})
			}, __('Create'));
		}

		frm.events.add_custom_buttons(frm);

		var mail=0
		$.each(frm.doc.items || [], function(i, v) {
			if(v.inspection_status == 'Debit')
			{
				mail=1
			}
		});

		if(mail == 1)
		{
			frm.add_custom_button(__('Send Mail to purchase'), () => frm.events.mail_send(frm));
		}

		frm.set_query("to_be_inspected_by", function() {
			return {
				filters: [
					["Employee","status","=", 'Active']
				]
			}

		});
	},
	function_name:function(frm){
		frappe.confirm('Are you sure you want to proceed?',
	    () => {
	        frappe.call({
			method:"wtt_module.customization.custom.frappe_call.allow_overbilling",
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
	mail_send:function(frm){
		frappe.confirm('Are you sure you send the mail to purchase?',
	    () => {
	        frappe.call({
			method:"wtt_module.customization.custom.frappe_call.mail_send",
			args:{
				"ref_name":frm.doc.name
			},
			callback(r){
				frappe.msgprint("Mail sent")
				frm.set_value("mail_status","Mail Sent");
				frm.refresh_field("mail_status");
				frm.save();
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
	company: function(frm) {
		frm.trigger("toggle_display_account_head");
		erpnext.accounts.dimensions.update_dimension(frm, frm.doctype);
	},

	toggle_display_account_head: function(frm) {
		var enabled = erpnext.is_perpetual_inventory_enabled(frm.doc.company)
		frm.fields_dict["items"].grid.set_column_disp(["cost_center"], enabled);
	}
});
frappe.ui.form.on("Purchase Receipt Item", {
	rejected_qty:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(child.doctype,child.name,"debit_quantity",child.rejected_qty)
		frm.refresh_field("debit_quantity");
	}
});
frappe.ui.form.on("PR Status",{
	setup:function(frm,cdt,cdn){
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status","=", 'Active']
				]
			}

		});
	},
	verifications_add: function(frm,cdt,cdn) {
		var child=locals[cdt][cdn];
		frappe.db.get_value("Employee",{"user_id":frappe.session.user},'name')
			.then(r => {
		        child.employee=r.message.name;
		        child.employee_name=frappe.session.user_fullname;
		    })
		frm.refresh_field("verifications");
	}
})
// erpnext.stock.PurchaseReceiptController = erpnext.buying.BuyingController.extend({
// 	setup: function(doc) {
// 		this.setup_posting_date_time_check();
// 		this._super(doc);
// 	},

// 	refresh: function() {
// 		var me = this;
// 		this._super();
// 		if(this.frm.doc.docstatus > 0) {
// 			this.show_stock_ledger();
// 			//removed for temporary
// 			this.show_general_ledger();

// 			this.frm.add_custom_button(__('Asset'), function() {
// 				frappe.route_options = {
// 					purchase_receipt: me.frm.doc.name,
// 				};
// 				frappe.set_route("List", "Asset");
// 			}, __("View"));

// 			this.frm.add_custom_button(__('Asset Movement'), function() {
// 				frappe.route_options = {
// 					reference_name: me.frm.doc.name,
// 				};
// 				frappe.set_route("List", "Asset Movement");
// 			}, __("View"));
// 		}

// 		if(!this.frm.doc.is_return && this.frm.doc.status!="Closed") {
// 			if (this.frm.doc.docstatus == 0) {
// 				this.frm.add_custom_button(__('Purchase Order'),
// 					function () {
// 						if (!me.frm.doc.supplier) {
// 							frappe.throw({
// 								title: __("Mandatory"),
// 								message: __("Please Select a Supplier")
// 							});
// 						}
// 						erpnext.utils.map_current_doc({
// 							method: "wtt_module.customization.custom.purchase_order.make_purchase_receipt",
// 							source_doctype: "Purchase Order",
// 							target: me.frm,
// 							setters: {
// 								supplier: me.frm.doc.supplier,
// 								schedule_date: undefined
// 							},
// 							get_query_filters: {
// 								docstatus: 1,
// 								status: ["not in", ["Closed", "On Hold"]],
// 								per_received: ["<", 99.99],
// 								company: me.frm.doc.company
// 							}
// 						})
// 					}, __("Get Items From"));
// 			}

// 			if(this.frm.doc.docstatus == 1 && this.frm.doc.status!="Closed") {
// 				if (this.frm.has_perm("submit")) {
// 					cur_frm.add_custom_button(__("Close"), this.close_purchase_receipt, __("Status"))
// 				}

// 				cur_frm.add_custom_button(__('Purchase Return'), this.make_purchase_return, __('Create'));

// 				cur_frm.add_custom_button(__('Make Stock Entry'), cur_frm.cscript['Make Stock Entry'], __('Create'));

// 				// if(flt(this.frm.doc.per_billed) < 100) {
// 				// 	cur_frm.add_custom_button(__('Purchase Invoice'), this.make_purchase_invoice, __('Create'));
// 				// }
// 				cur_frm.add_custom_button(__('Retention Stock Entry'), this.make_retention_stock_entry, __('Create'));

// 				if(!this.frm.doc.auto_repeat) {
// 					cur_frm.add_custom_button(__('Subscription'), function() {
// 						erpnext.utils.make_subscription(me.frm.doc.doctype, me.frm.doc.name)
// 					}, __('Create'))
// 				}

// 				cur_frm.page.set_inner_btn_group_as_primary(__('Create'));
// 			}
// 		}


// 		if(this.frm.doc.docstatus==1 && this.frm.doc.status === "Closed" && this.frm.has_perm("submit")) {
// 			cur_frm.add_custom_button(__('Reopen'), this.reopen_purchase_receipt, __("Status"))
// 		}

// 		this.frm.toggle_reqd("supplier_warehouse", this.frm.doc.is_subcontracted==="Yes");
// 	},

// 	make_purchase_invoice: function() {
// 		frappe.model.open_mapped_doc({
// 			method: "erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_purchase_invoice",
// 			frm: cur_frm
// 		})
// 	},

// 	make_purchase_return: function() {
// 		frappe.model.open_mapped_doc({
// 			method: "erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_purchase_return",
// 			frm: cur_frm
// 		})
// 	},

// 	close_purchase_receipt: function() {
// 		cur_frm.cscript.update_status("Closed");
// 	},

// 	reopen_purchase_receipt: function() {
// 		cur_frm.cscript.update_status("Submitted");
// 	},

// 	make_retention_stock_entry: function() {
// 		frappe.call({
// 			method: "erpnext.stock.doctype.stock_entry.stock_entry.move_sample_to_retention_warehouse",
// 			args:{
// 				"company": cur_frm.doc.company,
// 				"items": cur_frm.doc.items
// 			},
// 			callback: function (r) {
// 				if (r.message) {
// 					var doc = frappe.model.sync(r.message)[0];
// 					frappe.set_route("Form", doc.doctype, doc.name);
// 				}
// 				else {
// 					frappe.msgprint(__("Purchase Receipt doesn't have any Item for which Retain Sample is enabled."));
// 				}
// 			}
// 		});
// 	},

// 	apply_putaway_rule: function() {
// 		if (this.frm.doc.apply_putaway_rule) erpnext.apply_putaway_rule(this.frm);
// 	}

// });

// // for backward compatibility: combine new and previous states
// $.extend(cur_frm.cscript, new erpnext.stock.PurchaseReceiptController({frm: cur_frm}));

// cur_frm.cscript.update_status = function(status) {
// 	frappe.ui.form.is_saving = true;
// 	frappe.call({
// 		method:"erpnext.stock.doctype.purchase_receipt.purchase_receipt.update_purchase_receipt_status",
// 		args: {docname: cur_frm.doc.name, status: status},
// 		callback: function(r){
// 			if(!r.exc)
// 				cur_frm.reload_doc();
// 		},
// 		always: function(){
// 			frappe.ui.form.is_saving = false;
// 		}
// 	})
// }

// cur_frm.fields_dict['items'].grid.get_field('project').get_query = function(doc, cdt, cdn) {
// 	return {
// 		filters: [
// 			['Project', 'status', 'not in', 'Completed, Cancelled']
// 		]
// 	}
// }

// cur_frm.fields_dict['select_print_heading'].get_query = function(doc, cdt, cdn) {
// 	return {
// 		filters: [
// 			['Print Heading', 'docstatus', '!=', '2']
// 		]
// 	}
// }

// cur_frm.fields_dict['items'].grid.get_field('bom').get_query = function(doc, cdt, cdn) {
// 	var d = locals[cdt][cdn]
// 	return {
// 		filters: [
// 			['BOM', 'item', '=', d.item_code],
// 			['BOM', 'is_active', '=', '1'],
// 			['BOM', 'docstatus', '=', '1']
// 		]
// 	}
// }

// frappe.provide("erpnext.buying");

// frappe.ui.form.on("Purchase Receipt", "is_subcontracted", function(frm) {
// 	if (frm.doc.is_subcontracted === "Yes") {
// 		erpnext.buying.get_default_bom(frm);
// 	}
// 	frm.toggle_reqd("supplier_warehouse", frm.doc.is_subcontracted==="Yes");
// });

// frappe.ui.form.on('Purchase Receipt Item', {
// 	item_code: function(frm, cdt, cdn) {
// 		var d = locals[cdt][cdn];
// 		frappe.db.get_value('Item', {name: d.item_code}, 'sample_quantity', (r) => {
// 			frappe.model.set_value(cdt, cdn, "sample_quantity", r.sample_quantity);
// 			validate_sample_quantity(frm, cdt, cdn);
// 		});
// 	},
// 	// received_qty:function(frm,cdt,cdn){
// 	// 	var d = locals[cdt][cdn];
// 	// 	frappe.model.set_value(cdt, cdn, "qty", d.received_qty);
// 	// },
// 	qty: function(frm, cdt, cdn) {
// 		validate_sample_quantity(frm, cdt, cdn);
// 	},
// 	sample_quantity: function(frm, cdt, cdn) {
// 		validate_sample_quantity(frm, cdt, cdn);
// 	},
// 	batch_no: function(frm, cdt, cdn) {
// 		validate_sample_quantity(frm, cdt, cdn);
// 	},
// });

// cur_frm.cscript['Make Stock Entry'] = function() {
// 	frappe.model.open_mapped_doc({
// 		method: "erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_stock_entry",
// 		frm: cur_frm,
// 	})
// }

// var validate_sample_quantity = function(frm, cdt, cdn) {
// 	var d = locals[cdt][cdn];
// 	if (d.sample_quantity && d.qty) {
// 		frappe.call({
// 			method: 'erpnext.stock.doctype.stock_entry.stock_entry.validate_sample_quantity',
// 			args: {
// 				batch_no: d.batch_no,
// 				item_code: d.item_code,
// 				sample_quantity: d.sample_quantity,
// 				qty: d.qty
// 			},
// 			callback: (r) => {
// 				frappe.model.set_value(cdt, cdn, "sample_quantity", r.message);
// 			}
// 		});
// 	}
// };

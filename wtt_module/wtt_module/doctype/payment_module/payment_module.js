// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Module', {
	paid_amount:function(frm){
		frm.set_value("received_amount",frm.doc.paid_amount);
		frm.refresh_field("received_amount");
		frm.set_value("total_amount",frm.doc.paid_amount);
		frm.refresh_field("total_amount");
		frm.set_df_property("total_amount","hidden",1);
	},
	received_amount:function(frm){
		frm.set_value("paid_amount",frm.doc.received_amount);
		frm.refresh_field("paid_amount");
		frm.set_value("total_amount",frm.doc.received_amount);
		frm.refresh_field("total_amount");
		frm.set_df_property("total_amount","hidden",1);
		
	},
	before_save:function(frm){
		if(frm.doc.payment_type=='Advance Payment')
		{
			var temp = frm.doc.advance_consolidate_table;
			var i,sum=0
			for(i=0;i<temp.length;i++)
			{
			sum+=temp[i].advance_amount;
			}
			frm.set_value("total_amount",sum);
			frm.refresh_field("total_amount");
			
		}
		else if(frm.doc.payment_type=='Freight Payment')
		{
			var temp = frm.doc.freight_consolidate_table;
			var i,sum=0
			for(i=0;i<temp.length;i++)
			{
			sum+=temp[i].advance_amount;
			}
			frm.set_value("total_amount",sum);
			frm.refresh_field("total_amount");
		}
		else if(frm.doc.payment_type=='Invoice Payment')
		{
			var temp = frm.doc.consolidate_table;
			var i,sum=0
			for(i=0;i<temp.length;i++)
			{
			sum+=temp[i].total;
			}
			frm.set_value("total_amount",sum);
			frm.refresh_field("total_amount");
		}
		else if(frm.doc.payment_type=='Landed Cost Voucher')
		{
			var temp = frm.doc.landed_table;
			var i,sum=0
			for(i=0;i<temp.length;i++)
			{
			sum+=temp[i].amount;
			}
			frm.set_value("total_amount",sum);
			frm.refresh_field("total_amount");
		}

	},
	check_balance:function(frm){
		if(frappe.session.user=='venkat@wttindia.com'|| frappe.session.user=='sarnita@wttindia.com' || frappe.session.user=='Administrator'){
			var html='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>' 
			html+="<table border='1px' width=100% text-align='center'><tr><th>Account</th><th>Balance</th></tr>"
			$(frm.fields_dict['account_details'].wrapper).html(html)
			frappe.call({
				method:"wtt_module.wtt_module.doctype.payment_module.payment_module.get_pc_bal",
				args:{
					act:'PETTY CASH II - WTT'
				},
				callback(r){
					var x=r.message[0].balance;
				    x=x.toString();
				    var afterPoint = '';
				    if(x.indexOf('.') > 0){
				       afterPoint = x.substring(x.indexOf('.'),x.length);
				    }
				    x = Math.floor(x);
				    x=x.toString();
				    var lastThree = x.substring(x.length-3);
				    var bal = x.substring(0,x.length-3);
				    if(bal != ''){
				        lastThree = ',' + lastThree;
				    }
					var amt1=bal.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + lastThree + afterPoint;
					html+="<tr style='text-align:center;';><td><b>Petty Cash</b></td><td>₹ "+amt1+"</td></tr>"
					frappe.call({
						method:"wtt_module.wtt_module.doctype.payment_module.payment_module.get_ca_bal",
						args:{
							act:'7252302061 - INDIAN BANK-CA - WTT'
						},
						callback(r){
							var x=r.message[0].balance;
						    x=x.toString();
						    var afterPoint = '';
						    if(x.indexOf('.') > 0){
						       afterPoint = x.substring(x.indexOf('.'),x.length);
						    }
						    x = Math.floor(x);
						    x=x.toString();
						    var lastThree = x.substring(x.length-3);
						    var bal = x.substring(0,x.length-3);
						    if(bal != ''){
						        lastThree = ',' + lastThree;
						    }
							var amt2=bal.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + lastThree + afterPoint;
							html+="<tr style='text-align:center;';><td><b>Current Account</b></td><td>₹ "+amt2+"</td></tr>"
							frappe.call({
								method:"wtt_module.wtt_module.doctype.payment_module.payment_module.get_od_bal",
								args:{
									act:'6475173650 - INDIAN BANK-OCC - WTT'
								},
								callback(r){
									var x=r.message[0].balance;
								    x=x.toString();
								    var afterPoint = '';
								    if(x.indexOf('.') > 0){
								       afterPoint = x.substring(x.indexOf('.'),x.length);
								    }
								    x = Math.floor(x);
								    x=x.toString();
								    var lastThree = x.substring(x.length-3);
								    var bal = x.substring(0,x.length-3);
								    if(bal != ''){
								        lastThree = ',' + lastThree;
								    }
									var amt2=bal.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + lastThree + afterPoint;
									
									var bala = 100000000+parseFloat(x)
									bala=bala.toString();
								    var afterPoint = '';
								    if(bala.indexOf('.') > 0){
								       afterPoint = bala.substring(x.indexOf('.'),bala.length);
								    }
								    bala = Math.floor(bala);
								    bala=bala.toString();
								    var lastThree = bala.substring(bala.length-3);
								    var bala = bala.substring(0,bala.length-3);
								    if(bala != ''){
								        lastThree = ',' + lastThree;
								    }
									var balamt = bala.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + lastThree + afterPoint;
									
									html+="<tr style='text-align:center;';><td><b>OCC Account</b></td><td>"+amt2+"</td></tr>"
									html+="<tr style='text-align:center;';><td><b>Available OCC</b></td><td>₹ "+balamt+"</td></tr>"
									$(frm.fields_dict['account_details'].wrapper).html(html)
								}
							})
						}
					});
				}
			});	
		}
	},
	onload:function(frm){
		frm.page.wrapper.find('.grey-link.dropdown-item:contains("Duplicate")').hide();
		$(frm.fields_dict['account_details'].wrapper).html("");
	},
	payment_type:function(frm){
		if(frm.doc.payment_type=='Advance Payment')
		{
			frm.set_value('naming_series','PO-ADV-PAY-')
		}
		else if(frm.doc.payment_type=='Freight Payment')
		{
			frm.set_value('naming_series','PO-FRE-PAY-')
		}
		else if(frm.doc.payment_type=='Invoice Payment')
		{
			frm.set_value('naming_series','INV-PAY-')
		}
		else if(frm.doc.payment_type=='Request for Payment')
		{
			frm.set_value('naming_series','REQ-PAY-')
		}
		else if(frm.doc.payment_type=='Landed Cost Voucher')
		{
			frm.set_value('naming_series','LAN-COST-')
		}
		else if(frm.doc.payment_type=='Internal Transfer')
		{
			frm.set_value('naming_series','INT-TRANS-')
		}
		else if(frm.doc.payment_type=='Logistics Payment')
		{
			frm.set_value('naming_series','LMP-.YY.-')
		}
		else if(frm.doc.payment_type=='')
		{
			frm.set_value('naming_series','')
		}
	},
	setup: function(frm) {
		if(frappe.session.user=='venkat@wttindia.com'|| frappe.session.user=='sarnita@wttindia.com' || frappe.session.user=='Administrator'){
			frm.set_df_property("check_balance","hidden",0);
		}
		frm.get_docfield("consolidate_table").allow_bulk_edit = 1;
		frm.set_query("po", function() {
			return {
				filters: [
					["Purchase Order","workflow_state", "=", "Approved"]
					
				]
			};
		});

		frm.set_query("order_no", function() {
			return {
				filters: [
					["Purchase Order","workflow_state", "=", "Approved"]
					
				]
			};
		});
		if(frappe.session.user=="Administrator" || frappe.session.user=='venkat@wttindia.com'|| frappe.session.user=='sarnita@wttindia.com'){
			frm.set_df_property("current_account","hidden",0);
			frm.set_df_property("od_account","hidden",0);
			frm.set_df_property("petty_cash","hidden",0);
		}
	},
	refresh:function(frm){
		if(frm.doc.docstatus == 1)
		{
		if(frappe.session.user == 'venkat@wttindia.com' || frappe.session.user == 'sarnita@wttindia.com' || frappe.session.user == 'karthi@wtt1401.com' || frappe.session.user == 'Administrator' || frappe.session.user == 'nithyanandan@wttindia.com')
		{
			frm.add_custom_button(__('Transferred'), () => {
			// frm.set_value("payment_status","Transferred");
			// frm.save();
			frappe.call({
				method:"wtt_module.wtt_module.doctype.payment_module.payment_module.update_trans",
				args:{
					ref_name:frm.doc.name
				},
				callback(r) {
					frm.reload()
					frappe.msgprint("Updated")
				}
			})
			});

			frm.add_custom_button(__('In Progress'), () => {
			// frm.set_value("payment_status","In Progress");
			// frm.save();
			frappe.call({
				method:"wtt_module.wtt_module.doctype.payment_module.payment_module.update_inpro",
				args:{
					ref_name:frm.doc.name
				},
				callback(r) {
					frm.reload()
					frappe.msgprint("Updated")
				}
			})
			});

			frm.add_custom_button(__('Not Transferred'), () => {
			// frm.set_value("payment_status","Not Transferred");
			// frm.save();
			frappe.call({
				method:"wtt_module.wtt_module.doctype.payment_module.payment_module.update_not",
				args:{
					ref_name:frm.doc.name
				},
				callback(r) {
					frm.reload()
					frappe.msgprint("Updated")
				}
			})
			});
			}
		}
		frm.page.wrapper.find('.grey-link.dropdown-item:contains("Duplicate")').hide();
		if(frappe.session.user=='venkat@wttindia.com'|| frappe.session.user=='sarnita@wttindia.com'){
			frm.set_df_property("check_balance","hidden",0);
		}
		frm.get_field("advance_consolidate_table").grid.setup_download;
		frm.fields_dict['search_table'].grid.add_custom_button('Add items', () => {	
		var arr=[]
		var arr2=[]
		$.each(frm.doc.advance_table, function (index, source_row) {
			arr2.push(source_row.order_no)
		});
		$.each(frm.doc.search_table, function (index, source_row) {
			    if(source_row.__checked==true)
			    {   
			    	if(arr2.includes(source_row.order_no)){
			    		console.log("yes")
			    	}
			    	else{
			    		arr.push({
			    		"order_no":source_row.order_no,
			    		"supplier":source_row.supplier,
			    		"age":source_row.age,
			    		"advance":source_row.advance,
			    		"outstanding":source_row.amount-source_row.paid_advance,
			    		"amount":source_row.amount,
			    		"currency":source_row.currency,
			    		"amount_in_po":source_row.total_amount
			    		})
			    	}
			    }
		});
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.payment_module.payment_module.searched_item',
			args: { 
				gok:arr
			},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{     
				var child = frm.add_child("advance_table");
				frappe.model.set_value(child.doctype, child.name, "order_no", r.message[i].order_no);
				var tt=r.message[i].order_no.slice(6);
				frappe.model.set_value(child.doctype, child.name, "po_no", tt);
				frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
				frappe.model.set_value(child.doctype, child.name, "pro", r.message[i].project);
				frappe.model.set_value(child.doctype, child.name, "age", r.message[i].age);
				frappe.model.set_value(child.doctype, child.name, "advance", r.message[i].advance);
				frappe.model.set_value(child.doctype, child.name, "outstanding", r.message[i].outstanding);
				frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
				frappe.model.set_value(child.doctype, child.name, "currency", r.message[i].currency);
				frappe.model.set_value(child.doctype, child.name, "amount_in_po", r.message[i].amount_in_po);
				frm.refresh_field("advance_table");
				}
			}
		});
		});
			frm.fields_dict['overdue_table'].grid.add_custom_button('Add items', () => {
			var ar=[]
			var ar2=[]
			$.each(frm.doc.final_table, function (index, v) {
				ar2.push(v.invoice_no)
			});
			$.each(frm.doc.overdue_table, function (index, source_row) {
			        if(source_row.__checked==true)
			        {
			        if(ar2.includes(source_row.invoice_no)){
			        	console.log('g')
			        }
			        else{
			        var childTable = cur_frm.add_child("final_table");
					childTable.invoice_no=source_row.invoice_no
					childTable.project=source_row.project
					childTable.supplier=source_row.supplier
					childTable.age=source_row.age
					childTable.credit_amount=source_row.credit_amount
					childTable.outstanding_amount=source_row.outstanding_amount
					frm.refresh_fields("final_table");

			        	// ar.push({
			        	// 	"invoice_no":source_row.invoice_no,
			        	// 	"supplier":source_row.supplier,
			        	// 	"age":source_row.age,
			        	// 	"credit_amount":source_row.credit_amount,
			        	// 	"outstanding_amount":source_row.outstanding_amount
			        	// })
			        }
			    	}
			});
			//frm.set_value('final_table',ar)
			});
	},
	// set_proj:function(frm){
	// 	// alert(frm.doc.name)
	// 	frappe.call({
	// 		method:"wtt_module.wtt_module.doctype.payment_module.payment_module.set_project",
	// 		args:{
	// 			name:frm.doc.name
	// 		}
	// 	})
	// },
	landed_search:function(frm,cdt,cdn){
		if(frm.doc.landed_cost_no){
			frappe.call({
				method:"wtt_module.wtt_module.doctype.payment_module.payment_module.get_landed_cost_voucher",
				args:{
					number:frm.doc.landed_cost_no
				},
				callback(r){
					frm.set_value("landed_table",r.message);
					frm.refresh_field("landed_table");
				}
			})
		}
	},
	validate:function(frm){
		if(frm.doc.payment_type=='Invoice Payment'){
			frm.clear_table("consolidate_table")
			frm.refresh_field("consolidate_table");
			var array=[]
			$.each(frm.doc.final_table, function (index, source_row) {	
		    	array.push({
		    		"supplier":source_row.supplier,
		    		"credit_amount":source_row.credit_amount,
		    		"outstanding_amount":source_row.outstanding_amount
		    	})
			});
			frappe.call({
					method: 'wtt_module.wtt_module.doctype.payment_module.payment_module.ap_update_items',
					args: { gok:array},
					callback(r) {
						for(var i=0;i<r.message.length;i++)
						{
						var child = frm.add_child("consolidate_table");
						frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
						frappe.model.set_value(child.doctype, child.name, "credit_amount", r.message[i].credit_amount);
						frappe.model.set_value(child.doctype, child.name, "total", r.message[i].total);
						frm.refresh_field("consolidate_table");
						}
					}
					});			
		}
		else if(frm.doc.payment_type=='Advance Payment'){
			frm.clear_table("advance_consolidate_table")
			frm.refresh_field("advance_consolidate_table");
			var array=[]
			$.each(frm.doc.advance_table, function (index, source_row) {	
		    	array.push({
		    		"supplier":source_row.supplier,
		    		"amount":source_row.amount,
		    		"outstanding":source_row.outstanding,
		    		"final_amount":source_row.final_amount
		    	})
			});
			frappe.call({
				method: 'wtt_module.wtt_module.doctype.payment_module.payment_module.consolidate',
				args: { 
					gok:array
				},
				callback(r) {
					for(var i=0;i<r.message.length;i++)
					{	
					var child = frm.add_child("advance_consolidate_table");
					frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
					frappe.model.set_value(child.doctype, child.name, "total", r.message[i].amount);
					frappe.model.set_value(child.doctype, child.name, "advance_amount", r.message[i].final_amount);
					frm.refresh_field("advance_consolidate_table");
					}
				}
				});

		

		}

		else if(frm.doc.payment_type=='Freight Payment'){
			frm.clear_table("freight_consolidate_table")
			frm.refresh_field("freight_consolidate_table");
			var array=[]
			$.each(frm.doc.freight_table, function (index, source_row) {
		        	array.push({
		        		"supplier":source_row.supplier,
		        		"amount":source_row.amount,
		        		"transport":source_row.transport,
		        		"account_head":source_row.account_head,
		        		"final_amount":source_row.final_amount
		        	})
				});
			frappe.call({
				method: 'wtt_module.wtt_module.doctype.payment_module.payment_module.fa_update_items',
				args: { 
					gok:array
				},
				callback(r) {
					for(var i=0;i<r.message.length;i++)
					{
					var child = frm.add_child("freight_consolidate_table");
					frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].transport);
					frappe.model.set_value(child.doctype, child.name, "total", r.message[i].amount);
					frappe.model.set_value(child.doctype, child.name, "account_head", r.message[i].account_head);
					frappe.model.set_value(child.doctype, child.name, "advance_amount", r.message[i].final_amount);
					frm.refresh_field("freight_consolidate_table");
					}
				}
				});
		}
	
	},
	get_items: function(frm) {

		frm.clear_table("advance_table")
		frm.refresh_field("advance_table");
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.payment_module.payment_module.ap_update_status',
			args: { go:"success"},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("advance_table");
				frappe.model.set_value(child.doctype, child.name, "order_no", r.message[i].name);
				frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
				frappe.model.set_value(child.doctype, child.name, "age", r.message[i].age);
				frappe.model.set_value(child.doctype, child.name, "advance", r.message[i].advance);
				frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
				frm.refresh_field("advance_table");
				}
			}
		});
	},

	clear:function(frm){
		frm.clear_table("search_table")
		frm.refresh_field("search_table");
	},
	log_get_details:function(frm){
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.payment_module.payment_module.get_log_details',
			args: { log_name:frm.doc.logistics_module },
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
					frm.set_value("log_project",r.message[i].project)
					frm.set_value("log_project_name",r.message[i].project_name)
					frm.set_value("log_type",r.message[i].type)
					frm.set_value("log_supplier",r.message[i].supplier)
					frm.set_value("log_from_warehouse",r.message[i].from_warehouse)
					frm.set_value("log_to_warehouse",r.message[i].to_warehouse)
					frm.set_value("log_reference_doctype",r.message[i].reference_doctype)
					frm.set_value("log_reference_name",r.message[i].reference_name)
					frm.set_value("log_terms_and_conditions",r.message[i].terms)
					frm.set_value("log_rounded_total",r.message[i].rounded_total)
					frm.set_value("log_bank_account",r.message[i].log_bank_account)
					frm.set_value("log_bank",r.message[i].log_bank)
					frm.set_value("log_bank_account_no",r.message[i].log_bank_account_no)
					frm.set_value("log_account",r.message[i].log_account)
					frm.set_value("log_branch",r.message[i].log_branch)
					frm.set_value("log_iban",r.message[i].log_iban)
					frm.set_value("log_branch_code",r.message[i].log_branch_code)
					frm.set_value("log_ifsc_code",r.message[i].log_ifsc_code)
				}
			}
		});
	},
	search: function(frm) {
		if(frm.doc.supplier==undefined && frm.doc.po==undefined){
			frappe.throw("Please Choose the PO NO")
		// frappe.call({
		// 	method: 'wtt_module.wtt_module.doctype.payment_module.payment_module.search_all',
		// 	args: { go:"done"},
		// 	callback(r) {
		// 		for(var i=0;i<r.message.length;i++)
		// 		{
		// 		var child = frm.add_child("search_table");
		// 		frappe.model.set_value(child.doctype, child.name, "order_no", r.message[i].name);
		// 		frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
		// 		frappe.model.set_value(child.doctype, child.name, "age", r.message[i].age);
		// 		frappe.model.set_value(child.doctype, child.name, "advance", r.message[i].advance);
		// 		frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
		// 		frappe.model.set_value(child.doctype, child.name, "total_amount", r.message[i].total);
		// 		frappe.model.set_value(child.doctype, child.name, "currency", r.message[i].currency);
		// 		frappe.model.set_value(child.doctype, child.name, "paid_advance", r.message[i].total_advance);
		// 		frm.refresh_field("search_table");
		// 		}
		// 	}
		// });
		}
		else if(frm.doc.po==undefined){
			frappe.throw("Please Choose the PO NO")
		// frappe.call({
		// 	method: 'wtt_module.wtt_module.doctype.payment_module.payment_module.search_po1',
		// 	args: { go:frm.doc.supplier},
		// 	callback(r) {
		// 		for(var i=0;i<r.message.length;i++)
		// 		{
		// 		var child = frm.add_child("search_table");
		// 		frappe.model.set_value(child.doctype, child.name, "order_no", r.message[i].name);
		// 		frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
		// 		frappe.model.set_value(child.doctype, child.name, "age", r.message[i].age);
		// 		frappe.model.set_value(child.doctype, child.name, "advance", r.message[i].advance);
		// 		frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
		// 		frappe.model.set_value(child.doctype, child.name, "paid_advance", r.message[i].total_advance);
		// 		frappe.model.set_value(child.doctype, child.name, "total_amount", r.message[i].total);
		// 		frappe.model.set_value(child.doctype, child.name, "currency", r.message[i].currency);
		// 		frm.refresh_field("search_table");
		// 		}
		// 	}
		// });
		}

		else if(frm.doc.supplier==undefined){
			var gug=[]
			if(frm.doc.search_table)
			{
			$.each(frm.doc.search_table, function (i,d) {
				gug.push(d.order_no)
			});
			}
			if(gug.includes(frm.doc.po))
			{
				console.log('g')
			}
			else
			{
			frappe.call({
			method: 'wtt_module.wtt_module.doctype.payment_module.payment_module.search_po2',
			args: { go:frm.doc.po},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("search_table");
				frappe.model.set_value(child.doctype, child.name, "order_no", r.message[i].name);
				frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
				frappe.model.set_value(child.doctype, child.name, "age", r.message[i].age);
				frappe.model.set_value(child.doctype, child.name, "advance", r.message[i].advance);
				frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
				frappe.model.set_value(child.doctype, child.name, "paid_advance", r.message[i].total_advance);
				frappe.model.set_value(child.doctype, child.name, "total_amount", r.message[i].total);
				frappe.model.set_value(child.doctype, child.name, "currency", r.message[i].currency);
				frm.refresh_field("search_table");
				}
			}
		});
		}	
		}
		else if(frm.doc.supplier!=undefined && frm.doc.po!=undefined){
		// frappe.call({
		// 	method: 'wtt_module.wtt_module.doctype.payment_module.payment_module.search_po',
		// 	args: { go:frm.doc.supplier,run:frm.doc.po},
		// 	callback(r) {
		// 		for(var i=0;i<r.message.length;i++)
		// 		{
		// 		var child = frm.add_child("search_table");
		// 		frappe.model.set_value(child.doctype, child.name, "order_no", r.message[i].name);
		// 		frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
		// 		frappe.model.set_value(child.doctype, child.name, "age", r.message[i].age);
		// 		frappe.model.set_value(child.doctype, child.name, "advance", r.message[i].advance);
		// 		frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
		// 		frappe.model.set_value(child.doctype, child.name, "paid_advance", r.message[i].total_advance);
		// 		frm.refresh_field("search_table");
		// 		}
		// 	}
		// });
		}
	},

	get_po:function(frm){
		var gug=[]
		if(frm.doc.freight_table)
		{
		$.each(frm.doc.freight_table, function (i,d) {
			gug.push(d.order_no)
		});
		}
		if(gug.includes(frm.doc.order_no))
		{
			console.log('g')
		}
		else
		{
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.payment_module.payment_module.fp_update_status',
			args: { go:frm.doc.order_no},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("freight_table");
				frappe.model.set_value(child.doctype, child.name, "order_no", r.message[i].name);
				frappe.model.set_value(child.doctype, child.name, "project", r.message[i].project);
				frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
				frappe.model.set_value(child.doctype, child.name, "amount", r.message[i].amount);
				frm.refresh_field("freight_table");
				}
			}
		});
		}
	},

	status:function(frm) {
		// alert("ff")
		frm.clear_table("overdue_table")
		frm.refresh_field("overdue_table");
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.payment_module.payment_module.pc_update_status',
			args: { 
				go:frm.doc.status,
				comp:frm.doc.company
			},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("overdue_table");
				frappe.model.set_value(child.doctype, child.name, "invoice_no", r.message[i].name);
				frappe.model.set_value(child.doctype, child.name, "project", r.message[i].project);
				frappe.model.set_value(child.doctype, child.name, "supplier", r.message[i].supplier);
				frappe.model.set_value(child.doctype, child.name, "status", r.message[i].status);
				frappe.model.set_value(child.doctype, child.name, "age", r.message[i].age);
				frappe.model.set_value(child.doctype, child.name, "credit_amount", r.message[i].credit_amount);
				frappe.model.set_value(child.doctype, child.name, "outstanding_amount", r.message[i].outstanding_amount);
				frm.refresh_field("overdue_table");
				}
			}
		});
	},
	reference_name:function(frm){
		if(frm.doc.reference_doctype=='Landed Cost Voucher'){
			frappe.call({
			method: 'wtt_module.wtt_module.doctype.payment_module.payment_module.lcv_amount',
			args: { go:frm.doc.reference_name},
			callback(r) {
				frm.set_value("party_type",'Supplier');
				for(var i=0;i<r.message.length;i++)
				{
				frm.set_value("grand_total",r.message[0]);
				frm.set_value("party",r.message[1]);
				}
			}
		});
		}
	},
	party:function(frm){
		if(frm.doc.party_type=="Employee" || frm.doc.party_type=="Farm Employee"){
			frappe.db.get_value(frm.doc.party_type, frm.doc.party, 'employee_name')
		    .then(r => {
		        frm.set_value("employee_name",r.message.employee_name);
		        frm.refresh_field("employee_name");
		    })

		    frappe.db.get_value(frm.doc.party_type, frm.doc.party, 'bank_ac_no')
		    .then(r => {
		        frm.set_value("employee_bank_account_no",r.message.bank_ac_no);
		        frm.refresh_field("employee_bank_account_no");
		    })

		    frappe.db.get_value(frm.doc.party_type, frm.doc.party, 'bank_name')
		    .then(r => {
		        frm.set_value("employee_bank_name",r.message.bank_name);
		        frm.refresh_field("employee_bank_name");
		    })

		    frappe.db.get_value(frm.doc.party_type, frm.doc.party, 'ifsc_code')
		    .then(r => {
		        frm.set_value("employee_bank_ifsc",r.message.ifsc_code);
		        frm.refresh_field("employee_bank_ifsc");
		    })
		}
	}
});


frappe.ui.form.on('Advance Table', {
	percentage:function(frm,cdt,cdn){
		calculate_priority1(frm, cdt, cdn);
	},


});
var calculate_priority1 = function(frm, cdt, cdn) {
	
	var child = locals[cdt][cdn];
	if(child.percentage>100){
	frappe.model.set_value(cdt, cdn, "percentage",100)
	}
	frappe.model.set_value(cdt, cdn, "final_amount",((child.percentage/100)*child.amount));
	frappe.model.set_value(cdt, cdn, "final_amount_in_po",((child.percentage/100)*child.amount_in_po));
};

frappe.ui.form.on('Advance Consolidate Table',{
	
	before_advance_consolidate_table_remove:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		var tbl = frm.doc.advance_table || [];
		var i = tbl.length;
		while (i--)
		{
		    if(tbl[i].supplier == d.supplier)
		    {
		        frm.get_field("advance_table").grid.grid_rows[i].remove();
		    }
		}
		frm.refresh();
	}
});
frappe.ui.form.on('Freight Consolidate Table',{
	before_freight_consolidate_table_remove:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		var tbl = frm.doc.freight_table || [];
		var i = tbl.length;
		while (i--)
		{
		    if(tbl[i].transport == d.supplier)
		    {
		        frm.get_field("freight_table").grid.grid_rows[i].remove();
		    }
		}
		frm.refresh();
	}
});
frappe.ui.form.on('Consolidate Table',{
	
	before_consolidate_table_remove:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		var tbl = frm.doc.final_table || [];
		var i = tbl.length;
		while (i--)
		{
		    if(tbl[i].supplier == d.supplier)
		    {
		        frm.get_field("final_table").grid.grid_rows[i].remove();
		    }
		}
		frm.refresh();
	}

});
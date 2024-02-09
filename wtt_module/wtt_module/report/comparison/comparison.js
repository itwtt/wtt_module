frappe.query_reports["Comparison"] = {
	"filters": [
		{
			fieldtype: "Link",
			label: __("Request for Quotation"),
			options: "Request for Quotation",
			fieldname: "request_for_quotation",
			"default":"RFQ-23-00007",
			"reqd": 1,
			get_query: () => {
				return { filters: { "docstatus": ["<", 2] } }
			}
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -2),
			"hidden":1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"hidden":1,
			"default": frappe.datetime.get_today()
		},
		{
			fieldtype: "Link",
			label: __("Company"),
			options: "Company",
			fieldname: "company",
			default: "WTT INTERNATIONAL PVT LTD"
		}
	],
	formatter: (value, row, column, data, default_formatter,datum) => {
		// column.editable = true;
		var ars=[]
		value = default_formatter(value, row, column, data);
			if(data['description']=='Basic Total')
			{
				value = `<div style="font-weight:bold">${value}</div>`;	
			}
			if(data['description']=='SQ No')
			{
				value = `<div style="font-weight:bold">${value}</div>`;	
			}
			if(data['description']=='Grand Total')
			{
						// if(typeof(value)=='number')
						// {
						// 	alert(value)
						// }
				// if(typeof(value)=='number')
				// {
				value = `<div style="font-weight:bold">${value}</div>`;
				// if(value>500000)
				// {
				// value = `<div style="font-weight:bold;color:red">${value}</div>`;	
				// }
				// else if(value<500000)
				// {
				// 	value = `<div style="font-weight:bold;color:green">${value}</div>`;	
				// }
				// }
				//value = `<div style="font-weight:bold;color:red">${value}</div>`;	
			}
		return value;
		},
		onload: function(report) {
		frappe.query_report.page.add_inner_button(__("Get Details"), function() {
			var selected_rows = [];
			var opy=[];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			var rfq = frappe.query_report.get_filter_value('request_for_quotation')
			for(var i in v)
			{
			if(frappe.query_report.data[parseInt(v[i])].item_code!=undefined)
		 	{
		 		opy.push(frappe.query_report.data[parseInt(v[i])].item_code)
		 		frappe.call({
				"method":"wtt_module.wtt_module.report.comparison.comparison.fun",
				args:{
					"rfq1":rfq,
					"item_code":frappe.query_report.data[parseInt(v[i])].item_code
				},
				callback: function(r) {
				var d = new frappe.ui.Dialog({
				'fields': [
				{'fieldtype': 'Link','label': 'Item Code', 'fieldname': 'item_code','options':'Item','default':frappe.query_report.data[parseInt(v[i])].item_code},
				{"fieldtype": "Select", "label":"Supplier Quotation", "fieldname": "sq",'options':''},
				{"fieldtype": "Data", "label":"Supplier", "fieldname": "supplier",'default':''},
				{"fieldtype": "Section Break", "label":"", "fieldname": "sec_br"},
				{"fieldtype": "Heading", "label":"Supplier Data", "fieldname": "supplier_data"},
				{"fieldtype": "Float", "label":"Qty", "fieldname": "sup_qty",'default':0,'read_only':1},
				{"fieldtype": "Float", "label":"Rate", "fieldname": "sup_rate",'default':0,'read_only':1},
				{"fieldtype": "Float", "label":"Amount", "fieldname": "sup_amount",'default':0,'read_only':1},
				{"fieldtype": "Data", "label":"MR Reference", "fieldname": "sup_mr_name",'default':'','read_only':1,'hidden':1},
				{"fieldtype": "Data", "label":"Price basis", "fieldname": "price_basis"},
				{"fieldtype": "Data", "label":"Payment Terms", "fieldname": "payment_terms"},
				{"fieldtype": "Data", "label":"Warranty", "fieldname": "warranty"},
				{"fieldtype": "Data", "label":"Delivery Time", "fieldname": "delivery_time"},

				{"fieldtype": "Column Break", "label":"", "fieldname": "col_br"},
				{"fieldtype": "Heading", "label":"Quotation", "fieldname": "supplier_data"},
				{"fieldtype": "Data", "label":"Currency", "fieldname": "currency","default":""},
				{"fieldtype": "Data", "label":"Exchange Rate", "fieldname": "cr","default":1},
				{"fieldtype": "Float", "label":"Qty", "fieldname": "qty",'default':0},
				{"fieldtype": "Float", "label":"Rate", "fieldname": "rate",'default':0},
				{"fieldtype": "Float", "label":"Amount", "fieldname": "amount",'default':0},				
				{"fieldtype": "Float", "label":"Rate Inr","fieldname":"rate_inr",'default':0,'read_only':1},
				{"fieldtype": "Float", "label":"Amount Inr","fieldname":"amount_inr",'default':0,'read_only':1},
				{"fieldtype": "Data", "label":"MR Reference", "fieldname": "mr_name",'default':'','hidden':1}
				],
				primary_action: function(values){
					frappe.call({
					"method":"wtt_module.wtt_module.report.comparison.comparison.update_supplier_quotation",
					args:{
						"item_code":values.item_code,
						"sq":values.sq,
						"mr":"values.mr",
						"supplier":values.supplier,
						"qty":values.qty,
						"rate":values.rate,
						"amt":values.amount,
						"mr_name":values.mr_name,
						"currency":values.currency,
						"base_rate":values.rate_inr,
						"base_amount":values.amount_inr,
						"price_basis":values.price_basis,
						"warranty":values.warranty,
						"delivery_time":values.delivery_time,
						"payment_terms":values.payment_terms
					},
					callback: function(r) {
						msgprint('Updated')
						report.refresh();
					}
				});
				//alert($("input[data-fieldname='qty']").val())
				}
				});
				d.set_df_property('sq','options',r.message);
				d.show();
				d.fields_dict.sq.refresh(); // enforce that the field have a input
				d.fields_dict.sq.$input.on("change", function(event){
    			var sqi = this.value;
				var itc = frappe.query_report.data[parseInt(v[i])].item_code
				frappe.call({
				"method":"wtt_module.wtt_module.report.comparison.comparison.fun_make2",
				args:{
					"sq":sqi,
					"itc":itc
				},
				callback: function(r) {
					d.set_value('supplier',r.message[0].supplier)
					d.set_value('qty',r.message[0].qty)
					d.set_value('rate',r.message[0].rate)
					d.set_value('amount',r.message[0].amount)
					d.set_value('mr_name',r.message[0].mr_name)
					d.set_value('sup_qty',r.message[0].sup_qty)
					d.set_value('sup_rate',r.message[0].sup_rate)
					d.set_value('sup_amount',r.message[0].sup_amount)
					d.set_value('sup_mr_name',r.message[0].sup_mr_name)
					d.set_value('currency',r.message[0].currency)
					d.set_value('cr',r.message[0].cr)
					d.set_value('rate_inr',r.message[0].rate*r.message[0].cr)
					d.set_value('amount_inr',r.message[0].amount*r.message[0].cr)
					d.set_value('warranty',r.message[0].warranty)
					d.set_value('price_basis',r.message[0].price_basis)
					d.set_value('delivery_time',r.message[0].delivery_time)
					d.set_value('payment_terms',r.message[0].payment_terms)

					d.fields_dict.qty.input.onchange = function() {
						var rate=$("input[data-fieldname='rate']").val()
						var number = Number(rate.replace(/[^0-9.-]+/g,""));
						var amt=parseFloat($("input[data-fieldname='qty']").val())*number
						d.set_value('amount',amt)
						d.set_value('amount_inr',amt*r.message[0].cr)
					}
					d.fields_dict.rate.input.onchange = function() {
						var rate=$("input[data-fieldname='rate']").val()
						var number = Number(rate.replace(/[^0-9.-]+/g,""));
						var amt=parseFloat($("input[data-fieldname='qty']").val())*number
						d.set_value('amount',amt)
						d.set_value('rate_inr',number*r.message[0].cr)
						d.set_value('amount_inr',amt*r.message[0].cr)
					}
					d.fields_dict.rate_inr.input.onchange = function() {
						var rate=$("input[data-fieldname='rate_inr']").val()
						var number = Number(rate.replace(/[^0-9.-]+/g,""));
						var amt=parseFloat($("input[data-fieldname='qty']").val())*number
						d.set_value('amount_inr',amt)
						d.set_value('rate',number/r.message[0].cr)
						d.set_value('amount',amt/r.message[0].cr)
					}
				}
				});
				});
				}
			});
			}
			}		
		});
		frappe.query_report.page.add_inner_button(__("Approve"), function() {
			var selected_rows = [];
			
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			var rfq = frappe.query_report.get_filter_value('request_for_quotation')
			var opy = [];
			for(i in v)
			{
			if(frappe.query_report.data[parseInt(v[i])].item_code!=undefined)
		 	{
		 		opy.push({"it":frappe.query_report.data[parseInt(v[i])].item_code})
		 	}
		 	}
			// alert(JSON.stringify(opy))

			if(frappe.query_report.data[v[0]].item_code!=undefined)
		 	{
		 		
		 		frappe.call({
				"method":"wtt_module.wtt_module.report.comparison.comparison.fun",
				args:{
					"rfq1":rfq,
					"item_code":frappe.query_report.data[parseInt(v[0])].item_code
				},
				callback: function(r) {
				var d = new frappe.ui.Dialog({
				'fields': [					
				{"fieldtype": "Select", "label":"Supplier Quotation", "fieldname": "sq",'options':''},
				{"fieldtype": "Data", "label":"Supplier", "fieldname": "supplier",'default':''},
				],
				primary_action: function(values){
					frappe.call({
					"method":"wtt_module.wtt_module.report.comparison.comparison.approvesq",
					args:{
						"sq":values.sq,
						"supplier":values.supplier,
						"user":frappe.session.user,
						"item":opy
						
					},
					callback: function(r) {
						report.refresh();
					if(frappe.session.user=='venkat@wttindia.com' || frappe.session.user=='Administrator' || frappe.session.user=='sarnita@wttindia.com'){
						frappe.call({
						"method":"wtt_module.wtt_module.report.comparison.comparison.fun12",
						args:{
							"source_name":values.sq
						},
						callback: function(r) {
							report.refresh();
							msgprint("Approved")
							
						}
					});
				}



				}
				});
				
				}
				});
				d.set_df_property('sq','options',r.message);
				d.show();
				d.fields_dict.sq.refresh();
				d.fields_dict.sq.$input.on("change", function(event){
    			var sqi = this.value;
				var itc = frappe.query_report.data[parseInt(v[0])].item_code
				frappe.call({
				"method":"wtt_module.wtt_module.report.comparison.comparison.fun_make",
				args:{
					"sq":sqi,
					"itc":itc
				},
				callback: function(r) {
					d.set_value('supplier',r.message[0].supplier)
					
				}
				});
				});
				}
			});
			}
					
		});
		// frappe.query_report.page.add_inner_button(__("Overall Quotation Reject"), function() {
		// 	var selected_rows = [];
			
		// 	var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
		// 	var rfq = frappe.query_report.get_filter_value('request_for_quotation')
			
		// 	if(frappe.query_report.data[v[2]].item_code!=undefined)
		//  	{
		 		
		//  		frappe.call({
		// 		"method":"wtt_module.wtt_module.report.comparison.comparison.fun",
		// 		args:{
		// 			"rfq1":rfq,
		// 			"item_code":frappe.query_report.data[parseInt(v[2])].item_code
		// 		},
		// 		callback: function(r) {
		// 		var d = new frappe.ui.Dialog({
		// 		'fields': [	
				
		// 		{"fieldtype": "Select", "label":"Supplier Quotation", "fieldname": "sq",'options':''},
		// 		{"fieldtype": "Data", "label":"Supplier", "fieldname": "supplier",'default':''},
		// 		],
		// 		primary_action: function(values){
		// 			frappe.call({
		// 		"method":"wtt_module.wtt_module.report.comparison.comparison.rejectsq",
		// 		args:{
		// 			"sq":values.sq,
		// 			"supplier":values.supplier,
		// 			"user":frappe.session.user
					
		// 		},
		// 		callback: function(r) {
		// 			report.refresh();
		// 			msgprint('Rejected')
		// 		}
		// 		});

		// 		}
		// 		});
		// 		d.set_df_property('sq','options',r.message);
		// 		d.show();
		// 		d.fields_dict.sq.refresh(); // enforce that the field have a input
		// 		d.fields_dict.sq.$input.on("change", function(event){
  //   			var sqi = this.value;
		// 		var itc = frappe.query_report.data[parseInt(v[2])].item_code
		// 		frappe.call({
		// 		"method":"wtt_module.wtt_module.report.comparison.comparison.fun_make",
		// 		args:{
		// 			"sq":sqi,
		// 			"itc":itc
		// 		},
		// 		callback: function(r) {
		// 			d.set_value('supplier',r.message[0].supplier)
					
		// 		}
		// 		});
		// 		});
		// 		}
		// 	});
		// 	}
					
		// });
		// frappe.query_report.page.add_inner_button(__("Individual Item Approve"), function() {
		// 	var selected_rows = [];
		// 	var opy=[]
		// 	var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
		// 	var rfq = frappe.query_report.get_filter_value('request_for_quotation')
		// 	for(i in v)
		// 	{
		// 	if(frappe.query_report.data[parseInt(v[i])].item_code!=undefined)
		//  	{
		//  		opy.push({"it":frappe.query_report.data[parseInt(v[i])].item_code})
		//  	}
		//  	}
		// 	// if(frappe.query_report.data[v[2]].item_code!=undefined)
		//  	// {
		 		
		//  		frappe.call({
		// 			"method":"wtt_module.wtt_module.report.comparison.comparison.fun",
		// 			args:{
		// 				"rfq1":rfq,
		// 				"item_code":frappe.query_report.data[parseInt(v[0])].item_code
		// 			},
		// 			callback: function(r) {
		// 				var d = new frappe.ui.Dialog({
		// 				'fields': [		
		// 					// {'fieldtype': 'Select','label': 'Item Code', 'fieldname': 'item_code','options':''},					
		// 					{"fieldtype": "Select", "label":"Supplier Quotation", "fieldname": "sq",'options':''},
		// 					{"fieldtype": "Data", "label":"Supplier", "fieldname": "supplier",'default':''},
		// 				],
		// 				primary_action: function(values){
		// 					frappe.call({
		// 						"method":"wtt_module.wtt_module.report.comparison.comparison.approveitc",
		// 						args:{
		// 							"sq":values.sq,
		// 							"supplier":values.supplier,
		// 							"item_code":"item_code",
		// 							"item":opy,
		// 							"user":frappe.session.user								
		// 						}
		// 					});
		// 					report.refresh();
		// 					msgprint('Approved')
		// 					}
		// 				});
		// 				d.set_df_property('sq','options',r.message);
		// 				// d.set_df_property('item_code','options',opy);
		// 				d.show();
		// 				d.fields_dict.sq.refresh(); // enforce that the field have a input
		// 				d.fields_dict.sq.$input.on("change", function(event){
		// 	    			var sqi = this.value;
		// 					var itc = frappe.query_report.data[parseInt(v[0])].item_code
		// 					frappe.call({
		// 						"method":"wtt_module.wtt_module.report.comparison.comparison.fun_make",
		// 						args:{
		// 							"sq":sqi,
		// 							"itc":itc
		// 						},
		// 						callback: function(r) {
		// 							d.set_value('supplier',r.message[0].supplier)
									
		// 						}
		// 					});
		// 				});
		// 			}
		// 		});
		// 	// }		
		// });
		frappe.query_report.page.add_inner_button(__("Reject"), function() {
			var selected_rows = [];
			var opy=[]
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			var rfq = frappe.query_report.get_filter_value('request_for_quotation')
			for(i in v)
			{
			if(frappe.query_report.data[parseInt(v[i])].item_code!=undefined)
		 	{
		 		opy.push({"it":frappe.query_report.data[parseInt(v[i])].item_code})
		 	}
		 	}
			if(frappe.query_report.data[v[2]].item_code!=undefined)
		 	{
		 		
		 		frappe.call({
					"method":"wtt_module.wtt_module.report.comparison.comparison.fun",
					args:{
						"rfq1":rfq,
						"item_code":frappe.query_report.data[parseInt(v[2])].item_code
					},
					callback: function(r) {
						var d = new frappe.ui.Dialog({
						'fields': [		
							// {'fieldtype': 'Select','label': 'Item Code', 'fieldname': 'item_code','options':''},					
							{"fieldtype": "Select", "label":"Supplier Quotation", "fieldname": "sq",'options':''},
							{"fieldtype": "Data", "label":"Supplier", "fieldname": "supplier",'default':''},
						],
						primary_action: function(values){
							frappe.call({
								"method":"wtt_module.wtt_module.report.comparison.comparison.rejectitc",
								args:{
									"sq":values.sq,
									"supplier":values.supplier,
									"item_code":"item_code",
									"item":opy,
									"user":frappe.session.user								
								}
							});
							report.refresh();
							msgprint('Rejected')
							}
						});
						d.set_df_property('sq','options',r.message);
						// d.set_df_property('item_code','options',opy);
						d.show();
						d.fields_dict.sq.refresh(); // enforce that the field have a input
						d.fields_dict.sq.$input.on("change", function(event){
			    			var sqi = this.value;
							var itc = frappe.query_report.data[parseInt(v[2])].item_code
							frappe.call({
								"method":"wtt_module.wtt_module.report.comparison.comparison.fun_make",
								args:{
									"sq":sqi,
									"itc":itc
								},
								callback: function(r) {
									d.set_value('supplier',r.message[0].supplier)
									
								}
							});
						});
					}
				});
			}		
		});
	},
	get_datatable_options(options) {
    return Object.assign(options, {
        checkboxColumn: true
    });
	}
	}

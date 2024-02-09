// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.buying");
frappe.provide("erpnext.accounts.dimensions");
{% include 'erpnext/public/js/controllers/buying.js' %};

frappe.ui.form.on('Purchase Order', {
	setup:function(frm,cdt,cdn){
		frm.get_docfield("combined_items").allow_bulk_edit = 1;
		if(frm.doc.docstatus==1){
			frm.set_df_property('combine_button', 'hidden', 1);
		}

	},
	validate:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		var ar=[];
		if(frm.doc.naming_series=="PO-.YY.-" && !(frm.doc.name).includes("JOB")){
			$.each(frm.doc.items || [], function(i, v) {
				if(v.material_request==undefined || v.material_request_item==undefined){frappe.throw("Please link MR to Order")}
				if(ar.includes(v.material_request_item)){
					frappe.throw("#Row "+(v.idx)+" has already exists")
				}
				else{
					ar.push(v.material_request_item)
				}
			});	
		}

	},
	update_date:function(frm){
		var f_date = frm.doc.delivery_from
		var to_date = frm.doc.delivery_to
		$.each(frm.doc.items || [], function(i, v) {
			v.delivery_from = f_date
			v.delivery_to = to_date
		});
		frm.save();
	},
	before_save:function(frm){
		// alert(frm.doc.workflow_state)
		var qty_check=[];
		var rate_check=[];
		var ws=[];
		$.each(frm.doc.po_status || [], function(i, v) {
			qty_check.push(v.qty_check);
			rate_check.push(v.rate_check);
			ws.push(v.workflow_state);
		})
		if(!ws.includes(frm.doc.workflow_state)){	
			frappe.throw("Need to verify qty and rate")
		}
		else if(!qty_check.includes(1) && !rate_check.includes(1)){		
			frappe.throw("Need to verify qty and rate")
		}		
	},
	combine_button:function(frm,cdt,cdn){
		var arr=[];
		$.each(frm.doc.items || [], function(i, v) {
			if(v.supplier_description==undefined){v.supplier_description=''}
			if (v.technical_description==undefined){
			arr.push({"idx":v.idx,"item_code":v.item_code,"item_name":v.item_name,"description":v.description,"technical_description":"","supplier_description":v.supplier_description,"qty":v.qty,"rate":v.rate,"amount":v.amount,"uom":v.uom,"stock_uom":v.stock_uom,"stock_qty":v.stock_qty})
			}
			else{
			arr.push({"idx":v.idx,"item_code":v.item_code,"item_name":v.item_name,"description":v.description,"technical_description":v.technical_description,"supplier_description":v.supplier_description,"qty":v.qty,"rate":v.rate,"amount":v.amount,"uom":v.uom,"stock_uom":v.stock_uom,"stock_qty":v.stock_qty})
			}	

		});
		
			frm.set_value("combined_items","")
			frappe.call({
			"method":"wtt_module.customization.custom.purchase_order.combine_items",
			args:{
				'arr':arr
			},
			callback(r) {
				
				for(var i=0;i<r.message.length;i++)
					{	
					var child = frm.add_child("combined_items");
					frappe.model.set_value(child.doctype, child.name, "item_code", r.message[i].item_code);
					frappe.model.set_value(child.doctype, child.name, "item_name", r.message[i].item_name);
					frappe.model.set_value(child.doctype, child.name, "description", r.message[i].description);
					frappe.model.set_value(child.doctype, child.name, "technical_description", r.message[i].technical_description);
					frappe.model.set_value(child.doctype, child.name, "supplier_description", r.message[i].supplier_description);
					frappe.model.set_value(child.doctype, child.name, "qty", r.message[i].qty);
					frappe.model.set_value(child.doctype, child.name, "uom1", r.message[i].uom);
					frappe.model.set_value(child.doctype, child.name, "stock_qty1", r.message[i].stock_qty);
					frappe.model.set_value(child.doctype, child.name, "stock_uom", r.message[i].stock_uom);
					frappe.model.set_value(child.doctype, child.name, "rate1", r.message[i].rate);
					frappe.model.set_value(child.doctype, child.name, "amount1", r.message[i].amount);
					frm.refresh_field("combined_items");
					}
				

				
			}
		});
	},
		get_compare:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		var arr=[]
		$.each(frm.doc.items || [], function(i, v) {
			if(v.model_no==undefined)
			{
			if (v.technical_description==undefined){
			arr.push({"model_no":"","nn":v.name,"item":v.item_code,"description":v.description,"technical_description":"","qty":v.qty})
			}
			else{
			arr.push({"model_no":"","nn":v.name,"item":v.item_code,"description":v.description,"technical_description":v.technical_description,"qty":v.qty})
			}
			}
			else
			{
			if (v.technical_description==undefined){
			arr.push({"model_no":v.model_no,"nn":v.name,"item":v.item_code,"description":v.description,"technical_description":"","qty":v.qty})
			}
			else{
			arr.push({"model_no":v.model_no,"nn":v.name,"item":v.item_code,"description":v.description,"technical_description":v.technical_description,"qty":v.qty})
			}
			}	
		});

		frappe.call({
			"method":"wtt_module.customization.custom.purchase_order.get_last_rate",
			args:{
				'arr':arr
			},
			callback: function(r) {
				for(var i=0;i<r.message.length;i++){
					var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
					htvalue+="<br><table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%'>S.NO</th><th style='width:4%'>DESCRIPTION</th><th style='width:12%'>TECHNICAL DESCRIPTION</th><th style='width:5%'>QUANTITY</th><th style='width:8%'>CURRENT RATE</th><th style='width:12%'>RATE 1</th><th style='width:12%'>RATE 2</th><th style='width:12%'>RATE 3</th></tr>"
					$.each(r.message, function(i, v) {
					var result=""
					var c=i+1
					var r1="-"
					var r2="-"
					var r3="-"
					if(v.rate3!=null)
					{
						r3=v.rate3
					}
					if(v.rate2!=null)
					{
						r2=v.rate2
					}
					if(v.rate1!=null)
					{
						r1=v.rate1
					}
					if(v.technical_description!="")
					{
					var gug=[]
					var vis=v.technical_description.split(",")
					var vg='<br>'
					for(var g in vis)
					{
					gug.push(vis[g])
					gug.push(vg)
					}
					result = gug.toString().replace(/,/g, "");
					}
					htvalue+='<tr style="text-align:center;"><td align="center">'+c+'<br></td><td align="center">'+v.description+'<br></td><td align="left">'+result+'<br></td><td align="center">'+v.qty+'</td><td align="center">-</td><td align="center">'+r1+'</td><td>'+r2+'</td><td>'+r3+'</td</tr>'
					});
					htvalue+='</table><br><br>'
					// if(frappe.session.user=='Administrator' || frappe.session.user=='venkat@wttindia.com'|| frappe.session.user=='poa@wttindia.com'|| frappe.session.user=='malayalaraj@wtt.com'){
					$(frm.fields_dict['linked_pr'].wrapper).html("");
					$(frm.fields_dict['linked_mr'].wrapper).html("");
					$(frm.fields_dict['rate_html'].wrapper).html(htvalue);
					}
				

			}

		});
		
	},
	download_table:function(frm,cdt,cdn){
		frappe.call({
			"method":"download_table",
			doc:frm.doc,
			callback: function(r) {	
				for(var i=0;i<r.message.length;i++){
				var file_url=JSON.stringify(r.message[0].url)
				file_url = file_url.replace(/#/g, '%23');
				file_url = file_url.replace(/"/g, '');
				window.open(file_url);
				}
			}
		});
	},


	hide_table: function(frm,cdt,cdn){
		frm.set_df_property('hide_table', 'hidden', 1);
		frm.set_df_property('preview', 'hidden', 0);
		$(frm.fields_dict['item_table'].wrapper).html("");
		$(frm.fields_dict['linked_mr'].wrapper).html("");
	},
	preview:function(frm,cdt,cdn){
		frm.set_df_property('download1', 'hidden', 1);
		frm.set_df_property('download', 'hidden', 1);
		frm.set_df_property('hide_table', 'hidden', 0);
		frm.set_df_property('preview', 'hidden', 1);
		var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
		if(frm.doc.is_subcontracted==0){
			htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>S.NO</th><th style='width:2%'>DESCRIPTION</th><th style='width:15%'>TECHNICAL DESCRIPTION</th><th style='width:10%'>SUPPLIER DESCRIPTION</th><th style='text-align:center;width:5%'>QTY</th><th style='text-align:center;width:5%'>RATE</th><th style='text-align:center;width:5%'>AMOUNT</th><th style='width:8%'>REMARKS</th><th style='width:8%'>MR NO</th><th style='width:8%'>TAB REF</th></tr>"
		}
		else if(frm.doc.is_subcontracted==1){
			htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>S.NO</th><th style='width:2%'>FG DESCRIPTION</th><th style='width:15%'>FG TECHNICAL DESCRIPTION</th><th style='width:10%'>SUPPLIER DESCRIPTION</th><th style='text-align:center;width:5%'>QTY</th><th style='text-align:center;width:5%'>MACHINING COST (PER QTY)</th><th style='text-align:center;width:5%'>AMOUNT</th><th style='width:8%'>REMARKS</th></tr>"	
		}
		$.each(frm.doc.items || [], function(i, v) {
			var result=''
			var re=''
			var su=''
			if(v.technical_description)
			{
			var go=[]
			var val=v.technical_description.split(",")
			var des=v.description
			// if(frm.doc.is_subcontracted==1){
			// 	val=v.fg_technical_description.split(",")
			// 	des=v.fg_description
			// }

			var gg='<br>'
			for(var g in val)
			{
				go.push(val[g])
				go.push(gg)
			}
			result = go.toString().replace(/,/g, "");
			}
			if(v.remarks)
			{
				re=v.remarks
			}
			if(v.supplier_description)
			{
				su=v.supplier_description
			}
			if(frm.doc.is_subcontracted==0){
				htvalue+='<tr style="text-align:center;"><td align="center">'+v.idx+'.</td><td align="center">'+v.description+'<br></td><td align="left">'+result+'</td><td>'+su+'</td><td>'+v.qty+'</td><td>'+v.rate+'</td><td>'+v.amount+'</td><td>'+re+'</td><td>'+v.material_request+'</td><td>'+v.name+'</td></tr>'
			}
			else if(frm.doc.is_subcontracted==1){
				htvalue+='<tr style="text-align:center;"><td align="center">'+v.idx+'.</td><td align="center">'+v.fg_description+'<br></td><td align="left">'+v.fg_technical_description+'</td><td>'+su+'</td><td>'+v.qty+'</td><td>'+v.rate+'</td><td>'+v.amount+'</td><td>'+re+'</td></tr>'	
			}
		});
		$(frm.fields_dict['linked_pr'].wrapper).html("")
		$(frm.fields_dict['linked_mr'].wrapper).html("")
		$(frm.fields_dict['item_table'].wrapper).html(htvalue);
	},
	check_mr:function(frm,cdt,cdn){
		frm.set_df_property('hide_table', 'hidden', 0);
		frm.set_df_property('preview', 'hidden', 1);
		frm.set_df_property('download', 'hidden', 0);
		frm.set_df_property('download1', 'hidden', 1);
		var d = locals[cdt][cdn];
		var arr1=[]
		var arr=[]
		$.each(frm.doc.items || [], function(i, v) {
			arr1.push({"aa":v.material_request_item})
			if (v.technical_description==undefined){
			arr.push({"idx":v.idx,"item":v.item_code,"description":v.description,"technical_description":"","qty":v.qty,"parent":v.material_request,"child":v.material_request_item})
			}
			else{
			arr.push({"idx":v.idx,"item":v.item_code,"description":v.description,"technical_description":v.technical_description,"qty":v.qty,"parent":v.material_request,"child":v.material_request_item})
			}
		});
		// msgprint(JSON.stringify(arr));
		
		frappe.call({

			"method":"wtt_module.customization.custom.purchase_order.mr_func",
			args:{
				'arr':arr
			},
			callback: function(r) {
				for(var i=0;i<r.message.length;i++){
					var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
					htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%'>S.NO</th><th style='width:4%'>DESCRIPTION</th><th style='width:12%'>TECHNICAL DESCRIPTION</th><th style='width:5%'>PO QUANTITY</th><th style='width:5%'>MR QUANTITY</th><th style='width:5%'>ROW</th><th style='width:8%'>MR</th><th style='width:8%'>MR STATUS</th></tr>"
					
					$.each(r.message, function(i, v) {
					var result=""
					var c=i+1
					// var amt=v.qty*v.rate
					if(v.rate=="-"){
						var amt=v.qty*0
					}
					else{
						var amt=v.qty*v.rate
					}
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
					htvalue+='<tr style="text-align:center;"><td align="center">'+v.idx+'<br></td><td align="center">'+v.description+'<br></td><td align="center">'+result+'<br></td><td align="center">PO qty- '+v.po_qty+'</td><td align="center">MR qty- '+v.qty+'</td><td align="center">MR row- '+v.rate+'</td><td>'+v.parent+'</td><td>'+v.status+'</td></tr>'
					});
					$(frm.fields_dict['linked_pr'].wrapper).html("")
					$(frm.fields_dict['item_table'].wrapper).html("");
					$(frm.fields_dict['linked_mr'].wrapper).html(htvalue)					
					}
			}
		});
	},
	check_receipt:function(frm,cdt,cdn){
		frm.set_df_property('hide_table', 'hidden', 0);
		frm.set_df_property('preview', 'hidden', 1);
		frm.set_df_property('download', 'hidden', 1);
		frm.set_df_property('download1', 'hidden', 0);
		var d = locals[cdt][cdn];
		var arr=[]

		$.each(frm.doc.items || [], function(i, v) {
			var iar=[]
			iar.push(v.item_code)
			if (v.technical_description==undefined){
			arr.push({"idx":v.idx,"item":v.item_code,"description":v.description,"technical_description":"","qty":v.qty,"parent":v.parent,"child":v.name,"mr2":v.material_request})
			}
			else{
			arr.push({"idx":v.idx,"item":v.item_code,"description":v.description,"technical_description":v.technical_description,"qty":v.qty,"parent":v.parent,"child":v.name,"mr2":v.material_request})
			}	
		});

		frappe.call({
			"method":"wtt_module.customization.custom.purchase_order.pr_func",
			args:{
				'arr':arr
			},
			callback: function(r) {

				for(var i=0;i<r.message.length;i++){
					
					var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
					htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%'>S.NO</th><th style='width:3%'>DESCRIPTION</th><th style='width:12%'>TECHNICAL DESCRIPTION</th><th style='width:2%'>PO QTY</th><th style='width:2%'>PR QTY</th><th style='width:1%'>PR ROW</th><th style='width:8%'>RECEIPT NO</th><th style='width:8%'>MR LINKED TO PR</th><th style='width:1%'>MR ROW</th><th style='width:1%'>MR QTY</th><th style='width:8%'>PR STATUS</th><th style='width:8%'>MR</th></tr>"
					
					$.each(r.message, function(i, v) {
					var result=""
					var c=i+1
					// var amt=v.qty*v.rate
					if(v.rate=="-"){
						var amt=v.qty*0
					}
					else{
						var amt=v.qty*v.rate
					}
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
					
					htvalue+='<tr style="text-align:center;"><td align="center">'+v.idx+'<br></td><td align="center">'+v.description+'<br></td><td align="center">'+result+'<br></td><td align="center">PO qty- '+v.po_qty+'</td><td align="center">PR qty- '+v.qty+'</td><td align="center">PR row- '+v.rate+'</td><td>'+v.parent+'<br>'+v.date+'</td><td>'+v.mr+'</td><td>MR row- '+v.mr_row+'</td><td>MR qty- '+v.mr_qty+'</td><td>'+v.status+'</td><td>'+v.mr2+'</td></tr>'
					});
					$(frm.fields_dict['linked_mr'].wrapper).html("")
					$(frm.fields_dict['item_table'].wrapper).html("");
					$(frm.fields_dict['linked_pr'].wrapper).html(htvalue)					
					}
				

			}

		});
	},
	download:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		var arr=[]
		$.each(frm.doc.items || [], function(i, v) {
			if (v.technical_description==undefined){
			arr.push({"idx":v.idx,"item":v.item_code,"description":v.description,"technical_description":"","qty":v.qty,"parent":v.material_request,"child":v.material_request_item,"mr2":v.material_request})
			}
			else{
			arr.push({"idx":v.idx,"item":v.item_code,"description":v.description,"technical_description":v.technical_description,"qty":v.qty,"parent":v.material_request,"child":v.material_request_item,"mr2":v.material_request})
			}	
		});
		frappe.call({
			"method":"wtt_module.customization.custom.purchase_order.download_mr_func",
			args:{
				'arr':arr
			},
			callback: function(r) {	
				for(var i=0;i<r.message.length;i++){
				var file_url=JSON.stringify(r.message[0].url)
				file_url = file_url.replace(/#/g, '%23');
				file_url = file_url.replace(/"/g, '');
				window.open(file_url);
				}
			}
		});
	},
	download1:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		var arr=[]
		$.each(frm.doc.items || [], function(i, v) {
			if (v.technical_description==undefined){
			arr.push({"idx":v.idx,"item":v.item_code,"description":v.description,"technical_description":"","qty":v.qty,"parent":v.parent,"child":v.name,"mr2":v.material_request})
			}
			else{
			arr.push({"idx":v.idx,"item":v.item_code,"description":v.description,"technical_description":v.technical_description,"qty":v.qty,"parent":v.parent,"child":v.name,"mr2":v.material_request})
			}	
		});
		frappe.call({
			"method":"wtt_module.customization.custom.purchase_order.download_pr_func",
			args:{
				'arr':arr
			},
			callback: function(r) {	
				for(var i=0;i<r.message.length;i++){
				var file_url=JSON.stringify(r.message[0].url)
				file_url = file_url.replace(/#/g, '%23');
				file_url = file_url.replace(/"/g, '');
				window.open(file_url);
				}
			}
		});
		
	},
	target_warehouse:function(frm){
		// alert(frm.doc.target_warehouse)
		frm.set_value("set_warehouse",frm.doc.target_warehouse)
	},
	onload: function(frm) {
		// add item, if previous view was item
		erpnext.utils.add_item(frm);

		// set schedule_date
		set_schedule_date(frm);

		frm.set_query("project", "items", function() {
		    return {
				filters: [
					["Project","status", "!=", "Open"],
					["Project","status", "!=", "Cancelled"],
					["Project","status", "!=", "Completed"]
				]
			};
		});
	},
	refresh: function(frm) {
		job_order_request(frm);
		if(frappe.session.user=='venkat@wttindia.com' || frappe.session.user=='sarnita@wttindia.com' || frappe.session.user == 'Administrator'){
			frm.add_custom_button(__('Allow Over Stock'), () => frm.events.function_name(frm));	
		}


		if(frm.doc.workflow_state=='Emergency Approval'){
		if (frappe.session.user=='venkat@wttindia.com' || frappe.session.user=='harshini@wttindia.com'){
		frm.add_custom_button(__('Proceed'), function(){
        frappe.call({
        	method:"wtt_module.customization.custom.purchase_order.approve_after_emergency_approval",
        	args:{
        		nn:frm.doc.name
        	},
        	callback(r){
        		frm.dirty();
				frm.reload_doc();
        	}
        })
    	});
    	}
		}


		frm.set_df_property('download1', 'hidden', 1);
		frm.set_df_property('download', 'hidden', 1);
		frm.set_df_property('hide_table', 'hidden', 1);
		$(frm.fields_dict['item_table'].wrapper).html("");
		$(frm.fields_dict['linked_mr'].wrapper).html("");
		$(frm.fields_dict['linked_pr'].wrapper).html("");
		// frm.toggle_reqd('customer', frm.doc.material_request_type=="Customer Provided");
		if (frm.doc.docstatus==0) {
			frm.add_custom_button(__('Job Order'), () => frm.events.get_items_from_issue(frm),
				__("Get Items From"));
		}
		if (frm.doc.docstatus==0) {
			frm.add_custom_button(__('Nesting and Machining'), () => frm.events.get_items_from_nesting(frm),
				__("Get Items From"));
		}
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Supplier Quotation'), () => frm.events.get_items_from_quotation(frm),
				__("Get Items From"));
		}
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Service Request'), () => frm.events.get_service_request(frm),
				__("Get Items From"));
		}
		if(frm.doc.docstatus == 1)
		{
			frm.add_custom_button(__('Send Mail for Order Confirmation'), () => frm.events.order_confirmation(frm));
		}
		
	},
	function_name:function(frm){
		frappe.confirm('Are you sure you want to proceed?',
	    () => {
	        frappe.call({
			method:"wtt_module.customization.custom.frappe_call.allow_over_stock",
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
	get_items_from_issue:function(frm){
		frm.set_value("naming_series","JOB-.YY.-");
		// frm.set_value("is_subcontracted",1);
		frm.refresh_field("naming_series");
		// frm.refresh_field("is_subcontracted");
		frm.set_value("purpose","Job Order");
		frm.refresh_field("purpose");

		erpnext.utils.map_current_doc({
			method: "wtt_module.customization.custom.purchase_order.make_request",
			source_doctype: "Job Order Request",
			target: frm,
			date_field: "posting_date",
			setters: {
				company: frm.doc.company,
			},
			get_query_filters: {
				docstatus: 1
			}
		});
	},
	get_items_from_nesting:function(frm){
		frm.set_value("naming_series","JOB-.YY.-");
		frm.refresh_field("naming_series");
		frm.set_value("purpose","Job Order");
		frm.refresh_field("purpose");

		erpnext.utils.map_current_doc({
			method: "wtt_module.customization.custom.purchase_order.make_nesting",
			source_doctype: "Nesting and Machining",
			target: frm,
			setters: {
				company: frm.doc.company,
			},
			get_query_filters: {
				docstatus: 0
			}
		});
	},
	get_items_from_quotation:function(frm){
		frm.set_value("naming_series","PO-.YY.-");
		frm.set_value("is_subcontracted",0);
		frm.refresh_field("naming_series");
		frm.refresh_field("is_subcontracted");
		frm.set_value("purpose","");
		frm.refresh_field("purpose");
		erpnext.utils.map_current_doc({
					method: "wtt_module.customization.custom.purchase_order.make_supplier_quote",
					source_doctype: "Supplier Quotation",
					target: frm,
					setters: {
						supplier: frm.doc.supplier,
						valid_till: undefined
					},
					get_query_filters: {
						docstatus: 1,
						status: ["not in", ["Stopped", "Expired"]],
					}
				})
	},

	get_service_request:function(frm){
		frm.set_value("naming_series","SER-.YY.-");
		frm.set_value("is_subcontracted",0);
		frm.refresh_field("naming_series");
		frm.refresh_field("is_subcontracted");
		frm.set_value("purpose","");
		frm.refresh_field("purpose");
		erpnext.utils.map_current_doc({
					method: "wtt_module.customization.custom.purchase_order.make_service_request",
					source_doctype: "Service Request",
					target: frm,
					setters: {
						schedule_date: undefined,
						status: undefined
					},
					get_query_filters: {
						docstatus: 1
					}
		})
	},
	order_confirmation:function(frm)
	{
		frappe.confirm('Are you sure you send the mail to supplier?',
	    () => {
	        frappe.call({
			method:"wtt_module.customization.custom.frappe_call.order_confirmation_mail",
			args:{
				"ref_name":frm.doc.name,
				"supplier":frm.doc.supplier
			},
			callback(r){
				frappe.msgprint("Mail sent")
				// frm.set_value("order_confirmation_mail","Order Confirmation Mail Sent");
				// frm.refresh_field("order_confirmation_mail");
				// frm.save();
			}
			})
	    }, () => {
	       frappe.msgprint({
			    title: __('Error'),
			    indicator: 'red',
			    message: __('Aborted')
			});
	    })
	}
});
frappe.ui.form.on('Raw Materials Purchase Order', {
	qty:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "amount", child.rate * child.qty);
		frm.refresh_field("amount");
	},
	rate:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "amount", child.rate * child.qty);
		frm.refresh_field("amount");
	}
});
frappe.ui.form.on("PO Status",{
	setup:function(frm,cdt,cdn){
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status","=", 'Active']
				]
			}

		});
	},
	po_status_add: function(frm,cdt,cdn) {
		var child=locals[cdt][cdn];
		frappe.db.get_value("Employee",{"user_id":frappe.session.user},'name')
			.then(r => {
		        child.employee=r.message.name;
		        child.employee_name=frappe.session.user_fullname;
		        if(frm.doc.workflow_state==undefined){child.workflow_state="Created"}
		        else{child.workflow_state=frm.doc.workflow_state}
		    })
		frm.refresh_field("po_status");
	}
})
var job_order_request = function(frm){
	
	if(frm.doc.docstatus==1 && frm.doc.is_subcontracted==1){
		frm.add_custom_button(__('Transfer'), function() {
			frappe.model.open_mapped_doc({
    			method: "wtt_module.customization.custom.purchase_order.create_stock_entry",
    			frm: frm
    		});
        },("Manage"));
        frm.add_custom_button(__('Receive'), function() {
			frappe.model.open_mapped_doc({
    			method: "wtt_module.customization.custom.purchase_order.receive_fg_items",
    			frm: frm
    		});
        },("Manage"));
    }
}
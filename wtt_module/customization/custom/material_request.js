// {% include 'erpnext/public/js/controllers/buying.js' %};
{% include 'erpnext/stock/doctype/material_request/material_request.js' %};

frappe.ui.form.on('Material Request', {
	after_save:function(frm){
		// frappe.call({
		// 	method:"wtt_module.customization.custom.material_request.check_multiple_items",
		// 	args:{
		// 		name:frm.doc.name
		// 	},
	
		// })
	},
	validate:function(frm) {
		var arr=[]
		$.each(frm.doc.items || [], function(i, v) {
			arr.push({"item":v.item_code,"qty":v.qty})	
		});

		frappe.call({
			"method":"wtt_module.customization.custom.material_request.get_rate",
			args:{
				'arr':arr
			},
			callback: function(r) {
				frm.set_value("tentative_amount",r.message)
			}
		});

		$.each(frm.doc.items || [], function(i, d) {
			d.project = frm.doc.project;
		});
	
	},
	status:function(frm){
		frm.model.set_value("final_status",frm.doc.status)
	},
	hide_table: function(frm,cdt,cdn){
		frm.set_df_property('hide_table', 'hidden', 1);
		frm.set_df_property('preview', 'hidden', 0);
		$(frm.fields_dict['item_table'].wrapper).html("");
		$(frm.fields_dict['previous_purchase'].wrapper).html("");
		$(frm.fields_dict['ht_rate'].wrapper).html("");
	},
	preview:function(frm,cdt,cdn){
		frm.set_df_property("download","hidden",1)
		frm.set_df_property('hide_table', 'hidden', 0);
		frm.set_df_property('preview', 'hidden', 1);
		var htvalue='<span style="height: 10px; width: 10px; background-color: green; border-radius: 50%;display: inline-block;"></span><b>Ordered&emsp;&emsp;&emsp;&emsp;</b><span style="height: 10px; width: 10px; background-color: blue; border-radius: 50%;display: inline-block;"></span><b>Issued&emsp;&emsp;&emsp;&emsp;</b><span style="height: 10px; width: 10px; background-color: tomato; border-radius: 50%;display: inline-block;"></span><b>Pending</b>&emsp;&emsp;&emsp;&emsp;<span style="height: 10px; width: 10px; background-color: #B1AE04; border-radius: 50%;display: inline-block;"></span><b>Freezed&emsp;&emsp;&emsp;&emsp;</b><br><br><br><style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
		htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>S.NO</th><th style='width:2%'>DESCRIPTION</th><th style='width:15%'>TECHNICAL DESCRIPTION</th><th style='text-align:center;width:5%'>QTY</th><th style='width:8%'>REMARKS</th><th style='width:5%'>DRAWING</th><th style='width:5%'>NAME</th></tr>"
		$.each(frm.doc.items || [], function(i, v) {
			var result=''
			var re=''
			var dn=''
			var dn_res=''
			
			if(v.technical_description)
			{
			var go=[]
			var val=v.technical_description.split(",")
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
			if(v.drawing_no!=undefined){
				// dn=v.drawing_no
				var dn_no=[]
				dn=v.drawing_no.split(",")
				var dn_br = '<br>'
				for(var dds in dn)
				{
					dn_no.push(dn[dds])
					dn_no.push(dn_br)
				}
				dn_res = dn_no.toString().replace(/,/g, "");
			}
			if(v.freeze>0){
				htvalue+='<tr style="text-align:center;"><td align="center"><span style="height: 10px; width: 10px; background-color: #B1AE04; border-radius: 50%;display: inline-block;"></span>&nbsp;'+v.idx+'.</td><td align="center" >'+v.description+'<br></td><td align="left">'+result+'</td><td>'+v.qty+' - '+v.uom+'</td><td>'+re+'</td><td>'+dn_res+'</td><td>'+v.name+'</td></tr>'	
			}
			else if(v.qty<=v.ordered_qty+v.freeze_qty){
				htvalue+='<tr style="text-align:center;"><td align="center"><span style="height: 10px; width: 10px; background-color: green; border-radius: 50%;display: inline-block;"></span>&nbsp;'+v.idx+'.</td><td align="center">'+v.description+'<br></td><td align="left">'+result+'</td><td>'+v.qty+' - '+v.uom+'</td><td>'+re+'</td><td>'+dn_res+'</td><td>'+v.name+'</td></tr>'				
			}
			else if(v.stock_issued_qty>0){
				htvalue+='<tr style="text-align:center;"><td align="center"><span style="height: 10px; width: 10px; background-color: blue; border-radius: 50%;display: inline-block;"></span>&nbsp;'+v.idx+'.</td><td align="center" >'+v.description+'<br></td><td align="left">'+result+'</td><td>'+v.qty+' - '+v.uom+'</td><td>'+re+'</td><td>'+dn_res+'</td><td>'+v.name+'</td></tr>'
			}
			else if(v.qty>v.ordered_qty+v.freeze_qty){
				htvalue+='<tr style="text-align:center;"><td align="center"><span style="height: 10px; width: 10px; background-color: tomato; border-radius: 50%;display: inline-block;"></span>&nbsp;'+v.idx+'.</td><td align="center" >'+v.description+'<br></td><td align="left">'+result+'</td><td>'+v.qty+' - '+v.uom+'</td><td>'+re+'</td><td>'+dn_res+'</td><td>'+v.name+'</td></tr>'	
			}		
		});
		$(frm.fields_dict['ht_rate'].wrapper).html("")
		$(frm.fields_dict['previous_purchase'].wrapper).html("")
		$(frm.fields_dict['item_table'].wrapper).html(htvalue);
	},
	check_po:function(frm,cdt,cdn){
		frm.set_df_property("download","hidden",0)
		frm.set_df_property("download1","hidden",1)
		var d = locals[cdt][cdn];
		var arr=[]
		$.each(frm.doc.items || [], function(i, v) {
			if (v.technical_description==undefined){
			arr.push({"nn":v.name,"idx":v.idx,"item":v.item_code,"description":v.description,"technical_description":"","qty":v.qty,"parent":v.parent})
			}
			else{
			arr.push({"nn":v.name,"idx":v.idx,"item":v.item_code,"description":v.description,"technical_description":v.technical_description,"qty":v.qty,"parent":v.parent})
			}	
		});
		console.log(JSON.stringify(arr))
		frappe.call({
			"method":"wtt_module.customization.custom.material_request.po_func",
			args:{
				'arr':arr
			},
			callback: function(r) {

				for(var i=0;i<r.message.length;i++){
					
					var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
					htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%'>MR ROW</th><th style='width:4%'>DESCRIPTION</th><th style='width:12%'>TECHNICAL DESCRIPTION</th><th style='width:5%'>MR QTY</th><th style='width:5%'>PO QTY</th><th style='width:5%'>PO ROW</th><th style='width:8%'>PO</th><th style='width:8%'>PO STATUS</th><th style='width:5%'>PR QTY</th><th style='width:5%'>PR ROW</th><th style='width:8%'>PR</th><th style='width:8%'>PR STATUS</th></tr>"
					
					$.each(r.message, function(i, v) {
					var result=""
					var c=i+1
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

					if(v.supplier_description!="-"){
						result += "<hr><b>Supplier Descrtion</b><br>"
						result += v.supplier_description
					}
					htvalue+='<tr style="text-align:center;"><td align="center">'+v.idx+'<br></td><td align="center">'+v.description+'<br></td><td align="center">'+result+'<br></td><td align="center">MR qty- '+v.mr_qty+'</td><td align="center">PO qty- '+v.qty+'</td><td align="center">PO row- '+v.rate+'</td><td>'+v.parent+'</td><td>'+v.status+'</td><td align="center">PR qty- '+v.pr_qty+'</td><td align="center">PR row- '+v.pr_row+'</td><td>'+v.pr+'</td><td>'+v.pr_status+'</td></tr>'
					});
					$(frm.fields_dict['ht_rate'].wrapper).html("")
					$(frm.fields_dict['item_table'].wrapper).html("");
					$(frm.fields_dict['previous_purchase'].wrapper).html(htvalue)					
					}
				

			}

		});
		
	},
	get_rate:function(frm,cdt,cdn){
		frm.set_df_property("download","hidden",1);
		frm.set_df_property("download1","hidden",0);
		var d = locals[cdt][cdn];
		var arr=[]
		$.each(frm.doc.items || [], function(i, v) {
			if (v.technical_description==undefined){
			arr.push({"nn":v.name,"item":v.item_code,"description":v.description,"technical_description":"","qty":v.qty})
			}
			else{
			arr.push({"nn":v.name,"item":v.item_code,"description":v.description,"technical_description":v.technical_description,"qty":v.qty})
			}	
		});

		frappe.call({
			// alert(str(arr));
			"method":"wtt_module.customization.custom.material_request.po_rate_func",
			args:{
				'arr':arr
			},
			callback: function(r) {

				for(var i=0;i<r.message.length;i++){
					
					var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
					htvalue+="<br><table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%'>S.NO</th><th style='width:4%'>DESCRIPTION</th><th style='width:12%'>TECHNICAL DESCRIPTION</th><th style='width:5%'>QUANTITY</th><th style='width:5%'>RATE</th><th style='width:5%'>AMOUNT</th><th style='width:8%'>PO</th><th style='width:8%'>PO STATUS</th></tr>"
					
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
					htvalue+='<tr style="text-align:center;"><td align="center">'+c+'<br></td><td align="center">'+v.description+'<br></td><td align="center">'+result+'<br></td><td align="center">'+v.qty+'</td><td align="center">'+v.rate+'</td><td align="center">'+parseFloat(amt).toFixed(2)+'</td><td>'+v.parent+'<br>'+v.supplier+'<br>'+v.date+'</td><td>'+v.status+'</td</tr>'

					});
					htvalue+='</table><br><br>'
					// if(frappe.session.user=='Administrator' || frappe.session.user=='venkat@wttindia.com'|| frappe.session.user=='poa@wttindia.com'|| frappe.session.user=='malayalaraj@wtt.com'){
					$(frm.fields_dict['previous_purchase'].wrapper).html("")
					$(frm.fields_dict['item_table'].wrapper).html("");
					$(frm.fields_dict['ht_rate'].wrapper).html(htvalue)
					// }
					// else{
					// $(frm.fields_dict['ht_rate'].wrapper).html("You are not permitted")
					// frappe.throw("Sorry,It is only for MD sir Reference")
					// }
					}
				

			}

		});
		
	},
	download:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		var arr=[]
		$.each(frm.doc.items || [], function(i, v) {
			if (v.technical_description==undefined){
			arr.push({"nn":v.name,"idx":v.idx,"item":v.item_code,"description":v.description,"technical_description":"","qty":v.qty,"parent":v.parent})
			}
			else{
			arr.push({"nn":v.name,"idx":v.idx,"item":v.item_code,"description":v.description,"technical_description":v.technical_description,"qty":v.qty,"parent":v.parent})
			}	
		});
		if(frm.fields_dict['ht_rate'].wrapper!=""){
		frappe.call({
			"method":"wtt_module.customization.custom.material_request.download_po_func",
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
		}
	},
	download1:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		var arr=[]
		$.each(frm.doc.items || [], function(i, v) {
			if (v.technical_description==undefined){
			arr.push({"nn":v.name,"idx":v.idx,"item":v.item_code,"description":v.description,"technical_description":"","qty":v.qty,"parent":v.parent})
			}
			else{
			arr.push({"nn":v.name,"idx":v.idx,"item":v.item_code,"description":v.description,"technical_description":v.technical_description,"qty":v.qty,"parent":v.parent})
			}	
		});
		if(frm.fields_dict['previous_purchase'].wrapper!=""){
		frappe.call({
			"method":"wtt_module.customization.custom.material_request.download_rate",
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
		}
	},
	update_changes:function(frm,cdt,cdn){
		frm.set_value("edit_items",0);
		frm.refresh_field("edit_items");
		frm.save();
		frappe.confirm('Are you sure you want to update changes?',
	    () => {
			frappe.call({
				method:"wtt_module.customization.custom.material_request.filter_and_update",
				args:{
					"ar":frm.doc.edit_table,
					"parent":frm.doc.name
				},
				callback(r){
					frm.reload_doc()
				}
			})
	    }, 
	    () => {
	        frappe.throw("Aborted")
	    })
	},

	setup: function(frm,cdt,cdn) {

		var d = locals[cdt][cdn];
		frm.custom_make_buttons = {
			'Stock Entry': 'Issue Material',
			'Pick List': 'Pick List',
			'Purchase Order': 'Purchase Order',
			'Request for Quotation': 'Request for Quotation',
			'Supplier Quotation': 'Supplier Quotation',
			'Work Order': 'Work Order'
		};
		// formatter for material request item
		
		// frm.set_indicator_formatter('item_code',
		// function(doc) { return (doc.stock_qty<=doc.ordered_qty) ? "green" : "orange"; });
		
		frm.set_indicator_formatter('item_code',
		function (doc) {
				if(doc.stock_issued_qty>0) {
					return "cyan";
				}
				else {
					
					return (doc.stock_qty<=doc.ordered_qty) ? "green" : "orange";
				}
			}
		);

		frm.set_query("from_warehouse", "items", function(doc) {
			return {
				filters: {'company': doc.company}
			};
		});
		if(frm.doc.docstatus!=1){
			frm.set_df_property('download_table', 'hidden', 1);
		}

		
	},
	project: function(frm) {
	$.each(frm.doc.items || [], function(i, d) {
	d.project = frm.doc.project;
	});
	refresh_field("project");
	},
	schedule_date: function(frm) {
	$.each(frm.doc.items || [], function(i, d) {
	d.schedule_date = frm.doc.schedule_date;
	});
	refresh_field("schedule_date");
	},
	onload: function(frm) {
		// add item, if previous view was item
		erpnext.utils.add_item(frm);

		// set schedule_date
		set_schedule_date(frm);

		frm.set_query("warehouse", "items", function(doc) {
			return {
				filters: {'company': doc.company}
			};
		});

		frm.set_query("set_warehouse", function(doc){
			return {
				filters: {'company': doc.company}
			};
		});

		frm.set_query("set_from_warehouse", function(doc){
			return {
				filters: {'company': doc.company}
			};
		});

		frm.set_query("project", function() {
			return {
				filters: [
					["Project","status", "!=", "Open"],
					["Project","status", "!=", "Cancelled"],
					["Project","status", "!=", "Completed"]
					
				]
			};
		});

		frm.set_query("project", "items", function() {
		    return {
				filters: [
					["Project","status", "!=", "Open"],
					["Project","status", "!=", "Cancelled"],
					["Project","status", "!=", "Completed"]
				]
			};
		});
		if(frm.doc.downgrade_value!="downgraded"){
			frm.set_df_property("get_materials","hidden",1);
			frm.set_df_property("update_items","hidden",1);
		}
	},

	onload_post_render: function(frm) {
		frm.get_field("items").grid.set_multiple_add("item_code", "qty");
	},

	refresh: function(frm) {
		// frm.add_custom_button(__('Update Items'), () => {
		// 	erpnext.utils.update_child_items({
		// 		frm: frm.doc,
		// 		child_docname: "items",
		// 		child_doctype: "Material Request Item",
		// 		cannot_add_row: false,
		// 	})
		// });

		// if(frm.doc.name.includes("new-material-request")){
		// 	frm.set_df_property("items","read_only",1);
		// 	frappe.msgprint("Kindly use Pre MR to avoid Item Repeatations")
		// 	frappe.set_route("Form","Pre MR","new-pre-mr-1")
			
		// }
		frm.get_docfield("edit_table").allow_bulk_edit = 1;
		if(frm.doc.docstatus==1)
		{
			//$('.form-attachments').hide();
			$('.add-attachment-btn').hide(); 
		}
		
		// if(frm.doc.items==undefined){
		// 	frm.set_df_property("items","read_only",1)
		// }
		// else{
		// 	frm.set_df_property("items","read_only",0)	
		// }
		
		if(frm.doc.workflow_state=='Emergency Approval'){
		frm.add_custom_button(__('Proceed'), function(){
		if (frappe.session.user=='venkat@wttindia.com' || frappe.session.user=='Administrator'){
        frappe.call({
        	method:"wtt_module.customization.custom.material_request.approve_after_emergency_approval",
        	args:{
        		nn:frm.doc.name
        	},
        	callback(r){
        		frm.dirty();
				frm.reload_doc();
        	}
        })
		}
		else{
			frappe.throw("Not Permitted")
		}
    	});
		}


		if(frm.doc.downgrade_value!="downgraded"){
			frm.set_df_property("get_materials","hidden",1);
			frm.set_df_property("update_items","hidden",1);
		}
		
		if(frm.doc.downgrade_value=='downgraded')
		{
			frm.set_df_property("edit_table","hidden",0);
			frm.set_df_property("update_changes","hidden",0);
			if(frappe.session.user=="Administrator"){
				frm.set_df_property("items","read_only",0);
			}
			else{
				frm.set_df_property("items","read_only",1);
			}
		
		}
		

		frm.set_df_property("download","hidden",1)
		frm.set_df_property("download1","hidden",1)
		frm.set_df_property('hide_table', 'hidden', 1);
		$(frm.fields_dict['item_table'].wrapper).html("");
		$(frm.fields_dict['previous_purchase'].wrapper).html("");
		$(frm.fields_dict['ht_rate'].wrapper).html("");
		$(frm.fields_dict['html'].wrapper).html("")
		frm.toggle_reqd('customer', frm.doc.material_request_type=="Customer Provided");
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Material Issue'), () => frm.events.get_items_from_issue(frm),
				__("Get Items From"));
			frm.add_custom_button(__('Tag List'), () => frm.events.get_items_from_tag(frm),
				__("Get Items From"));
		
			
		
			
		}
		// if (frm.doc.docstatus===1){
			
		// 	if(frappe.session.user=='venkat@wttindia.com' || frappe.session.user=='sarnita@wttindia.com' || frappe.session.user=='harshini@wttindia.com' || frappe.session.user=='Administrator')
		// 	// if(frappe.session.user=='Administrator')
		// 	{
		// 	frm.add_custom_button(__('Downgrade'), () => {
		// 	frappe.call({
		// 	method: 'wtt_module.customization.custom.material_request.downgrade',
		// 	args: { name: frm.doc.name },
		// 		callback(r) {
		// 			if (!r.exc) {
		// 				frm.reload_doc();
		// 			}
		// 		}
		// 	});	
		// 	});
		// 	}
		// }
	},
	get_items_from_issue:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.customization.custom.material_request.make_request",
					source_doctype: "Material Request",
					target: frm,
					date_field: "transaction_date",
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 1
					}
				});
	},
	
	get_items_from_tag:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.customization.custom.material_request.make_tag",
					source_doctype: "Tag Listing",
					target: frm,
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 0
					}
				});
	},
	update_status: function(frm, stop_status) {
		frappe.call({
			method: 'erpnext.stock.doctype.material_request.material_request.update_status',
			args: { name: frm.doc.name, status: stop_status },
			callback(r) {
				if (!r.exc) {
					frm.reload_doc();
				}
			}
		});
	},

	get_items_from_sales_order: function(frm) {
		erpnext.utils.map_current_doc({
			method: "erpnext.selling.doctype.sales_order.sales_order.make_material_request",
			source_doctype: "Sales Order",
			target: frm,
			setters: {
				company: frm.doc.company
			},
			get_query_filters: {
				docstatus: 1,
				status: ["not in", ["Closed", "On Hold"]],
				per_delivered: ["<", 99.99],
			}
		});
	},

	get_item_data: function(frm, item) {
		if (item && !item.item_code) { return; }

		frm.call({
			method: "erpnext.stock.get_item_details.get_item_details",
			child: item,
			args: {
				args: {
					item_code: item.item_code,
					warehouse: item.warehouse,
					doctype: frm.doc.doctype,
					buying_price_list: frappe.defaults.get_default('buying_price_list'),
					currency: frappe.defaults.get_default('Currency'),
					name: frm.doc.name,
					qty: item.qty || 1,
					stock_qty: item.stock_qty,
					company: frm.doc.company,
					conversion_rate: 1,
					material_request_type: frm.doc.material_request_type,
					plc_conversion_rate: 1,
					rate: item.rate,
					conversion_factor: item.conversion_factor
				}
			},
			callback: function(r) {
				const d = item;
				if(!r.exc) {
					$.each(r.message, function(k, v) {
						if(!d[k]) d[k] = v;
					});
				}
			}
		});
	},

	get_items_from_bom: function(frm) {
		var d = new frappe.ui.Dialog({
			title: __("Get Items from BOM"),
			fields: [
				{"fieldname":"bom", "fieldtype":"Link", "label":__("BOM"),
					options:"BOM", reqd: 1, get_query: function() {
						return {filters: { docstatus:1 }};
					}},
				{"fieldname":"warehouse", "fieldtype":"Link", "label":__("Warehouse"),
					options:"Warehouse", reqd: 1},
				{"fieldname":"qty", "fieldtype":"Float", "label":__("Quantity"),
					reqd: 1, "default": 1},
				{"fieldname":"fetch_exploded", "fieldtype":"Check",
					"label":__("Fetch exploded BOM (including sub-assemblies)"), "default":1},
				{fieldname:"fetch", "label":__("Get Items from BOM"), "fieldtype":"Button"}
			]
		});
		d.get_input("fetch").on("click", function() {
			var values = d.get_values();
			if(!values) return;
			values["company"] = frm.doc.company;
			if(!frm.doc.company) frappe.throw(__("Company field is required"));
			frappe.call({
				method: "erpnext.manufacturing.doctype.bom.bom.get_bom_items",
				args: values,
				callback: function(r) {
					if (!r.message) {
						frappe.throw(__("BOM does not contain any stock item"));
					} else {
						erpnext.utils.remove_empty_first_row(frm, "items");
						$.each(r.message, function(i, item) {
							var d = frappe.model.add_child(cur_frm.doc, "Material Request Item", "items");
							d.item_code = item.item_code;
							d.item_name = item.item_name;
							d.description = item.description;
							d.warehouse = values.warehouse;
							d.uom = item.stock_uom;
							d.stock_uom = item.stock_uom;
							d.conversion_factor = 1;
							d.qty = item.qty;
							d.project = item.project;
						});
					}
					d.hide();
					refresh_field("items");
				}
			});
		});
		d.show();
	},

	make_purchase_order: function(frm) {
				frappe.model.open_mapped_doc({
					method: "erpnext.stock.doctype.material_request.material_request.make_purchase_order",
					frm: frm,
					run_link_triggers: true
				});
	},

	make_request_for_quotation: function(frm) {
		frappe.model.open_mapped_doc({
			method: "wtt_module.customization.custom.material_request.make_request_for_quotation",
			frm: frm,
			run_link_triggers: true
		});
	},

	make_supplier_quotation: function(frm) {
		frappe.model.open_mapped_doc({
			method: "erpnext.stock.doctype.material_request.material_request.make_supplier_quotation",
			frm: frm
		});
	},

	make_stock_entry: function(frm) {
		frappe.model.open_mapped_doc({
			method: "erpnext.stock.doctype.material_request.material_request.make_stock_entry",
			frm: frm
		});
	},

	create_pick_list: (frm) => {
		frappe.model.open_mapped_doc({
			method: "erpnext.stock.doctype.material_request.material_request.create_pick_list",
			frm: frm
		});
	},

	raise_work_orders: function(frm) {
		frappe.call({
			method:"erpnext.stock.doctype.material_request.material_request.raise_work_orders",
			args: {
				"material_request": frm.doc.name
			},
			callback: function(r) {
				if(r.message.length) {
					frm.reload_doc();
				}
			}
		});
	},
	material_request_type: function(frm) {
		frm.toggle_reqd('customer', frm.doc.material_request_type=="Customer Provided");
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
	}

});
frappe.ui.form.on("Filter Items", {
	before_edit_table_remove:function(frm,cdt,cdn){
		frm.set_df_property("items","read_only",0);

		var d = locals[cdt][cdn];
		$.each(frm.doc.items || [], function(i, k) {
		if(k.name==d.row_name){
			frm.get_field("items").grid.grid_rows[i].remove();
		}
		else if(k.corrected_from==d.name){
			frm.get_field("items").grid.grid_rows[i].remove();
		}

		frm.refresh_field("items")

		})
		frm.set_df_property("items","read_only",1);
	}


});


frappe.ui.form.on("Material Request Item", {
	qty: function (frm, doctype, name) {

		var d = locals[doctype][name];
		if (flt(d.qty) < flt(d.min_order_qty)) {
			frappe.msgprint(__("Warning: Material Requested Qty is less than Minimum Order Qty"));
		}
		const item = locals[doctype][name];
		frm.events.get_item_data(frm, item);
		frappe.model.set_value(item.doctype,item.name,"bal_qty",item.qty);
	},

	rate: function(frm, doctype, name) {
		const item = locals[doctype][name];
		frm.events.get_item_data(frm, item);
	},

	item_code: function(frm, doctype, name) {
		const item = locals[doctype][name];
		item.rate = 0;
		set_schedule_date(frm);
		frm.events.get_item_data(frm, item);
	},

	schedule_date: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.schedule_date) {
			if(!frm.doc.schedule_date) {
				erpnext.utils.copy_value_in_all_rows(frm.doc, cdt, cdn, "items", "schedule_date");
			} else {
				set_schedule_date(frm);
			}
		}
	}
});

// erpnext.buying.MaterialRequestController = erpnext.buying.BuyingController.extend({
// 	tc_name: function() {
// 		this.get_terms();
// 	},

// 	item_code: function() {
// 		// to override item code trigger from transaction.js
// 	},

// 	validate_company_and_party: function() {
// 		return true;
// 	},

// 	calculate_taxes_and_totals: function() {
// 		return;
// 	},

// 	validate: function() {
// 		set_schedule_date(this.frm);
// 	},
// 	onload: function(doc, cdt, cdn) {
// 		this.frm.set_query("item_code", "items", function() {
// 			if (doc.material_request_type == "Customer Provided") {
// 				return{
// 					query: "erpnext.controllers.queries.item_query",
// 					filters:{ 'customer': me.frm.doc.customer }
// 				}
// 			} else if (doc.material_request_type != "Manufacture") {
// 				return{
// 					query: "erpnext.controllers.queries.item_query",
// 					filters: {'is_purchase_item': 1}
// 				}
// 			}
// 		});

		
// 	},

// 	items_add: function(doc, cdt, cdn) {
// 		var row = frappe.get_doc(cdt, cdn);
// 		if(doc.schedule_date) {
// 			row.schedule_date = doc.schedule_date;
// 			refresh_field("schedule_date", cdn, "items");
// 		} else {
// 			this.frm.script_manager.copy_from_first_row("items", row, ["schedule_date"]);
// 		}
// 	},

// 	items_on_form_rendered: function() {
// 		set_schedule_date(this.frm);
// 	},

// 	schedule_date: function() {
// 		set_schedule_date(this.frm);
// 	}
// });

// // for backward compatibility: combine new and previous states
// $.extend(cur_frm.cscript, new erpnext.buying.MaterialRequestController({frm: cur_frm}));
	
// function set_schedule_date(frm) {
// 	if(frm.doc.schedule_date){
// 		erpnext.utils.copy_value_in_all_rows(frm.doc, frm.doc.doctype, frm.doc.name, "items", "schedule_date");
// 	}
// }
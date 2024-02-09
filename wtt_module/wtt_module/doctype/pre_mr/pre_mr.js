// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pre MR', {
	setup:function(frm,cdt,cdn){
		frm.get_docfield("items").allow_bulk_edit = 1;
		frm.get_docfield("combo_table").allow_bulk_edit = 1;

		frm.set_query("set_warehouse", function(doc) {
				return {
					filters: {'company': doc.company}
				};
			});
		var hidebtn = $('*[data-fieldname="items"]');
		hidebtn .find('.grid-add-row').hide();
		hidebtn .find('.grid-remove-rows').hide();
	},
	preview:function(frm,cdt,cdn){
		frm.set_df_property("hide","hidden",0);
		frm.set_df_property("preview","hidden",1);
			var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
			htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>S.NO</th><th style='width:2%'>DESCRIPTION</th><th style='width:15%'>TECHNICAL DESCRIPTION</th><th style='text-align:center;width:5%'>QTY</th><th style='width:8%'>REMARKS</th><th style='width:5%'>DRAWING</th><th style='width:5%'>NAME</th></tr>"
			$.each(frm.doc.items || [], function(i, v) {
				var result=''
				var re=''
				var dn=''
				
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
					dn=v.drawing_no
				}
				htvalue+='<tr style="text-align:center;"><td align="center">&nbsp;'+v.idx+'.</td><td align="center">'+v.description+'<br></td><td align="left">'+result+'</td><td>'+v.qty+' - '+v.uom+'</td><td>'+re+'</td><td>'+dn+'</td><td>'+v.name+'</td></tr>'				
				
			});
			$(frm.fields_dict['html'].wrapper).html(htvalue);
	},
	show_combo_items:function(frm,cdt,cdn){
		frm.set_df_property("hide","hidden",0);
		frm.set_df_property("preview","hidden",1);
			var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
			htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>S.NO</th><th style='width:2%'>DESCRIPTION</th><th style='width:15%'>TECHNICAL DESCRIPTION</th><th style='text-align:center;width:5%'>QTY</th><th style='width:8%'>REMARKS</th><th style='width:5%'>DRAWING</th><th style='width:5%'>NAME</th></tr>"
			$.each(frm.doc.combo_table || [], function(i, v) {
				var result=''
				var re=''
				var dn=''
				
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
					dn=v.drawing_no
				}
				htvalue+='<tr style="text-align:center;"><td align="center">&nbsp;'+v.idx+'.</td><td align="center">'+v.description+'<br></td><td align="left">'+result+'</td><td>'+v.qty+' - '+v.uom+'</td><td>'+re+'</td><td>'+dn+'</td><td>'+v.name+'</td></tr>'				
				
			});
			$(frm.fields_dict['html'].wrapper).html(htvalue);
	},
	hide:function(frm,cdt,cdn){
		frm.set_df_property("preview","hidden",0);
		frm.set_df_property("hide","hidden",1);
		$(frm.fields_dict['html'].wrapper).html("");
	},
	refresh:function(frm,cdt,cdn){
		frm.set_df_property("hide","hidden",1);
		$(frm.fields_dict['html'].wrapper).html("");
		// if (frm.doc.docstatus==0) {
		// 	frm.add_custom_button(__("Bill of Materials"),
		// 		() => frm.events.get_items_from_bom(frm), __("Get Items From"));
		// 	frm.add_custom_button(__('Product Bundle'), () => frm.events.get_items_from_product_bundle(frm),
		// 		__("Get Items From"));
		// }
		
	},
	get_items_from_bom: function(frm) {
		var d = new frappe.ui.Dialog({
			title: __("Get Items from BOM"),
			fields: [
				{"fieldname":"bom", "fieldtype":"Link", "label":__("BOM"),
					options:"BOM", reqd: 1, get_query: function() {
						return {filters: { docstatus:1 }};
					}},
				{"fieldname":"warehouse", "fieldtype":"Link", "label":__("For Warehouse"),
					options:"Warehouse", reqd: 1,"default":"Stores - WTT"},
				{"fieldname":"qty", "fieldtype":"Float", "label":__("Quantity"),
					reqd: 1, "default": 1},
				{"fieldname":"fetch_exploded", "fieldtype":"Check",
					"label":__("Fetch exploded BOM (including sub-assemblies)"), "default":1}
			],
			primary_action_label: 'Get Items',
			primary_action(values) {
				frm.set_value("set_warehouse",values.warehouse)
				frm.refresh_field("set_warehouse");
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
							erpnext.utils.remove_empty_first_row(frm, "combo_table");
							$.each(r.message, function(i, item) {
								var d = frappe.model.add_child(cur_frm.doc, "combo_table");
								d.item_code = item.item_code;
								d.item_name = item.item_name;
								d.description = item.description;
								d.technical_description=item.technical_description;
								d.uom = item.stock_uom;
								d.uom_in_item = item.stock_uom;
								d.stock_uom = item.stock_uom;
								d.conversion_factor = 1;
								d.qty = item.qty;

							});
						}
						d.hide();
						refresh_field("combo_table");
					}
				});
			}
		});

		d.show();
	},
	get_items_from_product_bundle:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.pre_mr.pre_mr.from_product_bundle",
					source_doctype: "Product Bundle",
					target: frm,
					setters: {
						
					},
					get_query_filters: {
						docstatus: 0
					}
				});
	},
	before_save:function(frm,cdt,cdn){
		frm.clear_table("items")
		frm.refresh_field("items");
		var ar=[]
		$.each(frm.doc.combo_table || [],function(i,v){
			var dn="";
			if(v.drawing_no!=undefined){
				dn=v.drawing_no
			}
			var rem="";
			if(v.remarks!=undefined){
				rem=v.remarks
			}
			ar.push({"item_code":v.item_code,"qty":v.qty,"drawing_no":dn,"uom":v.uom,"remarks":rem})
		});
		frappe.call({
			method:"wtt_module.wtt_module.doctype.pre_mr.pre_mr.get_item_list",
			args:{
				"ar":ar
			},
			callback(r){
				for (var i=0;i<r.message.length;i++){
					var doc = frappe.model.add_child(frm.doc, "Pre MR Table", "items");
					doc.item_code=r.message[i].item_code
					doc.pre_mr_uom=r.message[i].uom
					doc.conversion_factor=1
					doc.pre_mr_qty=r.message[i].qty
					doc.drawing_no=r.message[i].drawing_no
					doc.remarks=r.message[i].remarks
					frm.refresh_field("items")
				}
			}
		})		
	}
	// refresh:function(frm){
	// 	frappe.call({
	// 		method:"wtt_module.customization.custom.material_request.downgrade",
	// 		args:{
	// 			name:"MR-22-00449"
	// 		}
	// 	})
	// }
	// validate:function(frm,cdt,cdn){
	// 	var d=locals[cdt][cdn]
	// 	$.each(frm.doc.items||[],function(i,v){
	// 		frappe.model.set_value(d.doctype,d.name,"req_qty",v.qty/1000);
	// 		frappe.model.set_value(d.doctype,d.name,"req_uom","Meter");

	// 	})
	// }
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Combo Table', {
	validate:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		frappe.db.get_value('Item', child.item_code, 'stock_uom')
	    .then(r => {
	        let values = r.message;	        
	        if(values.stock_uom=="Meter"){	        	
	        	frappe.model.set_value(cdt, cdn, "uom", "Millimeter");
	        }
	        else{
	        	frappe.model.set_value(cdt, cdn, "uom", values.stock_uom);
	        }
	    })
	},
	item_code:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		frappe.db.get_value('Item', child.item_code, 'stock_uom')
	    .then(r => {
	        let values = r.message;	        
	        if(values.stock_uom=="Meter"){	        	
	        	frappe.model.set_value(cdt, cdn, "uom", "Millimeter");
	        }
	        else{
	        	frappe.model.set_value(cdt, cdn, "uom", values.stock_uom);
	        }
	    })
	}
});
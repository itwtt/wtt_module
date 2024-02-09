// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Job Order Request', {
	refresh:function(frm){
		frm.set_df_property('hide_table', 'hidden', 1);
		frm.set_df_property('preview', 'hidden', 0);
		$(frm.fields_dict['html_field'].wrapper).html("");

		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Material Request'), () => frm.events.get_items_from_request(frm),
				__("Get Items From"));
		}
	},
	setup: function(frm) {
		// frm.set_query("fg_item", "items", function() {
		//     return {
		// 		filters: [
		// 			["Item","is_sub_contracted_item", "=", 1],
		// 			["Item","is_stock_item", "=", 1],
		// 		]
		// 	};
		// });
		frm.set_query("to_warehouse", function() {
		    return {
				filters: [
					["Warehouse","company", "=", frm.doc.company]

				]
			};
		});

		// frm.toggle_reqd('customer', frm.doc.material_request_type=="Customer Provided");
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Stock Entry'), () => frm.events.get_items_from_issue(frm),
				__("Get Items From"));
		}
		
	},
	hide_table: function(frm,cdt,cdn){
		frm.set_df_property('hide_table', 'hidden', 1);
		frm.set_df_property('preview', 'hidden', 0);
		$(frm.fields_dict['html_field'].wrapper).html("");
	},
	preview:function(frm,cdt,cdn){
		frm.set_df_property('hide_table', 'hidden', 0);
		frm.set_df_property('preview', 'hidden', 1);
		var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
		htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>S.NO</th><th style='width:2%'>DESCRIPTION</th><th style='width:15%'>TECHNICAL DESCRIPTION</th><th style='text-align:center;width:5%'>QTY</th></tr>"
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
			htvalue+='<tr style="text-align:center;"><td align="center">'+v.idx+'.</td><td align="center" >'+v.description+'<br></td><td align="left">'+result+'</td><td>'+v.qty+' - '+v.uom+'</td></tr>'	
				
		});
		$(frm.fields_dict['html_field'].wrapper).html(htvalue);
	},

	get_items_from_issue:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.job_order.job_order.make_request",
					source_doctype: "Stock Entry",
					target: frm,
					date_field: "posting_date",
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 1,
						stock_entry_type: 'Material Receipt'
					}
				});
	},

	get_items_from_request:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.job_order_request.job_order_request.make_entry",
					source_doctype: "Material Request",
					target: frm,
					date_field: "transaction_date",
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 1,
					}
				});
	}



});
frappe.ui.form.on("Job Order Table", {
	qty: function(frm, cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "amount", child.qty * child.basic_rate);
	},
	basic_rate: function(frm, cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "amount", child.qty * child.basic_rate);
	}
});
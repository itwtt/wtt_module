// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
{% include 'erpnext/public/js/controllers/buying.js' %};

frappe.ui.form.on('Material Issue', {
	hide_table: function(frm,cdt,cdn){
		$(frm.fields_dict['item_table'].wrapper).html("");
	},
	preview:function(frm,cdt,cdn){
		var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
		htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>S.NO</th><th style='width:2%'>DESCRIPTION</th><th style='width:15%'>TECHNICAL DESCRIPTION</th><th style='text-align:center;width:5%'>QTY</th><th style='width:8%'>REMARKS</th><th style='width:8%'>DRAWING NO</th></tr>"
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
			// if(v.drawing_no)
			// {
			// 	dd=v.drawing_no
			// }
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
			htvalue+='<tr style="text-align:center;"><td align="center">'+v.idx+'.</td><td align="center">'+v.description+'<br></td><td align="left">'+result+'</td><td>'+v.qty+'</td><td>'+re+'</td><td>'+dn_res+'</td></tr>'
		});
		$(frm.fields_dict['item_table'].wrapper).html(htvalue);
	},
	refresh: function(frm) {
		frm.toggle_reqd('customer', frm.doc.material_request_type=="Customer Provided");
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Material Request'), () => frm.events.get_items_from_issue(frm),
				__("Get Items From"));
		}
		
	},
	get_items_from_issue:function(frm){
		erpnext.utils.map_current_doc({
			method: "wtt_module.wtt_module.doctype.material_issue.material_issue.make_request",
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
	update_status: function(frm, stop_status) {
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.material_issue.material_issue.update_status',
			args: { name: frm.doc.name, status: stop_status },
			callback(r) {
				if (!r.exc) {
					frm.reload_doc();
				}
			}
		});
	}
});

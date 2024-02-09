cur_frm.cscript.refresh = cur_frm.cscript.inspection_type;

frappe.ui.form.on("Item Inspection", {
onload:function(frm){
	frm.set_query("s_warehouse", function() {
		    return {
				filters: [
					["Warehouse","company", "=", frm.doc.company],
					["Warehouse","is_group", "=", "0"]
				]
			};
		});
	frm.set_query("inspected_by", function() {
		    return {
				filters: [
					["Employee","status", "=", 'Active'],
				]
			};
		});
	frm.set_query("verified_by", function() {
		    return {
				filters: [
					["Employee","status", "=", 'Active'],
				]
			};
		});
},
refresh: function(frm) {
	$(frm.fields_dict['html'].wrapper).html("");
	if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Purchase Receipt'), function() {
				erpnext.utils.map_current_doc({
					method: "wtt_module.customization.custom.purchase_receipt.make_quality",
					source_doctype: "Purchase Receipt",
					target: frm,
					date_field: "posting_date",
					setters: {
						supplier: frm.doc.supplier || undefined,
					},
					get_query_filters: {
						docstatus: 0
					}
				})
			}, __("Get items from"));

			
			frm.add_custom_button(__('Subcontracting Receipt'), function() {
				frm.set_value("is_subcontracted",1);
				frm.refresh_field("is_subcontracted");
				erpnext.utils.map_current_doc({
					method: "wtt_module.customization.overrides.subcontracting_receipt.subcontracting_receipt.make_quality",
					source_doctype: "Subcontracting Receipt",
					target: frm,
					date_field: "posting_date",
					setters: {
						supplier: frm.doc.supplier || undefined,
					},
					get_query_filters: {
						docstatus: 0
					}
				})
			}, __("Get items from"));
			
	}	
},
hide_table: function(frm,cdt,cdn){
	$(frm.fields_dict['html'].wrapper).html("");
},
preview:function(frm,cdt,cdn){
	var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
	htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>S.NO</th><th style='width:2%'>DESCRIPTION</th><th style='width:15%'>TECHNICAL DESCRIPTION</th><th style='text-align:center;width:5%'>QTY</th><th style='text-align:center;width:5%'>ACCEPTED QTY</th><th style='text-align:center;width:5%'>REJECTED QTY</th><th style='text-align:center;width:5%'>STATUS</th></tr>"
	$.each(frm.doc.items || [], function(i, v) {
		var result=''
		var re=''
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
		htvalue+='<tr style="text-align:center;"><td align="center">'+v.idx+'.</td><td align="center">'+v.description+'<br></td><td align="center">'+result+'</td><td>'+v.qty+'</td><td>'+v.acc_qty+'</td><td>'+v.rej_qty+'</td><td>'+v.ins_status+'</td></tr>'
	});
	$(frm.fields_dict['html'].wrapper).html(htvalue);
},
s_warehouse: function(frm) {
$.each(frm.doc.items || [], function(i, d) {
if(!d.s_warehouse) d.s_warehouse = frm.doc.s_warehouse;
});
refresh_field("s_warehouse");
}
});

frappe.ui.form.on("Item Inspection item", {
	acc_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "rej_qty", child.qty - child.acc_qty);
		calculate_total(frm, cdt, cdn);
	},
	rate: function(frm, cdt, cdn){
		calculate_total(frm, cdt, cdn);
	},
	ins_status: function(frm, cdt, cdn){
		calculate_total(frm, cdt, cdn);
	},
	s_warehouse: function(frm, cdt, cdn) {
	if(!frm.doc.s_warehouse) {
	erpnext.utils.copy_value_in_all_rows(frm.doc, cdt, cdn, "items","s_warehouse");
	refresh_field("s_warehouse");
	}
	}
});
var calculate_total = function(frm, cdt, cdn) {
	var child = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "amount", child.acc_qty * child.rate);

	var i,sum=0,sum_amount=0,sub=0,sub_amount=0,val,val2,r;
	var temp = frm.doc.items;

	for(i=0;i<temp.length;i++)
	{
		if(temp[i].ins_status=="Accepted")
		{
		sum+=temp[i].acc_qty;
		sum_amount+=temp[i].amount;
		}
	}
	if(child.ins_status=="Accepted")
	{
	frm.set_value("total_qty",sum);
	frm.set_value("total",sum_amount);
	}
	else if(child.ins_status=="Rejected")
	{
	frappe.model.set_value(cdt, cdn, "acc_qty",0.00);
	frappe.model.set_value(cdt, cdn, "rej_qty",child.qty);
	frm.set_value("total_qty",sum);
	frm.set_value("total",sum_amount);
	}
}

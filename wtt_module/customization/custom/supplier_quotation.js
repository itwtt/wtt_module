{% include 'erpnext/buying/doctype/supplier_quotation/supplier_quotation.js' %};
frappe.ui.form.on("Supplier Quotation", {
	setup: function(frm) {
		frm.get_docfield('combined_table').allow_bulk_edit = 1;
		// frm.get_docfield('supplier_data_table').allow_bulk_edit = 1;
		
	},
	upload:function(frm){
		frappe.call({
			method:"wtt_module.customization.custom.supplier_quotation.get_data_from_excel",
			args:{
				file_path:"C:/Users/erp-1/Downloads/RFQ-22-00168.csv"
			}
		})
	},
	get_combined:function(frm){
				
	},
	custom_duty_percentage:function(frm){
		frm.set_value("custom_duty_amount",frm.doc.base_total*(frm.doc.custom_duty_percentage/100));
		frm.refresh_field("custom_duty_amount");
	},
	import_duty_percentage:function(frm){
		frm.set_value("import_duty_amount",frm.doc.base_total*(frm.doc.import_duty_percentage/100));
		frm.refresh_field("import_duty_amount");
	},
	validate:function(frm,cdt,cdn){
		frm.set_value("import_and_custom",(frm.doc.import_duty_amount+frm.doc.custom_duty_amount));
		
		if(frm.doc.conversion_rate>0){
		$.each(frm.doc.supplier_data_table, function (i, cd) {
			cd.rate_inr = (cd.rate*frm.doc.conversion_rate)
			cd.amount_inr = (cd.amount*frm.doc.conversion_rate)
		})
		$.each(frm.doc.combined_table, function (i, cd) {
			cd.rate_inr = (cd.rate2*frm.doc.conversion_rate)
			cd.amount_inr = (cd.amount2*frm.doc.conversion_rate)
		})
		}
	},
	before_save:function(frm){		
		var r1=frm.doc.combined_table
		if(r1.length == 0){
			frm.clear_table("combined_table");
			frm.refresh_field("combined_table");
			var array=[]
			$.each(frm.doc.supplier_data_table, function (index, vv) {
		        	array.push({
		        		"item_code":vv.item_code,
		        		"description":vv.description,
		        		"item_name":vv.item_name,
		        		"technical_description":vv.technical_description,
		        		"supplier_description":vv.supplier_description,
		        		"mr_qty":vv.mr_qty,
		        		"qty":vv.qty,
		        		"rate":vv.rate,
		        		"amount":vv.amount,
		        		"item_tax_template":vv.item_tax_template,
		        		"uom":vv.uom,
		        		"stock_uom":vv.stock_uom,
		        		"conversion_rate":vv.conversion_rate,
		        		"price_list_rate":vv.price_list_rate,
		        		"discount_percentage":vv.discount_percentage,
		        		"discount_amount":vv.discount_amount
		        	})
				});
			// alert(array)
			for(var i in array){
			var child = frm.add_child("combined_table");
			frappe.model.set_value(child.doctype, child.name, "item_code", array[i].item_code);
			frappe.model.set_value(child.doctype, child.name, "description", array[i].description);
			frappe.model.set_value(child.doctype, child.name, "technical_description", array[i].technical_description);
			frappe.model.set_value(child.doctype, child.name, "item_name", array[i].item_name);
			frappe.model.set_value(child.doctype, child.name, "supplier_description", array[i].supplier_description);
			frappe.model.set_value(child.doctype, child.name, "mr_qty",array[i].mr_qty);
			frappe.model.set_value(child.doctype, child.name, "qty", array[i].qty);
			frappe.model.set_value(child.doctype, child.name, "price_list_rate2", array[i].price_list_rate);
			frappe.model.set_value(child.doctype, child.name, "discount_percentage2", array[i].discount_percentage);
			frappe.model.set_value(child.doctype, child.name, "discount_amount2", array[i].discount_amount);
			frappe.model.set_value(child.doctype, child.name, "rate2", array[i].rate);
			frappe.model.set_value(child.doctype, child.name, "amount2", array[i].rate * array[i].qty);
			frappe.model.set_value(child.doctype, child.name, "item_tax_template", array[i].item_tax_template);
			frappe.model.set_value(child.doctype, child.name, "uom", array[i].uom);
			frappe.model.set_value(child.doctype, child.name, "stock_uom", array[i].stock_uom);
			frappe.model.set_value(child.doctype, child.name, "conversion_rate", array[i].conversion_rate);
			}
			frm.refresh_field("combined_table");
			
		}
		
	},
	after_save:function(frm,cdt,cdn){
		frappe.call({
			method:"wtt_module.customization.custom.supplier_quotation.set_rate",
			args:{
				name:frm.doc.name
			},
			callback(r){
				frm.reload_doc()
				frm.save()
			}
		})
	},
	// btn1:function(frm,cdt,cdn){
	// 	var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
	// 	htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>S.NO</th><th style='width:2%'>DESCRIPTION</th><th style='width:15%'>TECHNICAL DESCRIPTION</th><th style='text-align:center;width:5%'>MR QTY</th><th style='text-align:center;width:5%'>QTY</th><th style='width:5%'>PRICE RATE</th><th style='width:5%'>DISCOUNT</th><th style='width:5%'>RATE</th><th style='width:5%'>AMOUNT</th></tr>"
	// 	$.each(frm.doc.supplier_data_table || [], function(i, v) {
	// 		var result=''
	// 		var re=''
			
	// 		if(v.technical_description)
	// 		{
	// 		var go=[]
	// 		var val=v.technical_description.split(",")
	// 		var gg='<br>'
	// 		for(var g in val)
	// 		{
	// 			go.push(val[g])
	// 			go.push(gg)
	// 		}
	// 		result = go.toString().replace(/,/g, "");
	// 		}
	// 		if(v.remarks)
	// 		{
	// 			re=v.remarks
	// 		}
	// 		htvalue+='<tr style="text-align:center;"><td align="center">'+v.idx+'.</td><td align="center">'+v.description+'<br></td><td align="left">'+result+'</td><td>'+v.mr_qty+'</td><td>'+v.qty+'</td><td>'+v.price_list_rate+'</td><td>'+v.discount_percentage+'</td><td>'+v.rate+'</td><td>'+v.amount+'</td></tr>'
	// 	});
	// 	$(frm.fields_dict['tab2'].wrapper).html("")
	// 	$(frm.fields_dict['tab3'].wrapper).html("")
	// 	$(frm.fields_dict['tab1'].wrapper).html(htvalue);
	// },
	// btn2:function(frm,cdt,cdn){
	// 	var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
	// 	htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>S.NO</th><th style='width:2%'>DESCRIPTION</th><th style='width:15%'>TECHNICAL DESCRIPTION</th><th style='text-align:center;width:5%'>MR QTY</th><th style='text-align:center;width:5%'>QUOTED QTY</th><th style='width:5%'>PRICE RATE</th><th style='width:5%'>DISCOUNT</th><th style='width:5%'>RATE</th><th style='width:5%'>AMOUNT</th></tr>"
	// 	$.each(frm.doc.combined_table || [], function(i, v) {
	// 		var result=''
	// 		var re=''
			
	// 		if(v.technical_description)
	// 		{
	// 		var go=[]
	// 		var val=v.technical_description.split(",")
	// 		var gg='<br>'
	// 		for(var g in val)
	// 		{
	// 			go.push(val[g])
	// 			go.push(gg)
	// 		}
	// 		result = go.toString().replace(/,/g, "");
	// 		}
	// 		if(v.remarks)
	// 		{
	// 			re=v.remarks
	// 		}
	// 		htvalue+='<tr style="text-align:center;"><td align="center">'+v.idx+'.</td><td align="center">'+v.description+'<br></td><td align="left">'+result+'</td><td>'+v.mr_qty+'</td><td>'+v.qty+'</td><td>'+v.price_list_rate2+'</td><td>'+v.discount_percentage2+'</td><td>'+v.rate2+'</td><td>'+v.amount2+'</td></tr>'
	// 	});
	// 	$(frm.fields_dict['tab1'].wrapper).html("")
	// 	$(frm.fields_dict['tab3'].wrapper).html("")
	// 	$(frm.fields_dict['tab2'].wrapper).html(htvalue);
	// },
	// btn3:function(frm,cdt,cdn){
	// 	var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
	// 	htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>S.NO</th><th style='width:2%'>DESCRIPTION</th><th style='width:15%'>TECHNICAL DESCRIPTION</th><th style='text-align:center;width:5%'>MR QTY</th><th style='text-align:center;width:5%'>REQUIRED QTY</th><th style='text-align:center;width:5%'>APPROVED QTY</th><th style='width:5%'>PRICE RATE</th><th style='width:5%'>DISCOUNT</th><th style='width:5%'>RATE</th><th style='width:5%'>AMOUNT</th></tr>"
	// 	$.each(frm.doc.items || [], function(i, v) {
	// 		var result=''
	// 		var re=''
			
	// 		if(v.technical_description)
	// 		{
	// 		var go=[]
	// 		var val=v.technical_description.split(",")
	// 		var gg='<br>'
	// 		for(var g in val)
	// 		{
	// 			go.push(val[g])
	// 			go.push(gg)
	// 		}
	// 		result = go.toString().replace(/,/g, "");
	// 		}
	// 		if(v.remarks)
	// 		{
	// 			re=v.remarks
	// 		}
	// 		htvalue+='<tr style="text-align:center;"><td align="center">'+v.idx+'.</td><td align="center">'+v.description+'<br></td><td align="left">'+result+'</td><td>'+v.mr_qty+'</td><td>'+v.qty+'</td><td>'+v.quoted_qty+'</td><td>'+v.price_list_rate+'</td><td>'+v.discount_percentage+'</td><td>'+v.rate+'</td><td>'+v.amount+'</td></tr>'
	// 	});
	// 	$(frm.fields_dict['tab2'].wrapper).html("")
	// 	$(frm.fields_dict['tab1'].wrapper).html("")
	// 	$(frm.fields_dict['tab3'].wrapper).html(htvalue);
	// },
	// refresh:function(frm,cdt,cdn){
	// 	$(frm.fields_dict['tab2'].wrapper).html("")
	// 	$(frm.fields_dict['tab1'].wrapper).html("")
	// 	$(frm.fields_dict['tab3'].wrapper).html("");

	// }
});

frappe.ui.form.on("Supplier Data Table", {
	rate: function(frm,cdt, cdn){
		var cd = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "amount", (cd.qty*cd.rate));

	},
	qty:function(frm,cdt,cdn){
		var cd = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "amount", (cd.qty*cd.rate));
	},
	amount:function(frm,cdt,cdn){
		calculate_time_and_amount_table1(frm);
	}
});

frappe.ui.form.on("SQ Combined Table", {
	refresh:function(frm){
		const collection = document.getElementsByClassName(".col.grid-static-col.col-xs-3");
		for (let i = 0; i < collection.length; i++) {
		  collection[i].style.height = "fit-content";
		}
	},
	discount_percentage2:function(frm,cdt,cdn){
		var cd = locals[cdt][cdn];
		var amt=(cd.discount_percentage2/100)*cd.price_list_rate2
		if(cd.descount_percentage2>100){
		frappe.model.set_value(cdt, cdn, "discount_percentage2",100)
		}
		frappe.model.set_value(cdt, cdn, "discount_amount2",amt);
		frappe.model.set_value(cdt,cdn,"rate2",cd.price_list_rate2-amt)
		frappe.model.set_value(cdt,cdn,"amount2",cd.qty*(cd.price_list_rate2-amt))
	},
	price_list_rate2:function(frm,cdt,cdn){
		var cd = locals[cdt][cdn];
		var amt=(cd.discount_percentage2/100)*cd.price_list_rate2
		if(cd.descount_percentage2>100){
		frappe.model.set_value(cdt, cdn, "discount_percentage2",100)
		}
		frappe.model.set_value(cdt, cdn, "discount_amount2",amt);
		frappe.model.set_value(cdt,cdn,"rate2",cd.price_list_rate2-amt)
		frappe.model.set_value(cdt,cdn,"amount2",cd.qty*(cd.price_list_rate2-amt))
		if(frm.doc.conversion_rate>0){
			frappe.model.set_value(cdt, cdn, "rate_inr", ((cd.price_list_rate2-amt)*frm.doc.conversion_rate));
			frappe.model.set_value(cdt, cdn, "amount_inr", (((cd.price_list_rate2-amt)*frm.doc.conversion_rate)*cd.qty));
		}
	},

	rate2: function(frm,cdt, cdn){
		var cd = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "amount2", (cd.qty*cd.rate2));
		if(frm.doc.conversion_rate>0){
			frappe.model.set_value(cdt, cdn, "rate_inr", (cd.rate2*frm.doc.conversion_rate));
			frappe.model.set_value(cdt, cdn, "amount_inr", ((cd.rate2*frm.doc.conversion_rate)*cd.qty));
		}
		
	},
	qty:function(frm,cdt,cdn){
		var cd = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "amount2", (cd.qty*cd.rate2));
		frappe.model.set_value(cdt, cdn, "amount_inr", (cd.qty*cd.rate2)*frm.doc.conversion_rate);
	},
	amount2:function(frm,cdt,cdn){
		calculate_time_and_amount(frm);
	}
});

frappe.ui.form.on("Supplier Quotation Item", {
	rate:function(frm,cdt,cdn){
		var cd = locals[cdt][cdn];
		if(frm.doc.conversion_rate){
			frappe.model.set_value(cdt, cdn, "rate_inr", (cd.rate2*frm.doc.conversion_rate));
			frappe.model.set_value(cdt, cdn, "amount_inr", ((cd.rate2*frm.doc.conversion_rate)*cd.qty));
		}
		// else
	},
	uom_rate: function(frm,cdt, cdn){
		calculate_total(frm, cdt, cdn);
	}
});

var calculate_total = function(frm, cdt, cdn) {
	var child = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "rate", ((child.stock_qty/child.qty)*child.uom_rate));
	}
var calculate_time_and_amount = function(frm) {
var temp = frm.doc.combined_table;
var i,sum=0
for(i=0;i<temp.length;i++)
{
sum+=temp[i].amount2;
}
frm.set_value("supplier_total",sum);
};

var calculate_time_and_amount_table1 = function(frm) {
var temp = frm.doc.supplier_data_table;
var i,sum=0
for(i=0;i<temp.length;i++)
{
sum+=temp[i].amount;
}
frm.set_value("supplier_total2",sum);
};
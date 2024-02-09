// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Service Request', {
	refresh:function(frm){
		frm.set_df_property('hide', 'hidden', 1);
		frm.set_df_property('preview', 'hidden', 0);
		$(frm.fields_dict['html'].wrapper).html("");
	},
	setup: function(frm) {
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


		frm.set_query("project", function() {
			return {
				filters: [
					["Project","status", "!=", "Open"],
					["Project","status", "!=", "Cancelled"]					
				]
			};
		});

		frm.set_query("project", "items", function() {
		    return {
				filters: [
					["Project","status", "!=", "Open"],
					["Project","status", "!=", "Cancelled"]
				]
			};
		});
	},
	hide: function(frm,cdt,cdn){
		frm.set_df_property('hide', 'hidden', 1);
		frm.set_df_property('preview', 'hidden', 0);
		$(frm.fields_dict['html'].wrapper).html("");
	},
	preview:function(frm,cdt,cdn){
		frm.set_df_property('hide', 'hidden', 0);
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
		$(frm.fields_dict['html'].wrapper).html(htvalue);
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
	set_warehouse: function(frm) {
	$.each(frm.doc.items || [], function(i, d) {
	d.warehouse = frm.doc.set_warehouse;
	});
	refresh_field("warehouse");
	}

});

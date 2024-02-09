// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Work Updates', {
	hide_table: function(frm,cdt,cdn){
		$(frm.fields_dict['item_table'].wrapper).html("");
	},
	preview:function(frm,cdt,cdn){
		var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
		var hr=''
		var re=''
		htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>S.NO</th><th style='width:2%'>TASK NAME</th><th style='width:15%'>DESCRIPTION</th><th style='text-align:center;width:5%'>TARGET DATE</th><th style='width:8%'>HOURS</th><th style='width:8%'>STATUS</th><th style='width:8%'>REMARKS</th></tr>"
		$.each(frm.doc.virtual_table || [], function(i, v) {
			if(v.target_time)
			{
				hr=v.target_time
			}
			else
			{
				hr='-'
			}
			if(v.remarks)
			{
				re=v.remarks
			}
			else
			{
				re='-'
			}
			htvalue+='<tr style="text-align:center;"><td align="center">'+v.idx+'.</td><td align="center">'+v.task_name+'<br></td><td align="left">'+v.description+'</td><td>'+v.target_date+'</td><td>'+hr+'</td><td>'+v.status+'</td><td>'+re+'</td></tr>'
		});
		$(frm.fields_dict['item_table'].wrapper).html(htvalue);
	},
	refresh: function(frm) {
		$(frm.fields_dict['item_table'].wrapper).html("");
	}
});

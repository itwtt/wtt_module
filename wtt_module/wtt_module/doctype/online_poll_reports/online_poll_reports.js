// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Online Poll Reports', {
	// refresh: function(frm) {

	// }
	get_data:function(frm){
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.online_poll_reports.online_poll_reports.poll_report',
			args: { 
				aa:frm.doc.name
			},
			callback: function(r) {
				var ar1=[];
				var ar2=[];
				var htvalue='<style>th{font-size: 15px;text-align:center;color:Red;}</style>'
				htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:2%'>NAME</th><th style='width:5%'>SMARTPHONES</th><th style='width:5%'>REASON</th></tr>"
				var htvalue1='<style>th{font-size: 15px;text-align:center;color:Green;}</style>'
				htvalue1+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:2%'>NAME</th><th style='width:5%'>SMARTPHONES</th><th style='width:5%'>REASON</th></tr>"
				for(var i=0;i<r.message.length;i++){
				
				

				if(r.message[i]["mob"]=='Can be Allowed'){
				ar1.push(r.message[i]["emp"])
				htvalue+='<tr style="text-align:center;"><td align="center">'+r.message[i]["emp"]+'.</td><td align="center">'+r.message[i]["mob"]+'<br></td><td align="center">'+r.message[i]["sug"]+'</td></tr>'
				}
				else if(r.message[i]["mob"]=='Can be Restricted'){
				ar2.push(r.message[i]["emp"])
				htvalue1+='<tr style="text-align:center;"><td align="center">'+r.message[i]["emp"]+'.</td><td align="center">'+r.message[i]["mob"]+'<br></td><td align="center">'+r.message[i]["sug"]+'</td></tr>'
				}

				}
				// frm.doc.set_value("to_allow",ar1.length)
				frm.set_value("to_allow",ar1.length);
				frm.set_value("to_restrict",ar2.length);

				$(frm.fields_dict['html_2'].wrapper).html(htvalue);
				$(frm.fields_dict['html_3'].wrapper).html(htvalue1);
				}
			
		});
	}
});

// Copyright (c) 2021, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Query Reply', {
	// replay:function(frm){
	// 	var arr=[]
	// 	arr.push(frm.doc.html)
	// 	arr.push(frm.doc.employee +": "+ frm.doc.replay)
	// 	for(let i=0;i<arr.length;i++){
	// 		var ht="<br>"+arr[i]+"<br>"
	// 		frm.set_value("html",ht)
	// 		frm.set_value('employee', '')
	// 		frm.set_value('employee_name', '')
	// 		frm.set_value('department', '')
	// 		frm.set_value('replay', '')
	// 	}
		
	// }
	replay_button:function(frm){
		var emp=[]
		var arr=[]

		arr.push(frm.doc.html)
		arr.push(frm.doc.employee_name +" : "+ frm.doc.replay)
		var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
		htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>Replay</th></tr>"
		for(let i=0;i<arr.length;i++){
		if(arr[i]!=undefined)
		{
		var child = frm.add_child("reply_table");
		frappe.model.set_value(child.doctype, child.name, "reply", arr[i]);
		
		frm.refresh_field("reply_table");
		}
		}
		//$(frm.fields_dict['html'].wrapper).html(htvalue);
		frm.set_value('employee', '')
		frm.set_value('employee_name', '')
		frm.set_value('department', '')
		frm.set_value('replay', '')
		
		// for(let i=0;i<arr.length;i++){
		// 	var ht="<br>"+arr[i]+"<br>"
		// 	//frm.set_value("html",ht)
		// 	frm.set_value('employee', '')
		// 	frm.set_value('employee_name', '')
		// 	frm.set_value('department', '')
		// 	frm.set_value('replay', '')
		// }
		
	}
});

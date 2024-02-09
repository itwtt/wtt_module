// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Kaizen', {
	after_workflow_action:function(frm){
		if(frm.doc.workflow_state=='Accepted'){
			frm.set_value("points",2);
			frm.set_value("status","Waiting for Kaizen Review");
			frm.save()
		}
		else if(frm.doc.workflow_state=='Appreciated'){
			if(frm.doc.points>1){
				if(frappe.session.user=='venkat@wttindia.com'){
					frm.set_value("status","Denied by MD");	
				}
				else{
					frm.set_value("status","Denied by Evalution Team");				
				}
			}
			else{
				frm.set_value("points",1);
				frm.set_value("status","Appreciated for Idea");		
			}
			frm.save()
			
		}
		else if(frm.doc.workflow_state=='Verified'){
			frm.set_value("points",5);
			frm.set_value("status","Waiting for MD Approval");
			frm.save()
		}
		
		else if(frm.doc.workflow_state=='Withheld'){
			var d = new frappe.ui.Dialog({
				'fields': [
				{"fieldtype": "Select",
				"label":"Waiting for",
				"fieldname": "waiting_for",
				"options":["Explanation","Modification","Development","Cost Calculation"]
				}
				],
				primary_action: function(values){ 
					frm.set_value("waiting_for",values.waiting_for);
					frm.refresh_field("waiting_for")				;
					frm.set_df_property("waiting_for","read_only",0);
					frm.set_df_property("remarks","read_only",0);
					frm.set_value("status","Withheld by Evalution Team");
					d.hide();
					frm.save();
				}
				});
				d.show();
				}

	},

	refresh: function(frm) {
		if(frm.doc.workflow_state=='Withheld'){
			frm.set_df_property("waiting_for","read_only",0);
			frm.set_df_property("remarks","read_only",0);
		}
		else{
			frm.set_df_property("waiting_for","hidden",1);
		}
		// $(frm.fields_dict['ht'].wrapper).html("")
		// $(frm.fields_dict['ht2'].wrapper).html("")
		frm.set_df_property("evaluation","hidden",1)
		frm.set_df_property("hide","hidden",1)
		var ar=["mythili@wtt.com","edp@wttindia.com","ragavendhiran@wtt.com","dhanalakshmi@wtt1370.com"]
		if(ar.includes(frappe.session.user)){
			frm.set_df_property('reason', 'read_only', 0);
		}
		
	// },
	// evaluation:function(frm){
		// frm.set_df_property("evaluation","hidden",1)
		// frm.set_df_property("hide","hidden",0)
		if(frm.doc.workflow_state=='Withheld' || frm.doc.workflow_state=='Accepted' || frm.doc.workflow_state=='Verified'){
			
		frappe.call({
			method:"wtt_module.wtt_module.doctype.kaizen.kaizen.evaluation",
			args:{
				name:frm.doc.evaluation_process
			},
			callback(r){
				var htvalue='<style>th{font-size: 12px;text-align:center;color:#6A5ACD;}</style>'
				htvalue+="<h3>EVALUATION TEAM REMARKS</h3><table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:5%;'>EVALUATOR</th><th style='width:5%;'>PRACTICALLY POSSIBLE</th><th style='width:5%;'>TIME REDUCTION</th><th style='width:5%;'>COST REDUCTION</th><th style='width:5%;'>EFFORT REDUCTION</th><th style='width:5%;'>QUALITY IMPROVEMENT</th><th style='width:5%;'>CUSTOMER SATISFACTION</th><th style='width:5%;'>VALUE PROPORTION</th><th style='width:5%;'>SAFETY</th><th style='width:5%;'>CAN BE APPROVED</th><th style='width:5%;'>EXPLANATION NEEDED</th><th style='width:5%;'>MODIFICATION NEEDED</th><th style='width:5%;'>CANT BE APPROVED</th></tr>"
				$.each(r.message[0] || [], function(i, v) {
					var a1="";
					var a2="";
					var a3="";
					var a4="";
					var a5="";
					var a6="";
					var a7="";
					var a8="";
					var a9="";
					var a10="";
					var a11="";
					var a12="";
					var a13="";
					var a14="";
					var a15="";
					var a16="";
					if(v.yes1==1){
						a1="Yes"
					}
					else if(v.no1==1){
						a1="No"
					}
					else{
						a1="-"
					}
					if(v.yes2==1){
						a2="Yes"
					}
					else if(v.no2==1){
						a2="No"
					}
					else{
						a2="-"
					}
					if(v.yes3==1){
						a3="Yes"
					}
					else if(v.no3==1){
						a3="No"
					}
					else{
						a3="-"
					}
					if(v.yes4==1){
						a4="Yes"
					}
					else if(v.no4==1){
						a4="No"
					}
					else{
						a4="-"
					}
					if(v.yes5==1){
						a5="Yes"
					}
					else if(v.no5==1){
						a5="No"
					}
					else{
						a5="-"
					}
					if(v.yes10==1){
						a14="Yes"
					}
					else if(v.no10==1){
						a14="No"
					}
					else{
						a14="-"
					}
					if(v.yes11==1){
						a15="Yes"
					}
					else if(v.no11==1){
						a15="No"
					}
					else{
						a15="-"
					}
					if(v.yes12==1){
						a16="Yes"
					}
					else if(v.no12==1){
						a16="No"
					}
					else{
						a16="-"
					}
					if(v.can_be_approved!=undefined){
						a6=v.can_be_approved
					}
					if(v.explanation_needed!=undefined){
						a7=v.explanation_needed
					}
					if(v.modification_needed!=undefined){
						a8=v.modification_needed
					}
					if(v.cant_be_approved!=undefined){
						a9=v.cant_be_approved
					}
					if(v.yes6==1){
						a10="Yes"
					}
					else{
						a10="No"
					}
					if(v.yes7==1){
						a11="Yes"
					}
					else{
						a11="No"
					}
					if(v.yes8==1){
						a12="Yes"
					}
					else{
						a12="No"
					}
					if(v.yes9==1){
						a13="Yes"
					}
					else{
						a13="No"
					}
					htvalue+='<tr style="text-align:center;"><td align="center">'+v.employee_name+'<br></td><td align="center">'+a1+'<br></td><td align="center">'+a3+'<br></td><td align="center">'+a2+'<br></td><td align="center">'+a4+'<br></td><td align="center">'+a5+'<br></td><td align="center">'+a14+'<br></td><td align="center">'+a15+'<br></td><td align="center">'+a16+'<br></td><td align="center">'+a10+',<br>'+a6+'<br></td><td align="center">'+a11+',<br>'+a7+'<br></td><td align="center">'+a12+',<br>'+a8+'<br></td><td align="center">'+a13+',<br>'+a9+'<br></td></tr>'
				})
				htvalue+="</table><br>"
				var htvalue2='<style>th{font-size: 12px;text-align:center;color:#6A5ACD;}</style>'
				htvalue2+="<h3>KAIZEN TEAM REMARKS</h3><table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:5%;'>EVALUATOR</th><th style='width:5%;'>PRACTICALLY POSSIBLE</th><th style='width:5%;'>TIME REDUCTION</th><th style='width:5%;'>COST REDUCTION</th><th style='width:5%;'>EFFORT REDUCTION</th><th style='width:5%;'>QUALITY IMPROVEMENT</th><th style='width:5%;'>CUSTOMER SATISFACTION</th><th style='width:5%;'>VALUE PROPORTION</th><th style='width:5%;'>SAFETY</th><th style='width:5%;'>CAN BE APPROVED</th><th style='width:5%;'>EXPLANATION NEEDED</th><th style='width:5%;'>MODIFICATION NEEDED</th><th style='width:5%;'>CANT BE APPROVED</th></tr>"
				$.each(r.message[1] || [], function(i, v) {
					var a1="";
					var a2="";
					var a3="";
					var a4="";
					var a5="";
					var a6=""					;
					var a7="";
					var a8="";
					var a9="";
					var a10="";
					var a11="";
					var a12="";
					var a12="";
					var a10="";
					var a11="";
					var a12="";
					var a13="";
					var a14="";
					var a15="";
					var a16="";
					if(v.yes1==1){
						a1="Yes"
					}
					else if(v.no1==1){
						a1="No"
					}
					else{
						a1="-"
					}
					if(v.yes2==1){
						a2="Yes"
					}
					else if(v.no2==1){
						a2="No"
					}
					else{
						a2="-"
					}
					if(v.yes3==1){
						a3="Yes"
					}
					else if(v.no3==1){
						a3="No"
					}
					else{
						a3="-"
					}
					if(v.yes4==1){
						a4="Yes"
					}
					else if(v.no4==1){
						a4="No"
					}
					else{
						a4="-"
					}
					if(v.yes5==1){
						a5="Yes"
					}
					else if(v.no5==1){
						a5="No"
					}
					else{
						a5="-"
					}
					if(v.yes10==1){
						a14="Yes"
					}
					else if(v.no10==1){
						a14="No"
					}
					else{
						a14="-"
					}
					if(v.yes11==1){
						a15="Yes"
					}
					else if(v.no11==1){
						a15="No"
					}
					else{
						a15="-"
					}
					if(v.yes12==1){
						a16="Yes"
					}
					else if(v.no12==1){
						a16="No"
					}
					else{
						a16="-"
					}
					if(v.can_be_approved!=undefined){
						a6=v.can_be_approved
					}
					if(v.explanation_needed!=undefined){
						a7=v.explanation_needed
					}
					if(v.modification_needed!=undefined){
						a8=v.modification_needed
					}
					if(v.cant_be_approved!=undefined){
						a9=v.cant_be_approved
					}
					if(v.yes6==1){
						a10="Yes"
					}
					else{
						a10="No"
					}
					if(v.yes7==1){
						a11="Yes"
					}
					else{
						a11="No"
					}
					if(v.yes8==1){
						a12="Yes"
					}
					else{
						a12="No"
					}
					if(v.yes9==1){
						a13="Yes"
					}
					else{
						a13="No"
					}
					htvalue2+='<tr style="text-align:center;"><td align="center">'+v.employee_name+'<br></td><td align="center">'+a1+'<br></td><td align="center">'+a3+'<br></td><td align="center">'+a2+'<br></td><td align="center">'+a4+'<br></td><td align="center">'+a5+'<br></td><td align="center">'+a14+'<br></td><td align="center">'+a15+'<br></td><td align="center">'+a16+'<br></td><td align="center">'+a10+',<br>'+a6+'<br></td><td align="center">'+a11+',<br>'+a7+'<br></td><td align="center">'+a12+',<br>'+a8+'<br></td><td align="center">'+a13+',<br>'+a9+'<br></td></tr>'
				})
				htvalue2+="</table><br>"
				$(frm.fields_dict['ht'].wrapper).html(htvalue)
				$(frm.fields_dict['ht2'].wrapper).html(htvalue2)
			
				
			}

		})
		}
		else{
				$(frm.fields_dict['ht'].wrapper).html("")
				$(frm.fields_dict['ht2'].wrapper).html("")
			}
		
	},
	// hide:function(frm){
	// 	frm.set_df_property("hide","hidden",1)
	// 	frm.set_df_property("evaluation","hidden",0)
	// 	$(frm.fields_dict['ht'].wrapper).html("")
	// 	$(frm.fields_dict['ht2'].wrapper).html("")
	// }
});

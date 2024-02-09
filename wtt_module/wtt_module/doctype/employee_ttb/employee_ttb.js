// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee TTB', {
	get_criteria:function(frm,cdt,dcn){
		
		frappe.call({
			method:"wtt_module.wtt_module.doctype.employee_ttb.employee_ttb.get_score",
			args:{
				"val":frm.doc.name
			},
			callback:function(r){
				
				for(var i=0;i<r.message.length;i++){
					var child = frm.add_child("attitude");
					frappe.model.set_value(child.doctype, child.name, "employee", r.message[i].employee);
					frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[i].employee_name);
					frm.refresh_field("attitude");

					var child = frm.add_child("personal");
					frappe.model.set_value(child.doctype, child.name, "employee", r.message[i].employee);
					frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[i].employee_name);
					frm.refresh_field("personal");

					var child = frm.add_child("skill");
					frappe.model.set_value(child.doctype, child.name, "employee", r.message[i].employee);
					frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[i].employee_name);
					frm.refresh_field("skill");

					var child = frm.add_child("team");
					frappe.model.set_value(child.doctype, child.name, "employee", r.message[i].employee);
					frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[i].employee_name);
					frm.refresh_field("team");

					var child = frm.add_child("work_knowledge");
					frappe.model.set_value(child.doctype, child.name, "employee", r.message[i].employee);
					frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[i].employee_name);
					frm.refresh_field("work_knowledge");

					var child = frm.add_child("work_performance");
					frappe.model.set_value(child.doctype, child.name, "employee", r.message[i].employee);
					frappe.model.set_value(child.doctype, child.name, "employee_name", r.message[i].employee_name);
					frm.refresh_field("work_performance");

				
				}
			}
		});
		frm.set_df_property("btn1","hidden",0);
		frm.set_df_property("btn2","hidden",0);
		frm.set_df_property("btn3","hidden",0);
		frm.set_df_property("btn4","hidden",0);
		frm.set_df_property("btn5","hidden",0);
		frm.set_df_property("btn6","hidden",0);

	},
	btn1:function(frm,cdt,cdn){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.employee_ttb.employee_ttb.get_attitude_score",
			args:{
				"val":frm.doc.name
			},
			callback:function(r){
					
				for(var i=0;i<r.message.length;i++){
					
					var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
					htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:5%'>NAME</th><th style='width:5%'>Anger Management</th><th style='width:5%'>Goal Oriented</th><th style='width:5%'>Initiative</th><th style='width:5%'>Positivity</th><th style='width:5%'>Responsible</th><th style='width:5%'>Humour</th></tr>"
					
					$.each(r.message, function(i, v) {
					
					htvalue+='<tr style="text-align:center;"><td align="center">'+v.employee_name+'<br></td><td align="center">'+v.anger_management+'<br></td><td align="center">'+v.goal_oriented+'</td><td align="center">'+v.initiative+'</td><td align="center">'+v.positivity+'</td><td>'+v.responsible+'</td><td>'+v.sense_of_humour+'</td></tr>'
					});
					$(frm.fields_dict['html1'].wrapper).html(htvalue)					
					}
			}
		});
		frm.set_df_property("btn1","hidden",1);
		frm.set_df_property("hide1","hidden",0);
	},
	hide1:function(frm,cdt,cdn){
		$(frm.fields_dict['html1'].wrapper).html("")
		frm.set_df_property("btn1","hidden",0);
		frm.set_df_property("hide1","hidden",1);
	},
	btn2:function(frm,cdt,cdn){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.employee_ttb.employee_ttb.get_personal_score",
			args:{
				"val":frm.doc.name
			},
			callback:function(r){
					
				for(var i=0;i<r.message.length;i++){
					
					var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
					htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:5%'>NAME</th><th style='width:5%'>Discipline</th><th style='width:5%'>Hygiene</th><th style='width:5%'>Professional Attire</th></tr>"
					
					$.each(r.message, function(i, v) {
					
					htvalue+='<tr style="text-align:center;"><td align="center">'+v.employee_name+'<br></td><td align="center">'+v.discipline+'<br></td><td align="center">'+v.hygiene+'</td><td align="center">'+v.attire+'</td></tr>'
					});
					$(frm.fields_dict['html2'].wrapper).html(htvalue)					
					}
			}
		});
		frm.set_df_property("btn2","hidden",1);
		frm.set_df_property("hide2","hidden",0);
	},
	hide2:function(frm,cdt,cdn){
		$(frm.fields_dict['html2'].wrapper).html("")
		frm.set_df_property("btn2","hidden",0);
		frm.set_df_property("hide2","hidden",1);
	},
	btn3:function(frm,cdt,cdn){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.employee_ttb.employee_ttb.get_skill_score",
			args:{
				"val":frm.doc.name
			},
			callback:function(r){
					
				for(var i=0;i<r.message.length;i++){
					
					var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
					htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:5%'>NAME</th><th style='width:5%'>Analytical</th><th style='width:5%'>Appreciation</th><th style='width:5%'>Consistancy</th><th style='width:5%'>Creativity</th><th style='width:5%'>Focus</th><th style='width:5%'>Language</th><th style='width:5%'>Organized Working</th><th style='width:5%'>Proactiveness</th><th style='width:5%'>Time Management</th></tr>"
					
					$.each(r.message, function(i, v) {
					
					htvalue+='<tr style="text-align:center;"><td align="center">'+v.employee_name+'<br></td><td align="center">'+v.a1+'<br></td><td align="center">'+v.a2+'</td><td align="center">'+v.a3+'</td><td align="center">'+v.a4+'</td><td align="center">'+v.a5+'</td><td align="center">'+v.a6+'</td><td align="center">'+v.a7+'</td><td align="center">'+v.a8+'</td><td align="center">'+v.a9+'</td></tr>'
					});
					$(frm.fields_dict['html3'].wrapper).html(htvalue)					
					}
			}
		});
		frm.set_df_property("btn3","hidden",1);
		frm.set_df_property("hide3","hidden",0);
	},
	hide3:function(frm,cdt,cdn){
		$(frm.fields_dict['html3'].wrapper).html("")
		frm.set_df_property("btn3","hidden",0);
		frm.set_df_property("hide3","hidden",1);
	},
	btn4:function(frm,cdt,cdn){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.employee_ttb.employee_ttb.get_team_score",
			args:{
				"val":frm.doc.name
			},
			callback:function(r){
					
				for(var i=0;i<r.message.length;i++){
					
					var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
					htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:5%'>NAME</th><th style='width:5%'>Caring Team Members</th><th style='width:5%'>Commanding</th><th style='width:5%'>Ego Balancing</th><th style='width:5%'>Feedback in Team</th><th style='width:5%'>Leadership</th><th style='width:5%'>Participation</th><th style='width:5%'>Relationship Maintenance</th></tr>"
					
					$.each(r.message, function(i, v) {
					
					htvalue+='<tr style="text-align:center;"><td align="center">'+v.employee_name+'<br></td><td align="center">'+v.a1+'<br></td><td align="center">'+v.a2+'</td><td align="center">'+v.a3+'</td><td align="center">'+v.a4+'</td><td align="center">'+v.a5+'</td><td align="center">'+v.a6+'</td><td align="center">'+v.a7+'</td></tr>'
					});
					$(frm.fields_dict['html4'].wrapper).html(htvalue)					
					}
			}
		});
		frm.set_df_property("btn4","hidden",1);
		frm.set_df_property("hide4","hidden",0);
	},
	hide4:function(frm,cdt,cdn){
		$(frm.fields_dict['html4'].wrapper).html("")
		frm.set_df_property("btn4","hidden",0);
		frm.set_df_property("hide4","hidden",1);
	},
	btn5:function(frm,cdt,cdn){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.employee_ttb.employee_ttb.get_knowledge_score",
			args:{
				"val":frm.doc.name
			},
			callback:function(r){
					
				for(var i=0;i<r.message.length;i++){
					
					var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
					htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:5%'>NAME</th><th style='width:5%'>Involvement</th><th style='width:5%'>Learning Curve</th><th style='width:5%'>Update In Field</th></tr>"
					
					$.each(r.message, function(i, v) {
					
					htvalue+='<tr style="text-align:center;"><td align="center">'+v.employee_name+'<br></td><td align="center">'+v.a1+'<br></td><td align="center">'+v.a2+'</td><td align="center">'+v.a3+'</td></tr>'
					});
					$(frm.fields_dict['html5'].wrapper).html(htvalue)					
					}
			}
		});
		frm.set_df_property("btn5","hidden",1);
		frm.set_df_property("hide5","hidden",0);
	},
	hide5:function(frm,cdt,cdn){
		$(frm.fields_dict['html5'].wrapper).html("")
		frm.set_df_property("btn5","hidden",0);
		frm.set_df_property("hide5","hidden",1);
	},
	btn6:function(frm,cdt,cdn){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.employee_ttb.employee_ttb.get_knowledge_score",
			args:{
				"val":frm.doc.name
			},
			callback:function(r){
					
				for(var i=0;i<r.message.length;i++){
					
					var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
					htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:5%'>NAME</th><th style='width:5%'>Involvement</th><th style='width:5%'>Learning Curve</th><th style='width:5%'>Update In Field</th></tr>"
					
					$.each(r.message, function(i, v) {
					
					htvalue+='<tr style="text-align:center;"><td align="center">'+v.employee_name+'<br></td><td align="center">'+v.a1+'<br></td><td align="center">'+v.a2+'</td><td align="center">'+v.a3+'</td></tr>'
					});
					$(frm.fields_dict['html6'].wrapper).html(htvalue)					
					}
			}
		});
		frm.set_df_property("btn6","hidden",1);
		frm.set_df_property("hide6","hidden",0);
	},
	hide6:function(frm,cdt,cdn){
		$(frm.fields_dict['html6'].wrapper).html("")
		frm.set_df_property("btn6","hidden",0);
		frm.set_df_property("hide6","hidden",1);
	},
	btn6:function(frm,cdt,cdn){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.employee_ttb.employee_ttb.get_knowledge_score",
			args:{
				"val":frm.doc.name
			},
			callback:function(r){
					
				for(var i=0;i<r.message.length;i++){
					
					var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
					htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:5%'>NAME</th><th style='width:5%'>Attendance</th><th style='width:5%'>Punctuality</th><th style='width:5%'>Reporting</th><th style='width:5%'>Result Driven</th><th style='width:5%'>Safety</th></tr>"
					
					$.each(r.message, function(i, v) {
					
					htvalue+='<tr style="text-align:center;"><td align="center">'+v.employee_name+'<br></td><td align="center">'+v.a1+'<br></td><td align="center">'+v.a2+'</td><td align="center">'+v.a3+'</td><td align="center">'+v.a4+'</td><td align="center">'+v.a5+'</td></tr>'
					});
					$(frm.fields_dict['html6'].wrapper).html(htvalue)					
					}
			}
		});
		frm.set_df_property("btn6","hidden",1);
		frm.set_df_property("hide6","hidden",0);
	},
	hide6:function(frm,cdt,cdn){
		$(frm.fields_dict['html6'].wrapper).html("")
		frm.set_df_property("btn6","hidden",0);
		frm.set_df_property("hide6","hidden",1);
	},
});

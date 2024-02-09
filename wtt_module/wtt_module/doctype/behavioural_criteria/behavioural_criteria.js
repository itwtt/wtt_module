// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Behavioural Criteria', {
	setup: function(frm,cdt,cdn) {
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status","=", 'Active']
				]
			}

		});
		frm.set_query("hod_id", function() {
			return {
				filters: [
					["Employee","status","=", 'Active']
				]
			}

		});
		var hidebtn1 = $('*[data-fieldname="attitude"]');
		var hidebtn2 = $('*[data-fieldname="personal"]');
		var hidebtn3 = $('*[data-fieldname="skill"]');
		var hidebtn4 = $('*[data-fieldname="team"]');
		var hidebtn5 = $('*[data-fieldname="work_performance"]');
		var hidebtn6 = $('*[data-fieldname="work_knowledge"]');

			hidebtn1 .find('.grid-add-row').hide();
			hidebtn1 .find('.grid-remove-rows').hide();

			hidebtn2 .find('.grid-add-row').hide();
			hidebtn2 .find('.grid-remove-rows').hide();

			hidebtn3 .find('.grid-add-row').hide();
			hidebtn3 .find('.grid-remove-rows').hide();

			hidebtn4 .find('.grid-add-row').hide();
			hidebtn4 .find('.grid-remove-rows').hide();

			hidebtn5 .find('.grid-add-row').hide();
			hidebtn5 .find('.grid-remove-rows').hide();

			hidebtn6 .find('.grid-add-row').hide();
			hidebtn6 .find('.grid-remove-rows').hide();

		
	},
	employee: function(frm) {
		var arr=["Anger Management","Goal Oriented","Initiative","Positivity","Responsible","Sense of Humour"]
		var arr1=["Discipline (Healthy practises)","Hygiene","Professional Attire"]
		var arr2=["Analytical","Appreciation","Consistancy","Creativity","Focus","Language","Organized working","Proactiveness","Time Management"]
		var arr3=["Caring Team Members","Commanding","Ego Balancing","Feed back in team","Leadership","Participation","Relationship Maintenance"]
		var arr4=["Attendance","Punctuality","Reporting","Result Driven","Safety"]
		var arr5=["Involvement","Learning Curve","Update in Field"]
		frm.clear_table("attitude")
		frm.clear_table("personal");
		frm.clear_table("skill")
		frm.clear_table("team");
		frm.clear_table("work_performance")
		frm.clear_table("work_knowledge");
		for (let i = 0; i < arr.length; i++) {			
			var child = frm.add_child("attitude");
			frappe.model.set_value(child.doctype, child.name, "criteria", arr[i])
			frm.refresh_field("attitude")
		};
		for (var i=0;i<arr1.length;i++){
			var child=frm.add_child("personal");
			frappe.model.set_value(child.doctype,child.name,"criteria",arr1[i])
			frm.refresh_field("personal")
		};
		for (var i=0;i<arr2.length;i++){
			var child=frm.add_child("skill");
			frappe.model.set_value(child.doctype,child.name,'criteria',arr2[i])
			frm.refresh_field('skill');
		};
		for (let i = 0; i < arr3.length; i++) {			
			var child = frm.add_child("team");
			frappe.model.set_value(child.doctype, child.name, "criteria", arr3[i])
			frm.refresh_field("team")
		};
		for (var i=0;i<arr4.length;i++){
			var child=frm.add_child("work_performance");
			frappe.model.set_value(child.doctype,child.name,"criteria",arr4[i])
			frm.refresh_field("work_performance")
		};
		for (var i=0;i<arr5.length;i++){
			var child=frm.add_child("work_knowledge");
			frappe.model.set_value(child.doctype,child.name,'criteria',arr5[i])
			frm.refresh_field('work_knowledge');
		};
	},
	refresh:function(frm){
		
		var hidebtn1 = $('*[data-fieldname="attitude"]');
		var hidebtn2 = $('*[data-fieldname="personal"]');
		var hidebtn3 = $('*[data-fieldname="skill"]');
		var hidebtn4 = $('*[data-fieldname="team"]');
		var hidebtn5 = $('*[data-fieldname="work_performance"]');
		var hidebtn6 = $('*[data-fieldname="work_knowledge"]');

			hidebtn1 .find('.grid-add-row').hide();
			hidebtn1 .find('.grid-remove-rows').hide();

			hidebtn2 .find('.grid-add-row').hide();
			hidebtn2 .find('.grid-remove-rows').hide();

			hidebtn3 .find('.grid-add-row').hide();
			hidebtn3 .find('.grid-remove-rows').hide();

			hidebtn4 .find('.grid-add-row').hide();
			hidebtn4 .find('.grid-remove-rows').hide();

			hidebtn5 .find('.grid-add-row').hide();
			hidebtn5 .find('.grid-remove-rows').hide();

			hidebtn6 .find('.grid-add-row').hide();
			hidebtn6 .find('.grid-remove-rows').hide();



		// var df1 = frappe.meta.get_docfield("Attitude Table","management_points", frm.doc.name); 
		// var df2 = frappe.meta.get_docfield("Attitude Table","your_points", frm.doc.name);
		// if(frappe.session.user!='Administrator' || frappe.session.user!='managingdirector@wttindia.com'){
		// 	df1.read_only = 1;
		// }
		// if(frappe.session.user=='managingdirector@wttindia.com'){
		// 	df2.read_only = 1;
		// }
	},
	onload:function(frm){
		
		var hidebtn1 = $('*[data-fieldname="attitude"]');
		var hidebtn2 = $('*[data-fieldname="personal"]');
		var hidebtn3 = $('*[data-fieldname="skill"]');
		var hidebtn4 = $('*[data-fieldname="team"]');
		var hidebtn5 = $('*[data-fieldname="work_performance"]');
		var hidebtn6 = $('*[data-fieldname="work_knowledge"]');

			hidebtn1 .find('.grid-add-row').hide();
			hidebtn1 .find('.grid-remove-rows').hide();

			hidebtn2 .find('.grid-add-row').hide();
			hidebtn2 .find('.grid-remove-rows').hide();

			hidebtn3 .find('.grid-add-row').hide();
			hidebtn3 .find('.grid-remove-rows').hide();

			hidebtn4 .find('.grid-add-row').hide();
			hidebtn4 .find('.grid-remove-rows').hide();

			hidebtn5 .find('.grid-add-row').hide();
			hidebtn5 .find('.grid-remove-rows').hide();

			hidebtn6 .find('.grid-add-row').hide();
			hidebtn6 .find('.grid-remove-rows').hide();
	},
	
});
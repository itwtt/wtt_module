// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Kaizen Evaluation Sheet', {
	setup:function(frm){
	frm.set_query("evaluation_by", function() {
		return {
			filters: [
				["Employee","status","=", "Active"],
				["Employee","employee_number","in","WTT1194,WTT1090,WTT912,WTT1211,WTT947,WTT1360,WTT1372,WTT1370"]
			]
		}

	});
	},
	refresh:function(frm){
		var ar1=["WTT1194","WTT1090","WTT912","WTT1211","WTT947","WTT1360","WTT1372","WTT1370"];
		var d=frappe.model.get_value('Employee', {'user_id': frappe.session.user}, 'name',
		  function(d) {		    
		    if(ar1.includes(d.name)){
		    	frm.set_value("evaluation_by",d.name)
		    }
		  })
	},
	validate:function(frm){
		if(frm.doc.evaluation_by!=undefined){
		var ar1=["WTT1090","WTT912","WTT1211","WTT947"]
		if(ar1.includes(frm.doc.evaluation_by)){
			var child = frm.add_child("hod_remarks");
			frappe.model.set_value(child.doctype, child.name, "employee_name", frm.doc.evaluator_name);
			frappe.model.set_value(child.doctype, child.name, "practically_possible", frm.doc.reason1);
			frappe.model.set_value(child.doctype, child.name, "yes1", frm.doc.yes);
			frappe.model.set_value(child.doctype, child.name, "no1", frm.doc.no);
			frappe.model.set_value(child.doctype, child.name, "cost_reduction",frm.doc.reason2);
			frappe.model.set_value(child.doctype, child.name, "yes2", frm.doc.yes1);
			frappe.model.set_value(child.doctype, child.name, "no2", frm.doc.no1);
			frappe.model.set_value(child.doctype, child.name, "time_reduction",frm.doc.reason3);
			frappe.model.set_value(child.doctype, child.name, "yes3", frm.doc.yes2);
			frappe.model.set_value(child.doctype, child.name, "no3", frm.doc.no2);
			frappe.model.set_value(child.doctype, child.name, "effort_reduction",frm.doc.reason4);
			frappe.model.set_value(child.doctype, child.name, "yes4", frm.doc.yes3);
			frappe.model.set_value(child.doctype, child.name, "no4", frm.doc.no3);
			frappe.model.set_value(child.doctype, child.name, "quality_improvement",frm.doc.reason5);
			frappe.model.set_value(child.doctype, child.name, "yes5", frm.doc.yes4);
			frappe.model.set_value(child.doctype, child.name, "no5", frm.doc.no4);
			frappe.model.set_value(child.doctype, child.name, "customer_satisfaction",frm.doc.reason10);
			frappe.model.set_value(child.doctype, child.name, "yes10", frm.doc.yes5);
			frappe.model.set_value(child.doctype, child.name, "no10", frm.doc.no5);
			frappe.model.set_value(child.doctype, child.name, "value_proportion",frm.doc.reason11);
			frappe.model.set_value(child.doctype, child.name, "yes11", frm.doc.yes6);
			frappe.model.set_value(child.doctype, child.name, "no11", frm.doc.no6);
			frappe.model.set_value(child.doctype, child.name, "safety",frm.doc.reason12);
			frappe.model.set_value(child.doctype, child.name, "yes12", frm.doc.yes7);
			frappe.model.set_value(child.doctype, child.name, "no12", frm.doc.no7);
			frappe.model.set_value(child.doctype, child.name, "can_be_approved",frm.doc.reason6);
			frappe.model.set_value(child.doctype, child.name, "yes6", frm.doc.can_be_approved);
			frappe.model.set_value(child.doctype, child.name, "explanation_needed",frm.doc.reason8);
			frappe.model.set_value(child.doctype, child.name, "yes7", frm.doc.explanation);
			frappe.model.set_value(child.doctype, child.name, "modification_needed",frm.doc.reason7);
			frappe.model.set_value(child.doctype, child.name, "yes8", frm.doc.modification_needed);
			frappe.model.set_value(child.doctype, child.name, "cant_be_approved",frm.doc.reason9);
			frappe.model.set_value(child.doctype, child.name, "yes9", frm.doc.cant_be_approved);
			frm.refresh_field("hod_remarks")

		}
		else{
			var child = frm.add_child("kaizen_lead_remarks");
			frappe.model.set_value(child.doctype, child.name, "employee_name", frm.doc.evaluator_name);
			frappe.model.set_value(child.doctype, child.name, "practically_possible", frm.doc.reason1);
			frappe.model.set_value(child.doctype, child.name, "yes1", frm.doc.yes);
			frappe.model.set_value(child.doctype, child.name, "no1", frm.doc.no);
			frappe.model.set_value(child.doctype, child.name, "cost_reduction",frm.doc.reason2);
			frappe.model.set_value(child.doctype, child.name, "yes2", frm.doc.yes1);
			frappe.model.set_value(child.doctype, child.name, "no2", frm.doc.no1);
			frappe.model.set_value(child.doctype, child.name, "time_reduction",frm.doc.reason3);
			frappe.model.set_value(child.doctype, child.name, "yes3", frm.doc.yes2);
			frappe.model.set_value(child.doctype, child.name, "no3", frm.doc.no2);
			frappe.model.set_value(child.doctype, child.name, "effort_reduction",frm.doc.reason4);
			frappe.model.set_value(child.doctype, child.name, "yes4", frm.doc.yes3);
			frappe.model.set_value(child.doctype, child.name, "no4", frm.doc.no3);
			frappe.model.set_value(child.doctype, child.name, "quality_improvement",frm.doc.reason5);
			frappe.model.set_value(child.doctype, child.name, "yes5", frm.doc.yes4);
			frappe.model.set_value(child.doctype, child.name, "no5", frm.doc.no4);
			frappe.model.set_value(child.doctype, child.name, "can_be_approved",frm.doc.reason6);
			frappe.model.set_value(child.doctype, child.name, "yes6", frm.doc.can_be_approved);
			frappe.model.set_value(child.doctype, child.name, "explanation_needed",frm.doc.reason8);
			frappe.model.set_value(child.doctype, child.name, "yes7", frm.doc.explanation_needed);
			frappe.model.set_value(child.doctype, child.name, "modification_needed",frm.doc.reason7);
			frappe.model.set_value(child.doctype, child.name, "yes8", frm.doc.modification_needed);
			frappe.model.set_value(child.doctype, child.name, "cant_be_approved",frm.doc.reason9);
			frappe.model.set_value(child.doctype, child.name, "yes9", frm.doc.cant_be_approved);
			refresh_field("kaizen_lead_remarks")
		}

	
		frm.set_value("evaluation_by","");
		frm.set_value("evaluator_name","");
		frm.set_value("evaluator_department","");
		frm.set_value("yes",0);
		frm.set_value("no",0);
		frm.set_value("reason1","");
		frm.set_value("yes1",0);
		frm.set_value("no1",0);
		frm.set_value("reason2","");
		frm.set_value("yes2",0);
		frm.set_value("no2",0);
		frm.set_value("reason3","");
		frm.set_value("yes3",0);
		frm.set_value("no3",0);
		frm.set_value("reason4","");
		frm.set_value("yes4",0);
		frm.set_value("no4",0);
		frm.set_value("reason5","");
		frm.set_value("can_be_approved",0);
		frm.set_value("reason6","");
		frm.set_value("explanation",0);
		frm.set_value("reason7","");
		frm.set_value("modification_needed",0);
		frm.set_value("reason8","");
		frm.set_value("cant_be_approved",0);
		frm.set_value("reason9","");

	}
}
});

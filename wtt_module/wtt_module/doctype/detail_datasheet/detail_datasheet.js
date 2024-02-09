// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Detail datasheet', {
	setup: function(frm,cdt,cdn) {
		frm.set_query("project", function() {
		    return {
				filters: [
					// ["Project","status", "!=", "Open"],
					["Project","status", "!=", "Cancelled"],
					["Project","status", "!=", "Completed"]
				]
			};
		});
		
	},
	onload:function(frm,cdt,cdn){
		var bb=[];
		$.each(frm.doc.system_table || [], function(i,v){
			bb.push(v.system_name);
		})
		var df = frappe.meta.get_docfield("Datasheet Instrument Table","system", frm.doc.name);
		df.options = bb;
	},
	get_queries:function(frm,cdt,cdn){
		var aa=[]
		var a1=[]
		var a2=[]
		var a3=[]
		var sd = locals[cdt][cdn];

		$.each(frm.doc.system_table || [], function(i, v) {
			if(v.__checked==true){
				aa.push(v.system_name)
			}
			var df = frappe.meta.get_docfield("Datasheet Instrument Table","system", frm.doc.name);
			df.options = aa;
		});
		frappe.call({
				"method":"wtt_module.wtt_module.doctype.detail_datasheet.detail_datasheet.get_beltpress",
				args:{
					"val":aa
				},

	
	// system_name: function(frm,cdt, cdn){
	// var sd = locals[cdt][cdn];
	// frappe.call({
	// 		"method":"wtt_module.wtt_module.doctype.detail_datasheet.detail_datasheet.get_beltpress",
	// 		args:{
	// 			"val":sd.system_name
	// 		},
			callback(r){

				for(var i=0;i<r.message.length;i++)
				{
					if(r.message[i].name1=='Pump List')
					{
					var child = frm.add_child("pump_list_details");
					frappe.model.set_value(child.doctype, child.name, "pump", r.message[i].parameter);
					frappe.model.set_value(child.doctype, child.name, "system", r.message[i].name);
					frm.refresh_field("pump_list_details");
					}
					if(r.message[i].name1=='Dosing Pump')
					{
					var child = frm.add_child("dosing_pump_details");
					frappe.model.set_value(child.doctype, child.name, "dosing_pump", r.message[i].parameter);
					frappe.model.set_value(child.doctype, child.name, "system", r.message[i].name);
					frm.refresh_field("dosing_pump_details");
					}
					if(r.message[i].name1=='Type')
					{
					var child = frm.add_child("system_details");
					frappe.model.set_value(child.doctype, child.name, "system", r.message[i].name);
					frappe.model.set_value(child.doctype, child.name, "type", r.message[i].parameter);
					frm.refresh_field("system_details");
					}
					if(r.message[i].name1=='Instrument')
					{
					var child = frm.add_child("instrument_details");
					frappe.model.set_value(child.doctype, child.name, "system", r.message[i].name);
					frappe.model.set_value(child.doctype, child.name, "instrument", r.message[i].parameter);
					frm.refresh_field("instrument_details");
					}		
				}
				// for(var i=0;i<aa.length;i++){
				// var v = frm.add_child("instrument_details");
				// frappe.model.set_value(v.doctype, v.name, "system", aa[i]);
				// frm.refresh_field("instrument_details");
				// }
			}
	});
	}
});


frappe.ui.form.on('System Table', {
	
	
});
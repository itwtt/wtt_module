// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Info', {
	get_link:function(frm){
		var htvalue = "<a style='background-color: white;color: black;border: 2px solid green;padding: 5px 5px;text-align: center;text-decoration: none;display: inline-block;' href="+frm.doc.location_link+" target='_blank'>Location</a>"
		$(frm.fields_dict['map'].wrapper).html(htvalue);
	},
	project: function(frm) {
		frm.clear_table("equipments");
		frm.refresh_field("equipments");
		frappe.call({
			method:"wtt_module.wtt_module.doctype.project_info.project_info.get_system_table",
			args:{
				project:frm.doc.project
			},
			callback(r){
				for(var i=0;i<r.message.length;i++){
					var child = frm.add_child("equipments");
					frappe.model.set_value(child.doctype, child.name, "system_name", r.message[i]);
					frm.refresh_field("equipments");

				}
			}
		})
	},
	validate:function(frm){
		frm.clear_table("tracking_table");
		frm.refresh_field("tracking_table");
		var arr=[]
		frappe.call({
			method:"wtt_module.wtt_module.doctype.project_info.project_info.get_tracking",
			args:{
				project:frm.doc.project
			},
			callback(r){
				for(var i=0;i<r.message.length;i++){
					var child = frm.add_child("tracking_table");
					frappe.model.set_value(child.doctype, child.name, "document_name", r.message[i].document_name);
					frappe.model.set_value(child.doctype, child.name, "created", r.message[i].created);
					frappe.model.set_value(child.doctype, child.name, "approved_by_hod", r.message[i].approved_by_hod);
					frappe.model.set_value(child.doctype, child.name, "emergency_app", r.message[i].emergency_app);
					frappe.model.set_value(child.doctype, child.name, "approved", r.message[i].approved);
					frappe.model.set_value(child.doctype, child.name, "total", r.message[i].total);
					frm.refresh_field("tracking_table");
				}
			}
		})

		frappe.call({
			method:"wtt_module.wtt_module.doctype.project_info.project_info.pr_details",
			args:{
				project:frm.doc.project
			},
			callback(r){
				for(var i=0;i<r.message.length;i++){
					frm.set_value("pr_draft",r.message[i].prdraft)
					frm.set_value("pr_to_bill",r.message[i].prbill)
					frm.set_value("pr_completed",r.message[i].prcom)
					frm.set_value("pr_total",r.message[i].prtotal)
					frm.set_value("inv_draft",r.message[i].pidraft)
					frm.set_value("inv_overdue",r.message[i].piover)
					frm.set_value("inv_paid",r.message[i].pipaid)
					frm.set_value("inv_total",r.message[i].pitotal)
				}
			}
		})
	}
});

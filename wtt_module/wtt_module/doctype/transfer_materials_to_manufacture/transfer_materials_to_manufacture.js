// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transfer Materials to Manufacture', {
	setup:function(frm){
		frm.set_query("bom", function() {
		return {
			filters: [
				["BOM","docstatus","=", 1]
			]
		}
		})
		frm.set_query("purchase_receipt", function() {
		return {
			filters: [
				["Purchase Receipt","docstatus","=", 1],
				["Purchase Receipt","naming_series","!=", "JR-.YY.-"]
			]
		}
		})
	},
	get_bom:function(frm){
		var bom = frm.doc.bom;
		frappe.call({
			method:"wtt_module.wtt_module.doctype.transfer_materials_to_manufacture.transfer_materials_to_manufacture.get_bom",
			args:{
				bom:bom
			},
			callback(r){
				frm.set_value("assembly_items",r.message);
				frm.refresh_field("assembly_items");
			}
		})
	},
	get_pr:function(frm){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.transfer_materials_to_manufacture.transfer_materials_to_manufacture.get_pr",
			args:{
				pr:frm.doc.purchase_receipt
			},
			callback(r){
				frm.set_value("raw_materials",r.message);
				frm.refresh_field("raw_materials");
			}
		})
	},
	refresh: function(frm) {
		frm.add_custom_button(__('START'), () => frm.events.send_raw_materials(frm)).addClass("btn-warning").css({'background-color':'tomato','color':'black','padding':'10dp'});
		frm.add_custom_button(__('FINISH'), () => frm.events.bring_assembled_item(frm)).addClass("btn-warning").css({'background-color':'green','color':'black','padding':'10dp'});
	},
	send_raw_materials(frm){
	    var d = new frappe.ui.Dialog({
		'fields': [
		{"fieldtype": "Link", "label":"To Warehouse", "fieldname": "to_warehouse","options":"Warehouse","get_query" : function(){return{"doctype": "Warehouse","filters":{"company":"W.t.t technology Services India Pvt Ltd"}}}
		}
		],
		primary_action: function(values){ 
			frappe.call({
			"method":"wtt_module.wtt_module.doctype.transfer_materials_to_manufacture.transfer_materials_to_manufacture.create_stock",
			args:{
				"items":frm.doc.raw_materials,
				"warehouse":values.to_warehouse
			},
			callback: function(r) {
				msgprint('Raw Materials were added in Stock')
			}
			});
			d.hide();
		}
		});
		d.show();
	},
	bring_assembled_item(frm){
	    var d = new frappe.ui.Dialog({
		'fields': [
		{"fieldtype": "Link", "label":"To Warehouse", "fieldname": "to_warehouse","options":"Warehouse","get_query" : function(){return{"doctype": "Warehouse","filters":{"company":"W.t.t technology Services India Pvt Ltd"}}}
		}
		],
		primary_action: function(values){ 
			frappe.call({
			"method":"wtt_module.wtt_module.doctype.transfer_materials_to_manufacture.transfer_materials_to_manufacture.get_stock",
			args:{
				"items":frm.doc.assembly_items,
				"warehouse":values.to_warehouse
			},
			callback: function(r) {
				msgprint('Assembled Items were added in Stock')
			}
			});
			d.hide();
		}
		});
		d.show();
	}
});

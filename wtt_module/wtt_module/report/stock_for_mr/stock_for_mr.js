// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stock for MR"] = {
	"filters": [
	{
		"label":"MATERIAL REQUEST",
		"fieldname":"material_request",
		"fieldtype":"Link",
		"options":"Material Request",
		"default":"MR-22-00355",
		"get_query" : function(){
			return{
				"filters":[
					["Material Request","docstatus", "=", 1],
				]
			}
		}
	}
	],
	onload: function(report) {
		frappe.query_report.page.add_inner_button(__("Allocate"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			for (var i in v){
				var d = new frappe.ui.Dialog({
			    'fields': [
			        {'fieldname': 'item_code', 'fieldtype': 'Link','options':'Item','label':'Item Code','default':frappe.query_report.data[v[i]].item_code,'read_only':1},
			        {'fieldname': 'description', 'fieldtype': 'Data','label':'Description','default':frappe.query_report.data[v[i]].description,'read_only':1},
					{'fieldname': 'technical_description', 'fieldtype': 'Text','label':'Technical Description','default':frappe.query_report.data[v[i]].technical_description,'read_only':1},
					{'fieldname': 'project', 'fieldtype': 'Link','label':'Project',"options":"Project"},
					{'fieldname': 'qty', 'fieldtype': 'Float','label':'Qty'},
					{'fieldname': 'uom', 'fieldtype': 'Data','label':'UOM','default':frappe.query_report.data[v[i]].uom,'read_only':1}

			    ],
			    primary_action: function(values){
			    	frappe.call({
			    		method:"wtt_module.wtt_module.report.stock_for_mr.stock_for_mr.func",
			    		args:{
			    			"item_code":values.item_code,
			    			"project":values.project,
			    			"qty":values.qty,
			    			"uom":values.uom
			    		},
			    		callback(r){
			        	frappe.query_report.refresh();
			        	}
			    	});
			        d.hide();

			    }
				});
				d.show();
			}
			
		});
		
	},
	get_datatable_options(options) {
        return Object.assign(options, {
            checkboxColumn: true
        });
    }
};

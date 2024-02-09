// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Convert PO"] = {
	"filters": [
		{	
		"label":"Item Group",
		"fieldname":"item_group",
		"fieldtype":"Link",
		"options":"Item Group",
		"default":"PIPES"
		},
		{	
		"label":"Description",
		"fieldname":"description",
		"fieldtype":"Select"
		},
		{	
		"label":"Project",
		"fieldname":"project",
		"fieldtype":"Link",
		"options":"Project",
		"default":"WTT-0408",
		"get_query" : function(){
			return{
				"filters":[
					["Project","status", "!=", "Open"],
					["Project","status", "!=", "Cancelled"],
					["Project","status", "!=", "Completed"]
				]
			}
		}
		},
		{	
		"label":"Attribute Value 1",
		"fieldname":"tech",
		"fieldtype":"Select"
		},
		{	
		"label":"Attribute Value 2",
		"fieldname":"tech1",
		"fieldtype":"Select"
		},
		{	
		"label":"Attribute Value 3",
		"fieldname":"tech2",
		"fieldtype":"Select"
		}
	],
	onload: function(report) {
		frappe.call({
				"method":"wtt_module.wtt_module.report.convert_po.convert_po.get_value",
				callback(r){
					var tt = frappe.query_report.get_filter('tech');
					tt.df.options = r.message[0];
					tt.refresh();

					var tt = frappe.query_report.get_filter('tech1');
					tt.df.options = r.message[0];
					tt.refresh();

					var tt = frappe.query_report.get_filter('tech2');
					tt.df.options = r.message[0];
					tt.refresh();

					var tt = frappe.query_report.get_filter('description');
					tt.df.options = r.message[1];
					tt.refresh();
				}
			})
	frappe.query_report.page.add_inner_button(__("Generate new RFQ"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();

			for(i in v)
			{
				selected_rows.push({
				'item_code':frappe.query_report.data[v[i]].item_code,
				'qty':frappe.query_report.data[v[i]].qty,
				'description':frappe.query_report.data[v[i]].description,
				'conversion_factor':frappe.query_report.data[v[i]].conversion_factor,
				'stock_uom':frappe.query_report.data[v[i]].stock_uom,
				'warehouse':'Stores - WTT',
				'uom':frappe.query_report.data[v[i]].uom,
				'material_request':frappe.query_report.data[v[i]].mr_no,
				'material_request_item':frappe.query_report.data[v[i]].ref,
				'project_name':frappe.query_report.data[v[i]].project
				})
			}
			frappe.run_serially([
		  	// () => frappe.route_options = {schedule_date:values.date},
		  	() => frappe.set_route('Form', 'Request for Quotation', "new-request-for-quotation-1"), 
		  	() => cur_frm.set_value("items", selected_rows),
		  	])

		},("Create"));
		frappe.query_report.page.add_inner_button(__("Existing RFQ"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();

			let d = new frappe.ui.Dialog({
			    title: 'Quotation Details',
			    fields: [
			        {
			            label: 'Request for Quotation',
			            fieldname: 'rfq',
			            fieldtype: 'Link',
			            options:"Request for Quotation",
			            "get_query" : function(){
							// var branch = frappe.query_report_filters_by_name.branch.get_value();
							return{
								"doctype": "Request for Quotation",
								"filters":{
									"docstatus":0,
								}
							}
						}
			        }
			    ],
			    primary_action_label: 'Create',
			    primary_action(values) {
			    	var currentdate = new Date();
			    	for(i in v)
						{
							selected_rows.push({
								'item_code':frappe.query_report.data[v[i]].item_code,
								'qty':frappe.query_report.data[v[i]].qty,
								'description':frappe.query_report.data[v[i]].description,
								'conversion_factor':frappe.query_report.data[v[i]].conversion_factor,
								'stock_uom':frappe.query_report.data[v[i]].stock_uom,
								'warehouse':"Stores - WTT",
								'uom':frappe.query_report.data[v[i]].uom,
								'material_request':frappe.query_report.data[v[i]].mr_no,
								'material_request_item':frappe.query_report.data[v[i]].ref,
								'schedule_date':currentdate.getFullYear() + "-" + currentdate.getMonth() + "-" + currentdate.getDate() ,
								'project_name':frappe.query_report.data[v[i]].project
							})
						}
						var dd = values.rfq
						frappe.call({
							method:"wtt_module.wtt_module.report.convert_po.convert_po.create_existing_po",
							args:{
								doc:dd
							},
							callback(r){
								for (var i=0;i<r.message.length;i++){
									selected_rows.push({
										'item_code':r.message[i].item_code,
										'qty':r.message[i].qty,
										'description':r.message[i].description,
										'conversion_factor':r.message[i].conversion_factor,
										'stock_uom':r.message[i].stock_uom,
										'warehouse':r.message[i].warehouse,
										'uom':r.message[i].uom,
										'material_request':r.message[i].material_request,
										'material_request_item':r.message[i].material_request_item,
										'schedule_date':r.message[i].schedule_date,
										'project_name':r.message[i].project_name
									})
								}
								frappe.run_serially([
							  	() => frappe.set_route('Form', 'Request for Quotation', dd), 
							  	() => cur_frm.set_value("items", selected_rows),
							  	])
							}
						})
					
					    d.hide();
					    }
					});

			d.show();

		},("Create"));
	},
	get_datatable_options(options) {
        return Object.assign(options, {
            checkboxColumn: true
        });
    }
};

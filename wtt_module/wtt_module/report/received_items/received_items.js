// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Received Items"] = {
	"filters": [
	{
		"label":"System",
		"fieldname":"system",
		"fieldtype":"Link",
		"options":"System3",
		"default":"Air Blower"
	},
	{
		"label":"Project",
		"fieldname":"project",
		"fieldtype":"Link",
		"options":"Project",
		"default":"WTT-0206",
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
		"label":"Start Date",
		"fieldname":"start_date",
		"fieldtype":"Date"
	},
	{
		"label":"End Date",
		"fieldname":"end_date",
		"fieldtype":"Date"
	},
	{
		"label":"Track Box",
		"fieldname":"track_boxes",
		"fieldtype":"Check"
	}
	],
	onload: function(report) {
		
		frappe.query_report.page.add_inner_button(__("Get Details"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();

			for(i in v)
			{
				selected_rows.push({
				'item_code':frappe.query_report.data[v[i]].item_code
				})
			}
			var gug = frappe.query_report.get_filter('project')
			var vis = frappe.query_report.get_filter('system')
			frappe.call({
				method:"wtt_module.wtt_module.report.received_items.received_items.get_details",
				args:{
					datas:selected_rows
				},
				callback(r){
					var arr = r.message;
					var htvalue = "<table border='1' width='100%'><th><center>PACKING SLIP</center></th><th><center>ROW</center></th><th><center>DESCRIPTION</center></th><th><center>QTY</center></th><th><center>UOM</center></th><th><center>BOX NO</center></th>";
					for(var i=0;i<arr.length;i++){
						htvalue += "<tr>"
						htvalue += "<td align='center'>"+arr[i].parent+"</td><td align='center'>"+arr[i].idx+"</td><td align='center'>"+arr[i].description+"</td><td align='center'>"+arr[i].qty+"</td><td align='center'>"+arr[i].stock_uom+"</td><td align='center'>"+arr[i].box_no+"</td>"
						htvalue += "</tr>"
					}
					htvalue += "</table>"
					let d = new frappe.ui.Dialog({
						fields: [
							{
								label: 'Packing Slip',
								fieldname: 'table',
								fieldtype: 'HTML',
								options:htvalue

							}
						]
						});
					d.show();
					
				}
			})

		});
	},
	get_datatable_options(options) {
		return Object.assign(options, {
		    checkboxColumn: true
		});
	}
};

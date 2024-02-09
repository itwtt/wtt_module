// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item Lead"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"label":"Material Request",
			"fieldname":"material_request",
			"fieldtype":"Link",
			"options":"Material Request",
			"get_query" : function(){
			return{
				"doctype": "Material Request",
				"filters":{
					"docstatus":1,
				}
			}
		}
		},
		{
			"label":"Item",
			"fieldname":"item",
			"fieldtype":"Link",
			"options":"Item",
			"get_query" : function(){
			return{
				"doctype": "Item",
				"filters":{
					"has_variants":1,
				}
			}
			}
		},
		{
			"fieldname":"dc",
			"label": __("Doctype"),
			"fieldtype": "Link",
			"options":"DocType",
			"default":"Material Request"
		}
	],
	onload: function(report) {
		report.page.add_inner_button(__("Material Request"), function() {
				var year_filter = frappe.query_report.get_filter('dc');
				year_filter.set_input("Material Request");
				year_filter.refresh();
				var dd = frappe.query_report.get_filter('from_date');
				dd.set_input(new Date(new Date().getFullYear(),new Date().getMonth()-new Date().getMonth()+3));
				dd.refresh();
		});

		report.page.add_inner_button(__("Item"), function() {
				var year_filter = frappe.query_report.get_filter('dc');
				year_filter.set_input("Item");
				year_filter.refresh();
				var dd = frappe.query_report.get_filter('from_date');
				dd.set_input(new Date(new Date().getFullYear(),new Date().getMonth()-new Date().getMonth()+3));
				dd.refresh();
		});
	}
};

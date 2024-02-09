// Copyright (c) 2016, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Overall report"] = {
	"filters": [
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options":"Project",
			"get_query": function() {
				return {
					filters: {
						"status": "On going"
					}
				};
			}
		},
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
			"fieldname":"dc",
			"label": __("Doctype"),
			"fieldtype": "Link",
			"options":"DocType"
		}
	],
	onload: function(report) {
		report.page.add_inner_button(__("Material Request"), function() {
				var year_filter = frappe.query_report.get_filter('dc');
				var hh = frappe.datetime.get_today().split('-')[0] + '-01-01'
				year_filter.set_input("Material Request");
				year_filter.refresh();
				var dd = frappe.query_report.get_filter('from_date');
				var vv = frappe.query_report.get_filter('project');
				vv.set_input("");
				vv.refresh();
				dd.set_input(hh);
				dd.refresh();
		});

		report.page.add_inner_button(__("Purchase Order"), function() {
				var vv = frappe.query_report.get_filter('project');
				vv.set_input("");
				vv.refresh();
				var year_filter = frappe.query_report.get_filter('dc');
				year_filter.set_input("Purchase Order");
				year_filter.refresh();
				var dd = frappe.query_report.get_filter('from_date');
				dd.set_input(frappe.datetime.get_today().split('-')[0] + '-01-01');
				dd.refresh();
				
		});

		report.page.add_inner_button(__("Purchase Receipt"), function() {
				var vv = frappe.query_report.get_filter('project');
				vv.set_input("");
				vv.refresh();
				var year_filter = frappe.query_report.get_filter('dc');
				year_filter.set_input("Purchase Receipt");
				year_filter.refresh();
				var dd = frappe.query_report.get_filter('from_date');
				dd.set_input(frappe.datetime.get_today().split('-')[0] + '-01-01');
				dd.refresh();

		});


		report.page.add_inner_button(__("Purchase Invoice"), function() {
				var vv = frappe.query_report.get_filter('project');
				vv.set_input("");
				vv.refresh();
				var year_filter = frappe.query_report.get_filter('dc');
				year_filter.set_input("Purchase Invoice");
				year_filter.refresh();
				var dd = frappe.query_report.get_filter('from_date');
				dd.set_input(frappe.datetime.get_today().split('-')[0] + '-01-01');
				dd.refresh();
		});


		// report.page.add_inner_button(__("Sales Invoice"), function() {
		// 		var year_filter = frappe.query_report.get_filter('dc');
		// 		year_filter.set_input("Sales Invoice");
		// 		year_filter.refresh();
		// 		var dd = frappe.query_report.get_filter('from_date');
		// 		dd.set_input(new Date(new Date().getFullYear(),new Date().getMonth()-new Date().getMonth()+3));
		// 		dd.refresh();
		// });
	}
};

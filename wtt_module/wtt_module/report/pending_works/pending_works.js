// Copyright (c) 2016, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pending works"] = {
	"filters": [
		{
			"fieldname":"emp",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options":"Employee"
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": new Date(new Date().getFullYear(),new Date().getMonth(),1)
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"dept",
			"label": __("Department"),
			"fieldtype": "Link",
			"options":"Department"
		},
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options":["","Pending","Partially pending","Completed"]
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
       	if(value=="Pending")
       	{
       		value = '<b style="color: red;">'+value+'</b>';
       	}
       	else if(value=="Completed")
       	{
       		value = '<b style="color: green;">'+value+'</b>';
       	}
       	else if(value=="Partially pending")
       	{
       		value = '<b style="color: orange;">'+value+'</b>';
       	}
       	return value
    },
    onload: function(report) {

    	var oneWeekAgo = new Date();
		oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

		var onemonth = new Date();
		onemonth.setMonth(onemonth.getMonth()-1);

		report.page.add_inner_button(__("Pending"), function() {
				var year_filter = frappe.query_report.get_filter('status');
				year_filter.set_input("Pending");
				year_filter.refresh();
				var dd = frappe.query_report.get_filter('from_date');
				dd.set_input(new Date(new Date().getFullYear(),new Date().getMonth(),1));
				dd.refresh();
		});
		report.page.add_inner_button(__("Partially pending"), function() {
				var year_filter = frappe.query_report.get_filter('status');
				year_filter.set_input("Partially pending");
				year_filter.refresh();
				var dd = frappe.query_report.get_filter('from_date');
				dd.set_input(new Date(new Date().getFullYear(),new Date().getMonth(),1));
				dd.refresh();
		});
		report.page.add_inner_button(__("Completed"), function() {
				var year_filter = frappe.query_report.get_filter('status');
				year_filter.set_input("Completed");
				year_filter.refresh();
				var dd = frappe.query_report.get_filter('from_date');
				dd.set_input(new Date(new Date().getFullYear(),new Date().getMonth(),1));
				dd.refresh();
		});
		report.page.add_inner_button(__("Overall"), function() {
				var year_filter = frappe.query_report.get_filter('status');
				year_filter.set_input("");
				year_filter.refresh();
				var dd = frappe.query_report.get_filter('from_date');
				dd.set_input(new Date(new Date().getFullYear(),new Date().getMonth(),1));
				dd.refresh();
		});

		report.page.add_inner_button(__("Today"), function() {
				var dd = frappe.query_report.get_filter('from_date');
				dd.set_input(frappe.datetime.get_today());
				dd.refresh();
		});

		report.page.add_inner_button(__("Last week"), function() {
				var year_filter = frappe.query_report.get_filter('status');
				year_filter.set_input("Pending");
				year_filter.refresh();
				var dd = frappe.query_report.get_filter('from_date');
				dd.set_input(oneWeekAgo);
				dd.refresh();
		});

		report.page.add_inner_button(__("Last month"), function() {
				var year_filter = frappe.query_report.get_filter('status');
				year_filter.set_input("Pending");
				year_filter.refresh();
				var dd = frappe.query_report.get_filter('from_date');
				dd.set_input(onemonth);
				dd.refresh();
		});
	},
};

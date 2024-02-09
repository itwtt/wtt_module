frappe.query_reports["Activity sheet"] = {
	"filters": [
		// {
		// 	"fieldname":"emp",
		// 	"label": __("Employee"),
		// 	"fieldtype": "Link",
		// 	"options":"Employee"
		// },
		// {
		// 	"fieldname":"pro",
		// 	"label": __("Project"),
		// 	"fieldtype": "Link",
		// 	"options":"Project"
		// },
		// {
		// 	"fieldname":"sys1",
		// 	"label": __("System"),
		// 	"fieldtype": "Link",
		// 	"options":"System Module"
		// },
		// {
		// 	"fieldname":"from_date",
		// 	"label": __("From Date"),
		// 	"fieldtype": "Date",
		// 	"default": frappe.datetime.get_today()
		// },
		// {
		// 	"fieldname":"to_date",
		// 	"label": __("To Date"),
		// 	"fieldtype": "Date",
		// 	"default": frappe.datetime.get_today()
		// },
		// {
		// 	"fieldname":"dept",
		// 	"label": __("Department"),
		// 	"fieldtype": "Link",
		// 	"options":"Department"
		// },
		// {
		// 	"fieldname":"dc",
		// 	"label": __("Doctype"),
		// 	"fieldtype": "Link",
		// 	"options":"DocType"
		// }
		{
			"fieldname": "emp",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "dept",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department"
		},
		{
			"fieldname": "date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default":frappe.datetime.add_days(frappe.datetime.get_today(), -1)
		}
	],
	// onload: function(report) {
	// 	report.page.add_inner_button(__("Other Department"), function() {
	// 			var year_filter = frappe.query_report.get_filter('dc');
	// 			year_filter.set_input("Activity Sheet");
	// 			year_filter.refresh();
	// 			var dd = frappe.query_report.get_filter('from_date');
	// 			dd.set_input(new Date(new Date().getFullYear(),new Date().getMonth(),1));
	// 			dd.refresh();
	// 	});
	// 	report.page.add_inner_button(__("Design Team"), function() {
	// 			var year_filter = frappe.query_report.get_filter('dc');
	// 			year_filter.set_input("Daily Activity");
	// 			year_filter.refresh();
	// 			var dd = frappe.query_report.get_filter('from_date');
	// 			dd.set_input(new Date(new Date().getFullYear(),new Date().getMonth(),1));
	// 			dd.refresh();
	// 	});
	// }
};

frappe.query_reports["Workshop Report"] = {
	"filters":  [
		{
			"fieldname":"emp",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options":"Employee",
			"get_query": function() {
				return {
					"doctype": "Employee",
					"filters": {
						"branch": "Workshop",
						"status":"Active"
					}
				}
			}
		},
		{
			"fieldname":"pro",
			"label": __("Project"),
			"fieldtype": "Link",
			"options":"Project"
		},
		{
			"fieldname":"skid",
			"label": __("Skid"),
			"fieldtype": "Link",
			"options":"Skid module"
		},
		{
			"fieldname":"nature_of_job",
			"label": __("Job Nature"),
			"fieldtype": "Link",
			"options":"job Module"
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
		}
	]
};
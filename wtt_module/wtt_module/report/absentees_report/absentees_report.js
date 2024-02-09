frappe.query_reports["Absentees Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Datetime",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Datetime",
			"width": "80",
			"reqd": 1,
			"default":new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate(), 9, 30,0)
		}
		/*{
			"fieldname":"branch",
			"fieldtype":"Link",
			"label":"Branch",
			"options":"Branch"
		},
		{
			"fieldname":"department",
			"fieldtype":"Link",
			"label":"Department",
			"options":"Department"
		}*/
	]
};

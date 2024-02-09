frappe.query_reports["Dev Follow Up"] = {
	"filters": [
	{
		"label":"Reports Type",
		"fieldtype":"Select",
		"fieldname":"reports_type",
		"options":["--Select--","Status wise","Followup Table wise"],
		"default":"Status wise"
	},
	{
		"label":"Lead Status",
		"fieldtype":"Select",
		"fieldname":"lead_ss",
		"options":["","Red Hot","Hot","Warm","Cold","Lead"],
	}
	]
};

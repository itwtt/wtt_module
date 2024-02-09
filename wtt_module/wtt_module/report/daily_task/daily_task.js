frappe.query_reports["Daily Task"] = {
	"filters": [
		{
			"label":"Employee",
			"fieldname":"employee",
			"fieldtype":"Link",
			"options":"Employee",
			"width":100
		},
		{
			"label":"From Date",
			"fieldname":"from_date",
			"fieldtype":"Date",
			"default":new Date(new Date().getFullYear(),new Date().getMonth()-1),
			"width":100
		},
		{
			"label":"To Date",
			"fieldname":"to_date",
			"fieldtype":"Date",
			"default": new Date(new Date().getFullYear(),new Date().getMonth()),
			"width":100
		},
		{
			"label":"Status",
			"fieldname":"status",
			"fieldtype":"Select",
			"options":["Pending","Partially Completed","Completed"] ,
			"width":100
		},
		{
			"label":"Department",
			"fieldname":"department",
			"fieldtype":"Link",
			"options":"Department",
			"width":100
		}


	]
	// "filters":  [
	// 	{
	// 		"fieldname":"emp",
	// 		"label": __("Employee"),
	// 		"fieldtype": "Link",
	// 		"options":"Employee"
	// 	},
	// 	{
	// 		"fieldname":"pro",
	// 		"label": __("Project"),
	// 		"fieldtype": "Link",
	// 		"options":"Project"
	// 	},
	// 	{
	// 		"fieldname":"sys1",
	// 		"label": __("System I"),
	// 		"fieldtype": "Link",
	// 		"options":"System Module"
	// 	},
	// 	{
	// 		"fieldname":"from_date",
	// 		"label": __("From Date"),
	// 		"fieldtype": "Date",
	// 		"default": frappe.datetime.get_today()
	// 	},
	// 	{
	// 		"fieldname":"to_date",
	// 		"label": __("To Date"),
	// 		"fieldtype": "Date",
	// 		"default": frappe.datetime.get_today()
	// 	}
	// 	/*{
	// 		"fieldname":"dc",
	// 		"label": __("Doctype"),
	// 		"fieldtype": "Link",
	// 		"options":"DocType"
	// 	}*/
	// ]
	/*onload: function(report) {
		report.page.add_inner_button(__("button "), function() {
				alert("hh")
		});
	}*/
};

	

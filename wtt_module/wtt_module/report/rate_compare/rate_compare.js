// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Rate Compare"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Project"
		},
		{
			"fieldname": "name",
			"label": __("Purchase Order"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Purchase Order",
			"get_query": () => {
			    return {
			        filters: [["docstatus", "=", 1], ["naming_series", '=', 'PO-.YY.-']]
			    };
			}
		},
		{
			"fieldname":"supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Supplier",
			"get_query": () =>{
				return {
					filters: { "disabled": 0 }
				}
			}
		}
	]
};

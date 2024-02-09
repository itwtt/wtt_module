// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Not Received Items"] = {
	"filters": [
		{	
		"label":"Purchase Order",
		"fieldname":"po_no",
		"fieldtype":"Link",
		"options":"Purchase Order"
		},
		{	
		"label":"Supplier",
		"fieldname":"supplier",
		"fieldtype":"Link",
		"options":"Supplier"
		},
		{
		"label":"Project",
		"fieldname":"project",
		"fieldtype":"Link",
		"options":"Project"
		}
	]
};

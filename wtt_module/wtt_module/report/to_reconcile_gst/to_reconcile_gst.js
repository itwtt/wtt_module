// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["to Reconcile GST"] = {
	"filters": [
	{
		"label":"Reconcile Number",
		"fieldname":"reconcile_number",
		"fieldtype":"Link",
		"options":"GST reconcilation"
	}
	]
};

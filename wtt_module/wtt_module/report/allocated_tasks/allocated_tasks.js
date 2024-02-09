// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Allocated Tasks"] = {
	"filters": [
		{
			"label":"Report Type",
			"fieldname":"report_type",
			"fieldtype":"Select",
			"options":["Task List","Employee Points","Department Points"] ,
			"default":"Task List",
			"width":100
		},
		{
			"label":"From Date",
			"fieldname":"from_date",
			"fieldtype":"Date",
			"default":new Date(new Date().getFullYear(),new Date().getMonth()),
			"width":100
		},
		{
			"label":"To Date",
			"fieldname":"to_date",
			"fieldtype":"Date",
			"default": new Date(new Date().getFullYear(),new Date().getMonth()+1,0),
			"width":100
		},
		{
			"label":"Employee",
			"fieldname":"employee",
			"fieldtype":"Link",
			"options":"Employee",
			"width":100
		},
		
		{
			"label":"Department",
			"fieldname":"department",
			"fieldtype":"Link",
			"options":"Department",
			"width":100
		},
		{
			"label":"Except",
			"fieldname":"status",
			"fieldtype":"Select",
			"options":["Pending","Partially pending","Completed"] ,
			"width":100
		}
		

	]
};

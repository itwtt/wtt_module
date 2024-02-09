// Copyright (c) 2016, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Approval leave"] = {
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
			"default":new Date(new Date().getFullYear(),new Date().getMonth(),1),
			"print_hide":1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": new Date(new Date().getFullYear(),new Date().getMonth()+1,0)
		}

	],
	"formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
       	if(value=="LOP")
       	{
       		value = '<b style="color: red;">'+value+'</b>';
       	}
       	else if(value=="EL")
       	{
       		value = '<b style="color: green;">'+value+'</b>';
       	}
       	else if(value=="EML")
       	{
       		value = '<b style="color: orange;">'+value+'</b>';
       	}
       	else if(value=="SL")
       	{
       		value = '<b style="color: cornflowerblue;">'+value+'</b>';
       	}
       	else if(value=="BL")
       	{
       		value = '<b style="color: indigo;">'+value+'</b>';
       	}
       	else if(value=="CL")
       	{
       		value = '<b style="color: purple;">'+value+'</b>';
       	}
       	return value
    }
};

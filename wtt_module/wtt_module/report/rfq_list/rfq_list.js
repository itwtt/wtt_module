// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["RFQ List"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.defaults.get_user_default("year_start_date"),
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		}
	]
};


function getURL(e) {
    var v='https://erp.wttindia.com/app/query-report/Comparison?request_for_quotation='
    var result = v.concat(e.getAttribute("data-message"));
    window.location.href = result;
}
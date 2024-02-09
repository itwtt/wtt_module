frappe.query_reports["PRE MR Ref"] = {
	"filters": [
		{
			fieldname: "pre_mr",
			label: __("Pre MR"),
			fieldtype: "Link",
			options: "Pre MR",
			"get_query": function() {
				return {
					filters: {
						"docstatus": 1
					}
				};
			}
		}
	]
};

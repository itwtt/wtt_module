// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item Variant Details With Supplier"] = {
	"filters": [
		{
			reqd: 1,
			default: "",
			options: "Item",
			label: __("Item"),
			fieldname: "item",
			fieldtype: "Link",
			get_query: () => {
				return {
					filters: { "has_variants": 1 }
				}
			}
		}
	]
};

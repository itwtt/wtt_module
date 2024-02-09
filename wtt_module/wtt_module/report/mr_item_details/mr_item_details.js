// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */
var ar=["Material Request","Purchase Order"]
frappe.query_reports["MR Item Details"] = {
	"filters": [
	{
		"label":"ITEM",
		"fieldname":"item",
		"fieldtype":"Link",
		"options":"Item",
		"get_query" : function(){
			return{
				"doctype": "Item",
				"filters":{
					"has_variants":1,
				}
			}
		}
	},
	{
		"label":"ITEM CODE",
		"fieldname":"item_code",
		"fieldtype":"Link",
		"options":"Item",
		"get_query" : function(){
			return{
				"doctype": "Item",
				"filters":{
					"has_variants":0
				}
			}
		}
	},
	{
		"label":"MODULE",
		"fieldname":"module",
		"fieldtype":"Link",
		"options":"DocType",
		"default":"Material Request"
		// "get_query" : function(){
		// 	return{
		// 		"doctype": "DocType",
		// 		"filters":{
		// 			["name" "=" "Material Request"]
		// 		}
		// 	}
		// }
		
	},
	{
		"label":"ITEM GROUP",
		"fieldname":"item_group",
		"fieldtype":"Link",
		"options":"Item Group",
	},
	{
		"label":"NAME",
		"fieldname":"mr_name",
		"fieldtype":"Dynamic Link",
		"options":"module"
	},
	{
		"label":"TOTAL",
		"fieldname":"total",
		"fieldtype":"Check"
	}

	]
};

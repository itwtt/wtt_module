# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet

class VendorDetails(NestedSet):
	pass

@frappe.whitelist()
def get_children(doctype, parent,category=None,supplier=None, is_root=False):	
	filters = [["docstatus", "<", "2"]]
	if supplier and category:
		filters.append(["supplier", "=", supplier])
		filters.append(["Category Table", "category_name", "=", category])
	elif supplier:
		filters.append(["supplier", "=", supplier])
	elif category:
		filters.append(["Category Table", "category_name", "=", category])
	elif parent and not is_root:
		filters.append(["parent_vendor_details", "=", parent])
	else:
		filters.append(['ifnull(`parent_vendor_details`, "")', "=", ""])

	tasks = frappe.get_list(
		doctype,
		fields=["name as value", "document_name as title", "is_group as expandable"],
		filters=filters
	)

	return tasks

@frappe.whitelist()
def add_node():
	from frappe.desk.treeview import make_tree_args
	args = frappe.form_dict
	args.update({
		"name_field": "document_name"
	})
	args = make_tree_args(**args)

	if args.parent_vendor_details == 'Vendor Details' or args.parent_vendor_details == args.supplier:
		args.parent_vendor_details = None

	frappe.get_doc(args).insert()

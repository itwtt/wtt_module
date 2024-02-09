# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet

class Testtree(NestedSet):
	pass


@frappe.whitelist()
def get_children(doctype, parent,department=None,project=None, is_root=False):	
	if is_root:
		parent = ""
	fields = ['name as value', 'subject as title','is_group as expandable']
	filters = [
		['docstatus', '<', '2'],
	]

	if project:
		filters.append(['project', '=', project])

	if department:
		filters.append(['department', '=', department])

	docs = frappe.get_list(doctype, fields=fields, filters=filters, order_by='name')
	return docs

@frappe.whitelist()
def add_node():
	from frappe.desk.treeview import make_tree_args
	args = frappe.form_dict
	args.update({
		"name_field": "subject"
	})
	args = make_tree_args(**args)

	if args.parent_project_documents == 'Project Documents' or args.parent_project_documents == args.project:
		args.parent_project_documents = None

	frappe.get_doc(args).insert()

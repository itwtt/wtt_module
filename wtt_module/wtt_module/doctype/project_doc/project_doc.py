# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet

class ProjectDoc(NestedSet):
	pass

@frappe.whitelist()
def get_children(doctype, parent,department=None,project=None, is_root=False):	
	filters = [["docstatus", "<", "2"]]
	if project and department:
		filters.append(["project", "=", project])
		filters.append(["department", "=", department])
	elif project:
		filters.append(["project", "=", project])
	elif department:
		filters.append(["department", "=", department])
	elif parent and not is_root:
		filters.append(["parent_project_doc", "=", parent])
	else:
		filters.append(['ifnull(`parent_project_doc`, "")', "=", ""])

	# if department:
	# 	filters.append(["department", "=", department])
	# elif parent and not is_root:
	# 	# via expand child
	# 	filters.append(["parent_project_doc", "=", parent])
	# else:
	# 	filters.append(['ifnull(`parent_project_doc`, "")', "=", ""])

	# if department:
	# 	filters.append(["department", "=", department])

	tasks = frappe.get_list(
		doctype,
		fields=["name as value", "document_name as title", "is_group as expandable"],
		filters=filters,
		order_by="name",
	)

	return tasks


	# if is_root:
	# 	parent = ""
	# fields = ['name as value', 'document_name as title','is_group as expandable']
	# filters = [
	# 	['docstatus', '<', '2'],
	# ]

	# if project:
	# 	filters.append(['project', '=', project])

	# if department:
	# 	filters.append(['department', '=', department])

	# docs = frappe.get_list(doctype, fields=fields, filters=filters, order_by='name')
	# return docs


@frappe.whitelist()
def add_node():
	from frappe.desk.treeview import make_tree_args
	args = frappe.form_dict
	args.update({
		"name_field": "document_name"
	})
	args = make_tree_args(**args)

	if args.parent_project_doc == 'Project Doc' or args.parent_project_doc == args.project:
		args.parent_project_doc = None

	frappe.get_doc(args).insert()

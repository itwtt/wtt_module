# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class DCTrack(Document):
	pass

@frappe.whitelist()
def update_mr_table(mr_no):
	ar=[]
	for i in frappe.db.sql("SELECT item_code,description,technical_description,qty,project,parent,name FROM `tabMaterial Request Item` WHERE parent='"+str(mr_no)+"'",as_dict=1):
		ar.append({
			'item_code':i.item_code,
			'description':i.description,
			'technical_description':i.technical_description,
			'qty':i.qty,
			'project':i.project,
			'material_request':i.parent,
			'mf_ref':i.name
		})
	return ar


@frappe.whitelist()
def get_mr(source_name,target_doc=None,args=None):
	if args is None:
		args = {}
	if isinstance(args, str):
		args = json.loads(args)

	def select_item(d):
		filtered_items = args.get("filtered_children", [])
		child_filter = d.name in filtered_items if filtered_items else True

		return child_filter

	doclist = get_mapped_doc(
		"Material Request",
		source_name,
		{
			"Material Request": {
				"doctype": "Dc Track",
				"validation": {"docstatus": ["=", 1]},
			},
			"Material Request Item": {
				"doctype": "DC Track Table",
				"field_map": [
					["name", "mr_ref"],
					["parent", "material_request"]
				],
				"condition": select_item,
			},
		},
		target_doc)

	return doclist
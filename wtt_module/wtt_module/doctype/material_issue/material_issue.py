from __future__ import unicode_literals

import json

import frappe
from frappe import _, msgprint
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cstr, flt, get_link_to_form, getdate, new_line_sep, nowdate
from six import string_types
from datetime import date,datetime,timedelta
from erpnext.buying.utils import check_on_hold_or_closed_status, validate_for_items
from erpnext.controllers.buying_controller import BuyingController
from erpnext.manufacturing.doctype.work_order.work_order import get_item_details
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.stock.stock_balance import get_indented_qty, update_bin_qty

class MaterialIssue(BuyingController):
	def on_submit(self):
		for i in self.items:
			for j in frappe.db.sql("SELECT mi_qty,qty FROM `tabMaterial Request Item` WHERE name='"+str(i.material_request_item)+"' and parent='"+str(i.material_request)+"' ",as_dict=1):
				if(j.mi_qty!=None):
					qt=j.mi_qty+i.qty
					qq=j.qty-qt
					frappe.db.sql("UPDATE `tabMaterial Request Item` SET mi_qty='"+str(qt)+"',bal_qty='"+str(qq)+"' WHERE name='"+str(i.material_request_item)+"' ",as_dict=1)

	def on_cancel(self):
		for i in self.items:
			for j in frappe.db.sql("SELECT mi_qty,qty,bal_qty FROM `tabMaterial Request Item` WHERE name='"+str(i.material_request_item)+"' and parent='"+str(i.material_request)+"' ",as_dict=1):
				if(j.mi_qty!=None):
					qt=j.mi_qty-i.qty
					qq=j.bal_qty+i.qty
					frappe.db.sql("UPDATE `tabMaterial Request Item` SET mi_qty='"+str(qt)+"',bal_qty='"+str(qq)+"' WHERE name='"+str(i.material_request_item)+"' ",as_dict=1)



@frappe.whitelist()
def update_status(name, status):
	material_request = frappe.get_doc('Material Issue', name)
	material_request.check_permission('write')
	material_request.update_status(status)

@frappe.whitelist()
def make_request(source_name, target_doc=None):
	def update_item(obj, source_parent, target):
		target.material_request_type="Material Issue"
		target.schedule_date=target.transaction_date
		for i in target.get("items"):
			i.schedule_date=target.transaction_date
			i.qty=obj.qty-obj.mi_qty
	doc = get_mapped_doc("Material Request", source_name, {
		"Material Request": {
			"doctype": "Material Issue",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map": {
				"name": "mr_no",
				"title":"title"
			}
		},
		"Material Request Item": {
			"doctype": "Material Issue Item",
			"field_map": {
				"bal_qty":"qty",
				"parent":"material_request",
				"name":"material_request_item"
			}
		},
		"postprocess": update_item,
		"condition": lambda doc: abs(doc.qty) != abs(doc.mi_qty)
	}, target_doc)
	return doc
# @frappe.whitelist()
# def make_stock_entry(source_name,target_doc=None):
# 	def update_item(obj, source_parent, target):
# 		target.stock_entry_type = "Material Transfer"
# 	doclist = get_mapped_doc("Material Issue", source_name,{
# 		"Material Issue": {
# 			"doctype": "Stock Entry"
# 		},
# 		"Material Issue Item": {
# 			"doctype": "Stock Entry Detail",
# 			"field_map": {
# 				"warehouse": "s_warehouse",
# 				"parent": "reference_material_issue",
# 				"name":"mi_item"
# 			}
# 		},
# 		"postprocess": update_item,
# 	}, target_doc)

# 	return doclist

@frappe.whitelist()
def make_stock_entry(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.stock_entry_type = "Material Transfer"
		target.from_warehouse = "Stores - WTT"
		target.to_warehouse = "SHOP FLOOR - WTT"
	def update_item(obj, source_parent, target):
		for i in target.get("items"):
			i.qty=obj.qty-obj.mi_qty
	doc = get_mapped_doc("Material Issue", source_name, {
		"Material Issue": {
			"doctype": "Stock Entry",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map": {
				"title":"title"
			}
		},
		"Material Issue Item": {
			"doctype": "Stock Entry Detail",
			"field_map": {
				"warehouse": "s_warehouse",
				"parent": "reference_material_issue",
				"name":"mi_item",
				"qty":"mi_qty"
			}
		},
		"postprocess": update_item,
		"condition": lambda doc: abs(doc.qty) != abs(doc.mi_qty)
	}, target_doc,set_missing_values)
	return doc
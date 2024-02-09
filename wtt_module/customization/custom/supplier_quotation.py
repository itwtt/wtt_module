# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, nowdate, add_days
from frappe.model.mapper import get_mapped_doc

from erpnext.controllers.buying_controller import BuyingController
from erpnext.buying.utils import validate_for_items
import json
import csv
import requests
form_grid_templates = {
	"items": "templates/form_grid/item_grid.html"
}

class SupplierQuotation(BuyingController):
	def validate(self):
		# # for rfq supplier submit only individual table append but comparison need combined table
		# if(self.combined_table==[] and self.supplier_data_table==[]):
		# 	for i in frappe.db.sql("SELECT item_code,sum(qty)as qty,uom,description,technical_description,rate,sum(amount)as amount,sum(price_list_rate)as price_list_rate,discount_percentage,discount_amount,item_tax_template,material_request FROM `tabSupplier Quotation Item` WHERE parent='"+str(self.name)+"' GROUP BY item_code ORDER BY technical_description",as_dict=1):
		# 		self.append("supplier_data_table",i)
		# 	for j in frappe.db.sql("SELECT item_code,sum(qty)as qty,uom,description,technical_description,rate as rate2,sum(amount)as amount2,sum(price_list_rate)as price_list_rate2,discount_percentage,discount_amount,item_tax_template,material_request FROM `tabSupplier Quotation Item` WHERE parent='"+str(self.name)+"' GROUP BY item_code ORDER BY technical_description",as_dict=1):
		# 		self.append("combined_table",j)

		super(SupplierQuotation, self).validate()
		if not self.status:
			self.status = "Draft"

		from erpnext.controllers.status_updater import validate_status
		validate_status(self.status, ["Draft", "Submitted", "Stopped",
			"Cancelled"])

		validate_for_items(self)
		self.validate_with_previous_doc()
		self.validate_uom_is_integer("uom", "qty")

	def on_submit(self):
		# for i in self.get("combined_table"):
		# 	if(i.approval=='Approved'):
		# 		frappe.db.sql("UPDATE `tabSupplier Quotation Item` SET quoted_qty='"+str(i.qty)+"',approval='"+str(i.approval)+"' WHERE item_code='"+str(i.item_code)+"' and parent='"+str(self.name)+"' ",as_dict=1)		
		frappe.db.set(self, "status", "Submitted")
		self.update_rfq_supplier_status(1)

	def on_cancel(self):
		frappe.db.set(self, "status", "Cancelled")
		self.update_rfq_supplier_status(0)

	def validate_with_previous_doc(self):
		super(SupplierQuotation, self).validate_with_previous_doc({
			"Material Request": {
				"ref_dn_field": "prevdoc_docname",
				"compare_fields": [["company", "="]],
			},
			"Material Request Item": {
				"ref_dn_field": "prevdoc_detail_docname",
				"compare_fields": [["item_code", "="], ["uom", "="]],
				"is_child_table": True
			}
		})
	def update_rfq_supplier_status(self, include_me):
		rfq_list = set([])
		for item in self.items:
			if item.request_for_quotation:
				rfq_list.add(item.request_for_quotation)
		for rfq in rfq_list:
			doc = frappe.get_doc('Request for Quotation', rfq)
			doc_sup = frappe.get_all('Request for Quotation Supplier', filters=
				{'parent': doc.name, 'supplier': self.supplier}, fields=['name', 'quote_status'])

			doc_sup = doc_sup[0] if doc_sup else None
			if not doc_sup:
				frappe.throw(_("Supplier {0} not found in {1}").format(self.supplier,
					"<a href='desk#Form/Request for Quotation/{0}'> Request for Quotation {0} </a>".format(doc.name)))

			quote_status = _('Received')
			for item in doc.items:
				sqi_count = frappe.db.sql("""
					SELECT
						COUNT(sqi.name) as count
					FROM
						`tabSupplier Quotation Item` as sqi,
						`tabSupplier Quotation` as sq
					WHERE sq.supplier = %(supplier)s
						AND sqi.docstatus = 1
						AND sq.name != %(me)s
						AND sqi.request_for_quotation_item = %(rqi)s
						AND sqi.parent = sq.name""",
					{"supplier": self.supplier, "rqi": item.name, 'me': self.name}, as_dict=1)[0]
				self_count = sum(my_item.request_for_quotation_item == item.name
					for my_item in self.items) if include_me else 0
				if (sqi_count.count + self_count) == 0:
					quote_status = _('Pending')
			if quote_status == _('Received') and doc_sup.quote_status == _('No Quote'):
				frappe.msgprint(_("{0} indicates that {1} will not provide a quotation, but all items \
					have been quoted. Updating the RFQ quote status.").format(doc.name, self.supplier))
				frappe.db.set_value('Request for Quotation Supplier', doc_sup.name, 'quote_status', quote_status)
				frappe.db.set_value('Request for Quotation Supplier', doc_sup.name, 'no_quote', 0)
			elif doc_sup.quote_status != _('No Quote'):
				frappe.db.set_value('Request for Quotation Supplier', doc_sup.name, 'quote_status', quote_status)

def get_list_context(context=None):
	from erpnext.controllers.website_list_for_contact import get_list_context
	list_context = get_list_context(context)
	list_context.update({
		'show_sidebar': True,
		'show_search': True,
		'no_breadcrumbs': True,
		'title': _('Supplier Quotation'),
	})

	return list_context

@frappe.whitelist()
def make_purchase_order(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.ignore_pricing_rule = 1
		target.run_method("set_missing_values")
		target.run_method("get_schedule_dates")
		target.run_method("calculate_taxes_and_totals")

	def update_item(obj, target, source_parent):
		target.stock_qty = flt(obj.qty) * flt(obj.conversion_factor)

	doclist = get_mapped_doc("Supplier Quotation", source_name,		{
		"Supplier Quotation": {
			"doctype": "Purchase Order",
			"validation": {
				"docstatus": ["=", 1],
			}
		},
		"Supplier Quotation Item": {
			"doctype": "Purchase Order Item",
			"field_map": [
				["name", "supplier_quotation_item"],
				["parent", "supplier_quotation"],
				["material_request", "material_request"],
				["material_request_item", "material_request_item"],
				["sales_order", "sales_order"]
			],
			"postprocess": update_item,
			"condition": lambda doc: doc.approval=="Approved" and doc.qty>0
		},
		"SQ Combined Table": {
			"doctype": "PO Combined Table",
			"field_map": [
				["price_list_rate2","price_list_rate"],
				["discount_percentage2","discount_percentage"],
				["discount_amount2","discount_amount"],
				["rate2","rate1"],
				["amount2","amount1"],
				["name", "sq_combined_item"],
				["parent", "supplier_quotation"],
				["material_request", "material_request"],
				["material_request_item", "material_request_item"],
				["sales_order", "sales_order"]
			],
			"postprocess": update_item,
			"condition": lambda doc: doc.approval=="Approved" and doc.qty>0
		},
		"Purchase Taxes and Charges": {
			"doctype": "Purchase Taxes and Charges",
		}
	}, target_doc, set_missing_values)

	return doclist

@frappe.whitelist()
def make_quotation(source_name, target_doc=None):
	doclist = get_mapped_doc("Supplier Quotation", source_name, {
		"Supplier Quotation": {
			"doctype": "Quotation",
			"field_map": {
				"name": "supplier_quotation",
			}
		},
		"Supplier Quotation Item": {
			"doctype": "Quotation Item",
			"condition": lambda doc: frappe.db.get_value("Item", doc.item_code, "is_sales_item")==1,
			"add_if_empty": True
		}
	}, target_doc)

	return doclist


@frappe.whitelist()
def set_rate(name):
	doc=frappe.get_doc("Supplier Quotation",name)
	for i in doc.combined_table:
		for sub in frappe.db.sql("SELECT name,qty from `tabSupplier Quotation Item` WHERE item_code='"+str(i.item_code)+"' ",as_dict=1):
			frappe.db.sql("UPDATE `tabSupplier Quotation Item` set price_list_rate='"+str(i.price_list_rate2)+"',discount_percentage='"+str(i.discount_percentage2)+"',discount_amount='"+str(i.discount_amount2)+"',rate='"+str(i.rate2)+"',amount='"+str(i.rate2*sub.qty)+"',supplier_description='"+str(i.supplier_description)+"' WHERE parent='"+str(name)+"' and item_code='"+str(i.item_code)+"' and name='"+str(sub.name)+"' ")
		
	return doc

@frappe.whitelist()
def get_data_from_excel(file_path):
	frappe.msgprint(str(file_path))
	flname = str(file_path)
	arr=[]
	val=[]
	v=[]
	with open(flname) as file_obj:
	    reader_obj = csv.reader(file_obj)
	    for row in reader_obj:
	        arr.append(row)

	    for j in range(len(arr)):
	        vals = {}
	        for k in range(len(arr[j])):
	            vals["col"+str(k)]=arr[j][k]
	        val.append(vals)
	frappe.msgprint(str(val))



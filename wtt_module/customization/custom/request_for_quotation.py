from __future__ import unicode_literals
import frappe, json
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import get_url, cint
from frappe.utils.user import get_user_fullname
from frappe.utils.print_format import download_pdf
from frappe.desk.form.load import get_attachments
from frappe.core.doctype.communication.email import make
from erpnext.accounts.party import get_party_account_currency, get_party_details
from erpnext.stock.doctype.material_request.material_request import set_missing_values
from erpnext.controllers.buying_controller import BuyingController
from erpnext.buying.utils import validate_for_items
from frappe.utils.xlsxutils import make_xlsx
import csv
from six import string_types
from frappe.utils import cstr, flt, cint
from erpnext.controllers.buying_controller import BuyingController
from erpnext.stock.doctype.item.item import get_last_purchase_details
from erpnext.stock.stock_balance import update_bin_qty, get_ordered_qty
from frappe.desk.notifications import clear_doctype_notifications
from erpnext.buying.utils import validate_for_items, check_on_hold_or_closed_status
from erpnext.stock.utils import get_bin
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.accounts.doctype.tax_withholding_category.tax_withholding_category import get_party_tax_withholding_details
from erpnext.accounts.doctype.sales_invoice.sales_invoice import (validate_inter_company_party,
	update_linked_doc, unlink_inter_company_doc)
from datetime import date,datetime,timedelta
import json
STANDARD_USERS = ("Guest", "Administrator")


# @frappe.whitelist()
# def create_supplier_quotation(doc):
# 	if isinstance(doc, string_types):
# 		doc = json.loads(doc)
# 	# frappe.msgprint(str(doc))
# 	try:
# 		sq_doc = frappe.get_doc({
# 			"doctype": "Supplier Quotation",
# 			"supplier": doc.get('supplier'),
# 			"terms": doc.get("terms"),
# 			"company": doc.get("company"),
# 			"request_for_quotation":doc.get("name"),
# 			"freight_terms":doc.get("fre"),
# 			"p_and_f":doc.get("p_f"),
# 			"delivary_time":doc.get("d_t"),
# 			"warranty":doc.get("war"),
# 			"price_basis":doc.get("price_basis"),
# 			"payment_terms":doc.get("p_t"),
# 			"currency": doc.get('currency') or get_party_account_currency('Supplier', doc.get('supplier'), doc.get('company')),
# 			"buying_price_list": doc.get('buying_price_list') or frappe.db.get_value('Buying Settings', None, 'buying_price_list')
# 		})
# 		add_items(sq_doc, doc.get('supplier'), doc.get('items'))
# 		sq_doc.flags.ignore_permissions = True
# 		sq_doc.run_method("set_missing_values")
# 		sq_doc.save()
# 		frappe.msgprint(_("Supplier Quotation {0} Created").format(sq_doc.name))
# 		return sq_doc.name
# 	except Exception:
# 		return None

# def add_items(sq_doc, supplier, items):
# 	for data in items:
# 		if data.get("qty") > 0:
# 			if isinstance(data, dict):
# 				data = frappe._dict(data)
# 			create_rfq_items(sq_doc, supplier, data)
				

# def create_rfq_items(sq_doc, supplier, data):
# 	args = {}
# 	for field in ['item_code', 'item_name', 'description', 'qty','amount', 'project', 'conversion_factor',
# 		'warehouse', 'material_request', 'material_request_item', 'stock_qty']:
# 		args[field] = data.get(field)
# 	dis_amt = data.discount_amount
# 	if(data.discount_amount==None):
# 		dis_amt=0
# 	args.update({
# 		"request_for_quotation_item": data.name,
# 		"request_for_quotation": data.parent,
# 		"price_list_rate":data.price_rate,
# 		"discount_percentage":data.dis,
# 		"discount_amount":dis_amt,
# 		"rate":data.price_rate - dis_amt,
# 		"item_tax_template":data.gst,
# 		"supplier_part_no": frappe.db.get_value("Item Supplier",
# 			{'parent': data.item_code, 'supplier': supplier}, "supplier_part_no")
# 	})

# 	sq_doc.append('items', args)


@frappe.whitelist()
def create_supplier_quotation(doc):
	if isinstance(doc, string_types):
		doc = json.loads(doc)
		sq_doc = frappe.get_doc({
			"doctype": "Supplier Quotation",
			"supplier": doc.get('supplier'),
			"request_for_quotation":doc.get('name'),
			"company": doc.get("company"),
			"freight_amount":doc.get("fre"),
			"p_and_f":doc.get("p_f"),
			"price_basis":doc.get("price_basis"),
			"delivary_time":doc.get("d_t"),
			"payment_terms":doc.get("p_t"),
			"warranty":doc.get("war"),
			"supplier_freight":doc.get("fre"),
			"supplier_p_and_f":doc.get("p_f"),
			"supplier_price_basis":doc.get("price_basis"),
			"supplier_delivary_time":doc.get("d_t"),
			"supplier_payment_terms":doc.get("p_t"),
			"supplier__warranty":doc.get("war"),
			"currency": doc.get('currency') or get_party_account_currency('Supplier', doc.get('supplier'), doc.get('company')),
			"buying_price_list": doc.get('buying_price_list') or frappe.db.get_value('Buying Settings', None, 'buying_price_list'),
			"total_qty":doc.get("total_qty"),
			"total":doc.get("grand_total"),
			"net_total":doc.get("grand_total")
		})
		add_items(sq_doc, doc.get('supplier'), doc.get('items'))
		sq_doc.flags.ignore_permissions = True
		sq_doc.run_method("set_missing_values")
		sq_doc.save()
		frappe.msgprint(_("Supplier Quotation {0} Created").format(sq_doc.name))
		return sq_doc.name

def add_items(sq_doc, supplier, items):
	# frappe.msgprint('gs')
	for data in items:
		if data.get("qty") > 0:
			if isinstance(data, dict):
				data = frappe._dict(data)
			create_rfq_items(sq_doc, supplier, data)

def create_rfq_items(sq_doc, supplier, data):
	if(data.dis==None):
		data.dis=0
	if(data.rate==None):
		data.rate=0
		
	sq_doc.append('supplier_data_table',{
	"item_code": data.item_code,
	"item_name": data.item_name,
	"description": data.description,
	"qty": data.qty,
	"rate": data.rate-((data.dis/100)*data.rate),
	"price_list_rate":data.rate,
	"discount_percentage":data.dis,
	"discount_amount":(data.dis/100)*data.rate,
	"item_tax_template":data.gst,
	"amount":data.amount,
	"supplier_description":data.des,
	"material_request":data.material_request
	})

	sq_doc.append('items',{
		"item_code": data.item_code,
		"item_name": data.item_name,
		"description": data.description,
		"qty": data.qty,
		"rate": data.rate-((data.dis/100)*data.rate),
		"price_list_rate":data.rate,
		"discount_percentage":data.dis,
		"discount_amount":(data.dis/100)*data.rate,
		"item_tax_template":data.gst,
		"warehouse":"Stores - WTT",
		"amount":data.amount,
		"supplier_description":data.des,
		"material_request":data.material_request,
		"material_request_item":data.material_request_item
	})
	
@frappe.whitelist()
def make_supplier_quotation_from_rfq(source_name, target_doc=None, for_supplier=None):
	def postprocess(source, target_doc):
		if for_supplier:
			target_doc.supplier = for_supplier
			args = get_party_details(for_supplier, party_type="Supplier", ignore_permissions=True)
			target_doc.currency = args.currency or get_party_account_currency('Supplier', for_supplier, source.company)
			target_doc.buying_price_list = args.buying_price_list or frappe.db.get_value('Buying Settings', None, 'buying_price_list')
		set_missing_values(source, target_doc)

	doclist = get_mapped_doc("Request for Quotation", source_name, {
		"Request for Quotation": {
			"doctype": "Supplier Quotation",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map": {
				"name": "request_for_quotation"
			}
		},
		"Request for Quotation Item": {
			"doctype": "Supplier Quotation Item",
			"field_map": {
				"name": "request_for_quotation_item",
				"parent": "request_for_quotation",
				"project_name":"project",
				"qty":"mr_qty"
			},
		},
		"RFQ Combined Table": {
			"doctype": "SQ Combined Table",
			"field_map": {
				"name": "request_for_quotation_item",
				"parent": "request_for_quotation",
				"qty":"mr_qty"
			},
		}
	}, target_doc, postprocess)
	return doclist


@frappe.whitelist()
def excel_for_supplier(val):
	data=[]
	doc=frappe.db.sql("SELECT cc.item_code,cc.item_name,cc.description,cc.technical_description,cc.qty,cc.uom FROM `tabRequest for Quotation Item`as cc,`tabRequest for Quotation`as pp WHERE cc.parent=pp.name and pp.name='"+str(val)+"' ",as_dict=1)
	for i in doc:
		if(i.technical_description!=None):
			data.append({
				"item_code":i.item_code,
				"description":i.description,
				"technical_description":i.technical_description,
				"qty":i.qty,
				"rate":"",
				"amount":""
				})
		else:
			data.append({
				"item_code":i.item_code,
				"description":i.description,
				"technical_description":"",
				"qty":i.qty,
				"rate":"",
				"amount":""
				})
	ur=[]
	xl=[["ITEM CODE","DESCRIPTION","TECHNICAL DECRIPTION","QTY","RATE","AMOUNT","SUPPLIER DESCRIPITION"]]

	for i in data:
		xl.append([i["item_code"],i["description"],i["technical_description"],i["qty"],i["rate"],i["amount"]])
	xlsx_file = make_xlsx(xl, "Quotation for WTT Link")
	file_data = xlsx_file.getvalue()

	_file = frappe.get_doc({
	"doctype": "File",
	"file_name": "Quoatation for WTT.xlsx",
	"folder": "Home/Attachments",
	"content": file_data})
	_file.save()
	ur.append({"url":_file.file_url})
	return ur


@frappe.whitelist()
def combine_table(doc):

	query = frappe.db.sql("SELECT distinct(item_code)as item_code,sum(qty)as qty,GROUP_CONCAT(distinct(material_request))as material_request,uom FROM `tabRequest for Quotation Item` WHERE parent='"+str(doc)+"' GROUP BY item_code ORDER BY technical_description",as_dict=1)
	rfq=frappe.get_doc("Request for Quotation",str(doc))
	rfq.combined_table = []
	for i in query:
		rfq.append("combined_table",i)
	rfq.save()

	return rfq

@frappe.whitelist()
def create_excel(doc,rfq):
	to_python = json.loads(doc)
	ur=[]
	xl=[["ITEM CODE","DESCRIPTION","TECHNICAL DESCRIPION","SUPPLIER DESCRIPTION","QTY","UOM","PRICE","DISCOUNT","DISCOUNT AMOUNT","RATE(per qty)","AMOUNT"]]
	for i in to_python:
		xl.append([i["item_code"],i["description"],i["technical_description"],"",i["qty"],i["uom"],0,0,'=G2*H2/100','=G2-I2','=J2*E2'])

	xlsx_file = make_xlsx(xl, "RFQ")
	file_data = xlsx_file.getvalue()
	_file = frappe.get_doc({
	"doctype": "File",
	"file_name": str(rfq)+".xlsx",
	"folder": "Home/Attachments",
	"content": file_data})
	
	_file.save()
	ur.append({"url":_file.file_url})
	return ur
from __future__ import unicode_literals
import frappe
import json
from frappe.utils import cstr, flt, cint,getdate
from frappe import msgprint, _
from frappe.model.mapper import get_mapped_doc
from erpnext.controllers.buying_controller import BuyingController
from erpnext.stock.doctype.item.item import get_last_purchase_details
from erpnext.stock.stock_balance import update_bin_qty, get_ordered_qty
from frappe.desk.notifications import clear_doctype_notifications
from erpnext.buying.utils import validate_for_items, check_on_hold_or_closed_status
from erpnext.stock.utils import get_bin
from erpnext.accounts.party import get_party_account_currency
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.accounts.doctype.tax_withholding_category.tax_withholding_category import get_party_tax_withholding_details
from erpnext.accounts.doctype.sales_invoice.sales_invoice import (validate_inter_company_party,
	update_linked_doc, unlink_inter_company_doc)

from datetime import date,datetime,timedelta
from frappe.utils.xlsxutils import make_xlsx
from pytz import timezone
from frappe.utils.background_jobs import enqueue

from erpnext.buying.doctype.purchase_order.purchase_order import PurchaseOrder

class customPO(PurchaseOrder):
	def validate(self):
		super().validate()

		if(self.naming_series=='JOB-.YY.-' or self.naming_series=="SER-.YY.-"):
			pass
		else:
			vvqty=0
			for i in self.items:
				mr_qty = frappe.db.get_value("Material Request Item",i.material_request_item,"qty")
				ordered_qty = frappe.db.get_value("Material Request Item",i.material_request_item,"ordered_qty")
				if(ordered_qty):
					ordered_qty=ordered_qty
				else:
					ordered_qty=0
				q = frappe.db.sql("SELECT po.name,poi.qty FROM `tabPurchase Order Item` as poi INNER JOIN `tabPurchase Order` as po on po.name=poi.parent WHERE poi.material_request_item='"+str(i.material_request_item)+"' and po.name!='"+str(self.name)+"' and po.workflow_state!='Approved' and po.workflow_state!='Rejected' and po.workflow_state!='Cancelled'",as_dict=1)
				if q:
					for k in q:
						vvqty=vvqty+(k.qty + i.qty)
				
				if((mr_qty+ordered_qty)<vvqty):
					if(self.remove_qty_restriction == 1):
						pass
					else:
						frappe.throw("The row "+str(i.idx)+" item already link with another PO")
				else:
					pass

		if(self.naming_series=="SER-.YY.-"):
			for i in frappe.db.sql("SELECT GROUP_CONCAT(distinct(service_request)) as service_request FROM `tabPurchase Order Item` WHERE parent='"+str(self.name)+"' ",as_dict=1):
				self.service_request=i.service_request


		pr=[]
		for i in frappe.db.sql("SELECT distinct(project) FROM `tabPurchase Order Item` WHERE parent='"+str(self.name)+"' ",as_dict=1):
			pr.append(i.project)
		if(len(pr)>1):
			frappe.throw("Order must be raised for single Project")
		if(self.workflow_state=='Approved by HOD' and self.approved_hod==None):
			self.approved_hod=frappe.session.user
		if(self.naming_series=='JOB-.YY.-'):
			aa=str(self.name)
			self.po=aa[7:]
		else:
			aa=str(self.name)
			self.po=aa[6:]
		if(self.workflow_state=="Rejected"):
			if(self.rejected_reason_hod==""):
				frappe.throw("Kindly Give Reason for Rejection")

		mr=[]
		pr=[]
		temp_list=[]
		temp_list1=[]
		for i in self.items:
			temp_list.append(i.material_request)
			temp_list1.append(i.project)
		unique_item = set(temp_list)
		unique_item1 = set(temp_list1)

		for j in unique_item:
			mr.append(j)

		for k in unique_item1:
			pr.append(k)

		str1 = ','.join(str(e) for e in mr)
		str2 = ','.join(str(f) for f in pr)

		self.material_series=str1
		self.project=str2

	def on_submit(self):
		super().on_submit()
		# if(self.naming_series=='PO-.YY.-'):
		# 	message="Dear sir ,<br> PO has been Approved Against the MR <br>PO NO: "+str(self.name)+"<br>MR NO: "+str(self.material_series)+""
		# 	password = None
		# 	email_args = {
		# 		"recipients": ["design-1@wttindia.com","design-2@wttindia.com","design-3@wttindia.com"],
		# 		"message": message,
		# 		"subject": "PO has been approved"
		# 		}
		# 	if not frappe.flags.in_test:
		# 		enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
		# 	else:
		# 		frappe.sendmail(**email_args)
			
		today = date.today()
		ead=(today)-timedelta(days=2)
		count=0
		if(frappe.session.user=='purchase@wttindia.com'):
			if(self.rounded_total>10000):
				frappe.throw("The Po amount  is cross the limit. (>10000).")
			ddoc1 = frappe.db.sql("SELECT count(name)as po from `tabPurchase Order` WHERE workflow_state='Emergency Approval' and name!='"+str(self.name)+"' and approver='"+str(frappe.session.user)+"' ",as_dict=1)
			if(ddoc1):
				count+=ddoc1.po
			ddoc = frappe.db.sql("SELECT name from `tabPurchase Order` WHERE workflow_state='Emergency Approval' and approved_date<='"+str(ead)+"' and name!='"+str(self.name)+"' and approver='"+str(frappe.session.user)+"' ",as_dict=1)
			if(ddoc or count>1):
				frappe.throw("Please get the approval from MD for Previous Record")
		if(self.naming_series=='JOB-.YY.-'):
			aa=str(self.name)
			self.po=aa[7:]
		else:
			aa=str(self.name)
			self.po=aa[6:]

		if(self.approved_date1==None):
			date1=frappe.get_doc("Purchase Order",self.name)
			date1.approved_date1=str(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d'))
			date1.approved_time1=str(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'))
			date1.approver=frappe.session.user
			date1.submit()

	def on_cancel(self):
		super().on_cancel()
		# if(self.rejected_reason_md==""):
		# 	frappe.throw("Kindly Give Reason for Rejection")
		# doc=frappe.db.sql("UPDATE `tabOrder Status` SET `po_status`='"+str(self.workflow_state)+"' WHERE po_no='"+str(self.name)+"'")

	def on_update(self):
		ar=[]
		for i in frappe.db.sql("SELECT DISTINCT(project)as project FROM `tabPurchase Order Item` WHERE parent='"+str(self.name)+"' ",as_dict=1):
			ar.append(i.project)
		if(len(ar)>1):
			frappe.throw("PO should not be raid for multiple Project")

	@frappe.whitelist(allow_guest=True)
	def download_table(self):
		ur=[]
		xl=[["Item Code","Description","Technical Description","Supplier Description","MR Qty","Qty","UOM","Price List","Discount Percentage","Discount Amount","Rate","Amount","MR No","MR Reference"]]
		for i in self.items:
			xl.append([i.item_code,i.description,i.technical_description,i.supplier_description,i.required_qty,i.qty,i.uom,i.price_list_rate,i.discount_percentage,i.discount_amount,i.rate,i.amount,i.material_request,i.material_request_item])
		xlsx_file = make_xlsx(xl,"ChildTable")
		file_data = xlsx_file.getvalue()
		_file = frappe.get_doc({
		"doctype": "File",
		"file_name":"ChildTable.xlsx",
		"folder": "Home/Attachments",
		"content": file_data})
		_file.save()
		ur.append({"url":_file.file_url})
		return ur

@frappe.whitelist()
def set_missing_values(source, target):
	target.run_method("set_missing_values")
	target.run_method("calculate_taxes_and_totals")
@frappe.whitelist()
def make_purchase_receipt(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		target.qty = flt(obj.qty) - flt(obj.received_qty)
		target.invoice_qty = flt(obj.qty) - flt(obj.received_qty)
		target.stock_qty = (flt(obj.qty) - flt(obj.received_qty)) * flt(obj.conversion_factor)
		target.amount = (flt(obj.qty) - flt(obj.received_qty)) * flt(obj.rate)
		target.base_amount = (flt(obj.qty) - flt(obj.received_qty)) * \
			flt(obj.rate) * flt(source_parent.conversion_rate)
	def select_item(d):
		filtered_items = args.get("filtered_children", [])
		child_filter = d.name in filtered_items if filtered_items else True

		return d.received_qty < d.qty and d.delivered_by_supplier!=1 and child_filter
	doc = get_mapped_doc("Purchase Order", source_name,	{
		"Purchase Order": {
			"doctype": "Purchase Receipt",
			"field_map": {
				"supplier_warehouse":"supplier_warehouse"
			},
			"validation": {
				"docstatus": ["=", 1],
			}
		},
		"Purchase Order Item": {
			"doctype": "Purchase Receipt Item",
			"field_map": {
				"name": "purchase_order_item",
				"parent": "purchase_order",
				"bom": "bom",
				"required_qty":"to_be_received",
				"qty":"po_qty",
				"material_request": "material_request",
				"material_request_item": "material_request_item",
				"reject_reason":"reject_reason"
			},
			"postprocess": update_item,
			"condition": lambda doc: abs(doc.received_qty) < abs(doc.qty) and doc.delivered_by_supplier!=1
			# "condition":select_item
		},
		"PO Combined Table":{
			"doctype":"PR Combined Table",
			"field_map": [
				["name", "po_combined_item"],
				["parent", "purchase_order"]
			],
		},
		"Purchase Taxes and Charges": {
			"doctype": "Purchase Taxes and Charges",
			"add_if_empty": True
		}
	}, target_doc, set_missing_values)

	return doc

@frappe.whitelist()
def make_subcontracting_order(source_name, target_doc=None):
	return get_mapped_subcontracting_order(source_name, target_doc)


def get_mapped_subcontracting_order(source_name, target_doc=None):

	if target_doc and isinstance(target_doc, str):
		target_doc = json.loads(target_doc)
		for key in ["service_items", "items", "supplied_items"]:
			if key in target_doc:
				del target_doc[key]
		target_doc = json.dumps(target_doc)

	target_doc = get_mapped_doc(
		"Purchase Order",
		source_name,
		{
			"Purchase Order": {
				"doctype": "Subcontracting Order",
				"field_map": {},
				"field_no_map": ["total_qty", "total", "net_total"],
				"validation": {
					"docstatus": ["=", 1],
				},
			},
			"Purchase Order Item": {
				"doctype": "Subcontracting Order Service Item",
				"field_map": {},
				"field_no_map": [],
			},
		},
		target_doc,
	)

	target_doc.populate_items_table()

	if target_doc.set_warehouse:
		for item in target_doc.items:
			item.warehouse = target_doc.set_warehouse
	else:
		source_doc = frappe.get_doc("Purchase Order", source_name)
		if source_doc.set_warehouse:
			for item in target_doc.items:
				item.warehouse = source_doc.set_warehouse
		else:
			for idx, item in enumerate(target_doc.items):
				item.warehouse = source_doc.items[idx].warehouse

	target_doc.save()

	return target_doc

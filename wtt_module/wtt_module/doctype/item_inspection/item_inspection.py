# Copyright (c) 2021, wtt_custom and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import cstr, cint, flt, comma_or, getdate, nowdate, formatdate, format_time, get_link_to_form
from erpnext.stock.doctype.quality_inspection_template.quality_inspection_template import get_template_details
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cstr, cint, flt, comma_or, getdate, nowdate, formatdate, format_time

class ItemInspection(Document):
	def on_submit(self):
		if(self.is_subcontracted==1):
			frappe.db.sql("UPDATE `tabSubcontracting Receipt` SET `total_qty`='"+str(self.total_qty)+"',`total`='"+str(self.total)+"' WHERE `name`='" +self.receipt_series+"'")
			doc=frappe.get_doc("Subcontracting Receipt",self.subcontracting_receipt)
			if(doc.docstatus==0):
				for item in self.get("items"):
					for i in doc.get("items"):
						if (i.name==item.subcontracting_receipt_item):
							i.qty = item.acc_qty
							i.rejected_qty = item.rej_qty
							i.inspected_qty = item.acc_qty
							i.warehouse=item.s_warehouse
							i.quantity_status="Accepted"
							i.item_inspection=self.name
							if(item.rej_qty>0):
								if(item.rejected_warehouse==None):
									frappe.throw("Give the reason for rejection "+str(item.description))
								else:
									i.rejected_warehouse=item.s_warehouse
			doc.submit()
			frappe.db.sql("UPDATE `tabPurchase Receipt Item` SET item_inspection='"+str(self.name)+"' WHERE parent='"+str(self.receipt_series)+"' ")
		# elif(self.receipt_series in ['PR-23-00598','PR-23-00564','PR-23-00605','PR-23-00592']):
		# 	for i in self.items:
		# 		frappe.db.sql("""UPDATE `tabPurchase Receipt Item` set 
		# 			qty='"""+str(acc_qty)+"""',
		# 			rejected_qty='"""+str(i.rej_qty)+"""',
		# 			return_qty='"""+str(i.acc_qty)+"""',
		# 			warehouse='"""+str(i.s_warehouse)+"""',
		# 			quantity_status='Accepted'
		# 			item_inspection='"""+str(self.name)+"""'
		# 			 """)
		# 	doc=frappe.get_doc("Purchase Receipt",self.receipt_series)
		# 	for item in self.get("items"):
		# 		for i in doc.get("items"):
		# 			if (i.name==item.pr_item):
		# 				if(item.rej_qty>0):
		# 					if(item.rejected_warehouse==None):
		# 						frappe.throw("Give the reason for rejection "+str(item.description))
		# 					else:
		# 						i.rejected_warehouse=item.s_warehouse
		# 		doc.save()
			# frappe.db.sql("UPDATE `tabPurchase Receipt Item` set item_inspection='"+str(self.name)+"',return_qty=qty WHERE parent='"+str(self.receipt_series)+"' ")

		else:
			frappe.db.sql("UPDATE `tabPurchase Receipt` SET `total_qty`='"+str(self.total_qty)+"',`total`='"+str(self.total)+"',`base_total`='"+str(self.total)+"',`net_total`='"+str(self.total)+"' WHERE `name`='" +self.receipt_series+"'")
			doc=frappe.get_doc("Purchase Receipt",self.receipt_series)
			for item in self.get("items"):
				for i in doc.get("items"):
					if (i.name==item.pr_item):
						i.qty = item.acc_qty
						i.rejected_qty = item.rej_qty
						i.return_qty = item.acc_qty
						i.warehouse=item.s_warehouse
						i.quantity_status="Accepted"
						i.item_inspection=self.name
						if(item.rej_qty>0):
							if(item.rejected_warehouse==None):
								frappe.throw("Give the reason for rejection "+str(item.description))
							else:
								i.rejected_warehouse=item.s_warehouse
			doc.save()

	def on_cancel(self):
		if(self.is_subcontracted==0):
			for i in self.get("items"):
				frappe.db.sql("UPDATE `tabPurchase Receipt Item` SET item_inspection = NULL WHERE item_inspection='"+str(self.name)+"' and name='"+str(i.pr_item)+"'",as_dict=1)
		# 	if(frappe.db.exists("Purchase Receipt", {"name": self.receipt_series, "docstatus": 0 })):
		# 		for item in self.items:
		# 			doc=frappe.get_doc("Purchase Receipt",self.receipt_series)
		# 			for i in doc.get("items"):
		# 				if (i.name==item.pr_item):
		# 					i.qty=item.acc_qty+item.rej_qty
		# 					i.rejected_qty=i.rejected_qty-item.rej_qty
		# 					i.return_qty=i.return_qty-item.acc_qty
		# 					i.warehouse='Stores - WTT'
		# 					i.rejeced_warehouse=None
		# 			doc.save()
		else:
			for i in self.get("items"):
				frappe.db.sql("UPDATE `tabSubcontracting Receipt Item` SET item_inspection = NULL WHERE item_inspection='"+str(self.name)+"' and name='"+str(i.subcontracting_receipt_item)+"'",as_dict=1)
		# 	if(frappe.db.exists("Subcontracting Receipt", {"name": self.subcontracting_receipt, "docstatus": 0 })):
		# 		for item in self.items:
		# 			doc=frappe.get_doc("Subcontracting Receipt",self.subcontracting_receipt)
		# 			for i in doc.get("items"):
		# 				if (i.name==item.subcontracting_receipt_item):
		# 					i.qty=item.acc_qty+item.rej_qty
		# 					i.rejected_qty=i.rejected_qty-item.rej_qty
		# 					i.inspected_qty=i.inspected_qty-item.acc_qty
		# 					i.warehouse='Stores - WTT'
		# 					i.rejeced_warehouse=None
		# 			doc.save()
		frappe.db.sql("UPDATE `tabItem Inspection item` SET subcontracting_receipt = NULL, subcontracting_receipt_item= NULL WHERE parent='"+str(self.name)+"' ",as_dict=1)

@frappe.whitelist()
def make_quality_inspection(source_name, target_doc=None):
	def postprocess(source, doc):
		doc.inspected_by = frappe.session.user
		doc.get_quality_inspection_template()
	doc = get_mapped_doc("BOM", source_name, {
		'BOM': {
			"doctype": "Quality Inspection",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map": {
				"name": "bom_no",
				"item": "item_code",
				"stock_uom": "uom",
				"stock_qty": "qty"
			},
		}
	}, target_doc, postprocess)
	return doc

@frappe.whitelist()
def make_quality(source_name, target_doc=None):
	doc = get_mapped_doc("Quality Inspection", source_name, {
		"Quality Inspection": {
			"doctype": "Stock Entry",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Quality Inspection Item": {
			"doctype": "Stock Entry Detail",
			"field_map": {
				"stock_qty": "transfer_qty",
				"batch_no": "batch_no",
				"rate":"basic_rate",
				"acc_qty":"qty"
			},
			"condition": lambda doc: doc.ins_status=="Accepted"
		}
	}, target_doc)
	return doc

	
@frappe.whitelist()
def revision(name):
	val = frappe.db.set_value("Item Inspection",name,'workflow_state','Approved')
	val1 = frappe.db.set_value("Item Inspection",name,'docstatus',1)
	doc=frappe.get_doc("Purchase Receipt","PR-22-00375-1")
	for i in doc.items:
		i.qty=i.accepted_qty
		# qty=i.qty-i.accepted_qty
		# if(i.accepted_qty>0):
		# 	frappe.db.sql("UPDATE `tabPurchase Receipt Item` SET rejected_qty='"+str(qty)+"',warehouse='Stores - WTT' WHERE name='"+str(i.name)+"' and parent='PR-22-00375-1' ",as_dict=1)
		# if(i.rejected_qty>0):
			# frappe.db.sql("UPDATE `tabPurchase Receipt Item` SET rejected_warehouse='Stores - WTT' WHERE name='"+str(i.name)+"' and parent='PR-22-00375-1' ",as_dict=1)
	doc.save()
	
	frappe.db.commit()
	frappe.msgprint("Done")


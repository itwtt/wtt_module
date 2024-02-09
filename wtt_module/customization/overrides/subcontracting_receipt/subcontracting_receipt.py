import frappe
from frappe import _
from frappe.utils import cint, flt, getdate, nowdate

import erpnext
from erpnext.accounts.utils import get_account_currency
from erpnext.controllers.subcontracting_controller import SubcontractingController
from frappe.model.mapper import get_mapped_doc

from erpnext.subcontracting.doctype.subcontracting_receipt.subcontracting_receipt import SubcontractingReceipt


class customSCR(SubcontractingReceipt):
	pass

@frappe.whitelist()
def make_quality(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		target.is_subcontracted=1
	# 	if(obj.rejected_qty==0):
	# 		target.qty = flt(obj.qty) - flt(obj.inspected_qty)
	# 		target.amount = (flt(obj.qty) - flt(obj.inspected_qty)) * flt(obj.rate)
	# 		target.base_amount = (flt(obj.qty) - flt(obj.inspected_qty)) * \
	# 			flt(obj.rate) * flt(source_parent.conversion_rate)
	# 	else:
	# 		target.qty = flt(obj.rejected_qty)
	# 		target.amount = flt(obj.rejected_qty) * flt(obj.rate)
	# 		target.base_amount = flt(obj.rejected_qty) * \
	# 			flt(obj.rate) * flt(source_parent.conversion_rate)	
	doc = get_mapped_doc("Subcontracting Receipt", source_name, {
		"Subcontracting Receipt": {
			"doctype": "Item Inspection",
			"validation": {
				"docstatus": ["=", 0]
			},
			"field_map": {
				"name": "subcontracting_receipt"
			},
			"postprocess": update_item,
		},
		"Subcontracting Receipt Item": {
			"doctype": "Item Inspection item",
			"field_map": {
				"parent":"subcontracting_receipt",
				"name":"subcontracting_receipt_item",
				"received_qty":"qty"
			},
			"condition": lambda doc: abs(doc.received_qty) != abs(doc.inspected_qty)
		}
	}, target_doc)

	return doc
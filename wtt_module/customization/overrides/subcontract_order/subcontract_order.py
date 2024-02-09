

import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt

from erpnext.buying.doctype.purchase_order.purchase_order import is_subcontracting_order_created
from erpnext.controllers.subcontracting_controller import SubcontractingController
from erpnext.stock.stock_balance import get_ordered_qty, update_bin_qty
from erpnext.stock.utils import get_bin



from erpnext.subcontracting.doctype.subcontracting_order.subcontracting_order import SubcontractingOrder


class SubcontractingOrderCustom(SubcontractingOrder):
	def validate(self):
		super().validate()


@frappe.whitelist()
def make_request(source_name, target_doc=None):
	def postprocess(source, target):
		target.purpose="Job Order",
		target.set_warehouse=source.to_warehouse
		# target.posting_date=target.posting_date
		# for i in target.get("items"):
		# 	i.posting_date=target.posting_date
	doc = get_mapped_doc("Job Order", source_name, {
		"Job Order": {
			"doctype": "Subcontracting Order",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map": {
				"from_warehouse":"source_warehouse",
				"to_warehouse":"target_warehouse"
			}
		},
		"Job Order Table": {
			"doctype": "Subcontracting Order Service Item"
		}
	}, target_doc,postprocess)
	return doc
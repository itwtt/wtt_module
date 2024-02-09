# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cstr, flt, get_link_to_form, getdate, new_line_sep, nowdate
from six import string_types

from erpnext.buying.utils import check_on_hold_or_closed_status, validate_for_items
from erpnext.controllers.buying_controller import BuyingController
from erpnext.manufacturing.doctype.work_order.work_order import get_item_details
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.stock.stock_balance import get_indented_qty, update_bin_qty

class JobOrder(BuyingController):
	def validate(self):
		self.total_incoming_value = self.total_outgoing_value = 0.0
		for d in self.get("items"):
			d.t_warehouse1=self.to_warehouse
			if d.t_warehouse1:
				self.total_incoming_value += flt(d.amount)
			if d.s_warehouse1:
				self.total_outgoing_value += flt(d.amount)

		self.value_difference = self.total_outgoing_value - self.total_incoming_value

	def on_submit(self):
		pass	
		# doc=frappe.new_doc("Stock Entry")
		# doc.stock_entry_type="Material Transfer"
		# doc.from_warehouse=self.from_warehouse
		# doc.to_warehouse=self.to_warehouse
		# # doc.total_incoming_value=self.total_incoming_value
		# # doc.total_outgoing_value=self.total_outgoing_value
		# doc.value_difference=self.value_difference
		# doc.project=self.project
		# doc.remark=self.remarks
		# for i in self.get("items"):
		# 	doc.append("items",{
		# 		# "s_warehouse":i.s_warehouse1,
		# 		# "t_warehouse":i.t_warehouse1,
		# 		"item_code":i.item_code,
		# 		"qty":i.qty,
		# 		"valuation_rate":i.valuation_rate,
		# 		"inspection_status":i.inspection_status,
		# 		"allow_zero_valuation_rate":i.allow_zero_valuation_rate,
		# 		"project":i.project,
		# 		"uom":i.uom
		# 		})
		# doc.submit()
		# frappe.db.commit()
		# frappe.msgprint("done")

@frappe.whitelist()
def make_request(source_name, target_doc=None):
	def postprocess(source, target):
		#target.job_order_type="Job Order"
		# target.posting_date=target.posting_date
		for i in target.get("items"):
			i.posting_date=target.posting_date
	doc = get_mapped_doc("Stock Entry", source_name, {
		"Stock Entry": {
			"doctype": "Job Order",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map": {
				"to_warehouse": "from_warehouse"
			}
		},
		"Stock Entry Detail": {
			"doctype": "Job Order Table",
			"field_map": {
				"stock_accepted": "qty",
				"t_warehouse":"s_warehouse1",
				"parent":"against_stock_entry",
				"name":"ste_detail"
			}
		}
	}, target_doc,postprocess)
	return doc



import json
from collections import defaultdict

import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.query_builder.functions import Sum
from frappe.utils import (
	cint,
	comma_or,
	cstr,
	flt,
	format_time,
	formatdate,
	getdate,
	month_diff,
	nowdate,
)

import erpnext
from erpnext.accounts.general_ledger import process_gl_map
from erpnext.controllers.taxes_and_totals import init_landed_taxes_and_totals
from erpnext.manufacturing.doctype.bom.bom import add_additional_cost, validate_bom_no
from erpnext.setup.doctype.brand.brand import get_brand_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.stock.doctype.batch.batch import get_batch_no, get_batch_qty, set_batch_nos
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.stock.doctype.serial_no.serial_no import (
	get_serial_nos,
	update_serial_nos_after_submit,
)
from erpnext.stock.doctype.stock_reconciliation.stock_reconciliation import (
	OpeningEntryAccountError,
)
from erpnext.stock.get_item_details import (
	get_bin_details,
	get_conversion_factor,
	get_default_cost_center,
	get_reserved_qty_for_so,
)
from erpnext.stock.stock_ledger import NegativeStockError, get_previous_sle, get_valuation_rate
from erpnext.stock.utils import get_bin, get_incoming_rate


class FinishedGoodError(frappe.ValidationError):
	pass


class IncorrectValuationRateError(frappe.ValidationError):
	pass


class DuplicateEntryForWorkOrderError(frappe.ValidationError):
	pass


class OperationsNotCompleteError(frappe.ValidationError):
	pass


class MaxSampleAlreadyRetainedError(frappe.ValidationError):
	pass


from erpnext.controllers.stock_controller import StockController
import traceback

form_grid_templates = {"items": "templates/form_grid/stock_entry_grid.html"}

from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry
class customStockEntry(StockEntry):
	def on_submit(self):
		super().on_submit()
		try:
			if(self.stock_entry_type in ["Send to Subcontractor","Material Receipt"]):
				for i in self.items:
					if(i.po_job_order!=None and i.po_job_order_item!=None):
						if(self.stock_entry_type=="Send to Subcontractor"):
							frappe.db.sql("UPDATE `tabRaw Materials Purchase Order` set transfered_qty=`tabRaw Materials Purchase Order`.`transfered_qty`+"+str(i.qty)+" WHERE parent='"+str(i.po_job_order)+"' and name='"+str(i.po_job_order_item)+"' ")
							frappe.db.sql("UPDATE `tabRaw Materials Job Order Request` set transfered_qty=`tabRaw Materials Job Order Request`.`transfered_qty`+"+str(i.qty)+" WHERE parent='"+str(i.job_order_request)+"' and name='"+str(i.job_order_request_item)+"' ")
						elif(self.stock_entry_type=="Material Receipt"):
							frappe.db.sql("UPDATE `tabPurchase Order Item` set fg_item_received_qty=`tabPurchase Order Item`.`fg_item_received_qty`+"+str(i.qty)+" WHERE parent='"+str(i.po_job_order)+"' and name='"+str(i.po_job_order_item)+"' ")
							frappe.db.sql("UPDATE `tabJob Order Table` set received_qty=`tabJob Order Table`.`received_qty`+"+str(i.qty)+" WHERE parent='"+str(i.job_order_request)+"' and name='"+str(i.job_order_request_item)+"' ")
			if(self.stock_entry_type in ["Send to Subcontractor","Material Receipt"]):
				self.update_status_jor()
		except Exception as e:
			error_message = f"An error occurred: {str(e)} (Line {traceback.extract_tb(e.__traceback__)[0].lineno})"
			frappe.throw(str(error_message))
	def on_cancel(self):
		super().on_cancel()
		try:
			if(self.stock_entry_type in ["Send to Subcontractor","Material Receipt"]):
				for i in self.items:
					if(i.po_job_order!=None and i.po_job_order_item!=None):
						if(self.stock_entry_type=="Send to Subcontractor"):
							frappe.db.sql("UPDATE `tabRaw Materials Purchase Order` set transfered_qty=`tabRaw Materials Purchase Order`.`transfered_qty`-"+str(i.qty)+" WHERE parent='"+str(i.po_job_order)+"' and name='"+str(i.po_job_order_item)+"' ")
							frappe.db.sql("UPDATE `tabRaw Materials Job Order Request` set transfered_qty=`tabRaw Materials Job Order Request`.`transfered_qty`-"+str(i.qty)+" WHERE parent='"+str(i.job_order_request)+"' and name='"+str(i.job_order_request_item)+"' ")
						elif(self.stock_entry_type=="Material Receipt"):
							frappe.db.sql("UPDATE `tabPurchase Order Item` set fg_item_received_qty=`tabPurchase Order Item`.`fg_item_received_qty`-"+str(i.qty)+" WHERE parent='"+str(i.po_job_order)+"' and name='"+str(i.po_job_order_item)+"' ")
							frappe.db.sql("UPDATE `tabJob Order Table` set received_qty=`tabJob Order Table`.`received_qty`-"+str(i.qty)+" WHERE parent='"+str(i.job_order_request)+"' and name='"+str(i.job_order_request_item)+"' ")
			if(self.stock_entry_type in ["Send to Subcontractor","Material Receipt"]):
				self.update_status_jor()
		except Exception as e:
			error_message = f"An error occurred: {str(e)} (Line {traceback.extract_tb(e.__traceback__)[0].lineno})"
			frappe.throw(str(error_message))
	def update_status_jor(self):
		jor=[]
		for i in self.items:
			if(i.job_order_request not in jor and i.job_order_request!=None and i.job_order_request_item!=None):
				jor.append(i.job_order_request)
		if(len(jor)>0):
			for jor_name in jor:
				sts='Pending'
				if(self.stock_entry_type=="Send to Subcontractor"):
					q=frappe.db.sql("""SELECT sum(joi.qty) as qty, sum(joi.transfered_qty)as tqty
						FROM `tabJob Order Request`as jo INNER JOIN `tabRaw Materials Job Order Request`as joi on jo.name=joi.parent 
						WHERE jo.name='"""+str(jor_name)+"""' """,as_dict=1)
					if q:
						if(float(q[0].tqty>=float(q[0].qty))):
							sts='Transferred'
						elif(float(q[0].tqty)>0 and float(q[0].tqty)<float(q[0].qty)):
							sts='Partially Transferred'

				elif(self.stock_entry_type=="Material Receipt"):
					q=frappe.db.sql("""SELECT sum(joi.qty) as qty, sum(joi.received_qty)as rqty
						FROM `tabJob Order Request`as jo INNER JOIN `tabJob Order Table`as joi on jo.name=joi.parent 
						WHERE jo.name='"""+str(jor_name)+"""' """,as_dict=1)
					if q:
						if(float(q[0].rqty>=float(q[0].qty))):
							sts='Completed'

						elif(float(q[0].rqty)>0 and float(q[0].rqty)<float(q[0].qty)):
							sts='Partially Received'
				frappe.db.sql("UPDATE `tabJob Order Request` set status='"+str(sts)+"' WHERE name='"+str(jor_name)+"' ")



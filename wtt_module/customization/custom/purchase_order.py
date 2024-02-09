# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

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

form_grid_templates = {
	"items": "templates/form_grid/item_grid.html"
}

class PurchaseOrder(BuyingController):
	def __init__(self, *args, **kwargs):
		super(PurchaseOrder, self).__init__(*args, **kwargs)
		self.status_updater = [{
			'source_dt': 'Purchase Order Item',
			'target_dt': 'Material Request Item',
			'join_field': 'material_request_item',
			'target_field': 'ordered_qty',
			'target_parent_dt': 'Material Request',
			'target_parent_field': 'per_ordered',
			'target_ref_field': 'stock_qty',
			'source_field': 'stock_qty',
			'percent_join_field': 'material_request'
		}]

	def onload(self):
		supplier_tds = frappe.db.get_value("Supplier", self.supplier, "tax_withholding_category")
		self.set_onload("supplier_tds", supplier_tds)

	def validate(self):
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
		# if(self.naming_series=='JOB-.YY.-' and self.workflow_state=='Approved by HOD'):
		# 	doc=frappe.new_doc("Stock Entry")
		# 	doc.stock_entry_type="Material Transfer"
		# 	doc.from_warehouse=self.source_warehouse
		# 	doc.to_warehouse=self.target_warehouse
			
			
		# 	for i in self.get("items"):
		# 		doc.append("items",{
		# 			"item_code":i.item_code,
		# 			"qty":i.qty,
		# 			"basic_rate":i.rate,
		# 			"conversion_factor":i.conversion_factor,
		# 			"project":i.project,
		# 			"uom":i.uom,
		# 			"po_job_order":i.parent,
		# 			"po_job_order_item":i.name
		# 			})

		# 	doc.submit()
		# 	frappe.msgprint("done")
		# 	frappe.db.commit()
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
			# self.append("mr_reference",{
			# 	"mr_number":j,
			# 	"project":frappe.db.get_value("Material Request",j,"project"),
			# 	"request_purpose":frappe.db.get_value("Material Request",j,"request_purpose")
			# 	})

		for k in unique_item1:
			pr.append(k)

		str1 = ','.join(str(e) for e in mr)
		str2 = ','.join(str(f) for f in pr)

		self.material_series=str1
		self.project=str2
		
		super(PurchaseOrder, self).validate()

		self.set_status()

		# apply tax withholding only if checked and applicable
		self.set_tax_withholding()

		self.validate_supplier()
		self.validate_schedule_date()
		validate_for_items(self)
		self.check_on_hold_or_closed_status()

		self.validate_uom_is_integer("uom", "qty")
		self.validate_uom_is_integer("stock_uom", "stock_qty")

		self.validate_with_previous_doc()
		self.validate_for_subcontracting()
		self.validate_minimum_order_qty()
		self.validate_bom_for_subcontracting_items()
		self.create_raw_materials_supplied("supplied_items")
		self.set_received_qty_for_drop_ship_items()
		validate_inter_company_party(self.doctype, self.supplier, self.company, self.inter_company_order_reference)

	def validate_with_previous_doc(self):
		super(PurchaseOrder, self).validate_with_previous_doc({
			"Supplier Quotation": {
				"ref_dn_field": "supplier_quotation",
				"compare_fields": [["supplier", "="], ["currency", "="]],
			},
			"Supplier Quotation Item": {
				"ref_dn_field": "supplier_quotation_item",
				"compare_fields": [["project", "="], ["item_code", "="],
					["uom", "="], ["conversion_factor", "="]],
				"is_child_table": True
			},
			# "Material Request": {
			# 	"ref_dn_field": "material_request", 
			# 	"compare_fields": [["company", "="]],
			# },
			"Material Request Item": {
				"ref_dn_field": "material_request_item",
				"compare_fields": [["project", "="], ["item_code", "="]],
				"is_child_table": True
			}
		})


		if cint(frappe.db.get_single_value('Buying Settings', 'maintain_same_rate')):
			self.validate_rate_with_reference_doc([["Supplier Quotation", "supplier_quotation", "supplier_quotation_item"]])

	def set_tax_withholding(self):
		if not self.apply_tds:
			return

		tax_withholding_details = get_party_tax_withholding_details(self, self.tax_withholding_category)

		if not tax_withholding_details:
			return

		accounts = []
		for d in self.taxes:
			if d.account_head == tax_withholding_details.get("account_head"):
				d.update(tax_withholding_details)
			accounts.append(d.account_head)

		if not accounts or tax_withholding_details.get("account_head") not in accounts:
			self.append("taxes", tax_withholding_details)

		to_remove = [d for d in self.taxes
			if not d.tax_amount and d.account_head == tax_withholding_details.get("account_head")]

		for d in to_remove:
			self.remove(d)

		# calculate totals again after applying TDS
		self.calculate_taxes_and_totals()

	def validate_supplier(self):
		prevent_po = frappe.db.get_value("Supplier", self.supplier, 'prevent_pos')
		if prevent_po:
			standing = frappe.db.get_value("Supplier Scorecard", self.supplier, 'status')
			if standing:
				frappe.throw(_("Purchase Orders are not allowed for {0} due to a scorecard standing of {1}.")
					.format(self.supplier, standing))

		warn_po = frappe.db.get_value("Supplier", self.supplier, 'warn_pos')
		if warn_po:
			standing = frappe.db.get_value("Supplier Scorecard",self.supplier, 'status')
			frappe.msgprint(_("{0} currently has a {1} Supplier Scorecard standing, and Purchase Orders to this supplier should be issued with caution.").format(self.supplier, standing), title=_("Caution"), indicator='orange')

		self.party_account_currency = get_party_account_currency("Supplier", self.supplier, self.company)

	def validate_minimum_order_qty(self):
		if not self.get("items"): return
		items = list(set(d.item_code for d in self.get("items")))

		itemwise_min_order_qty = frappe._dict(frappe.db.sql("""select name, min_order_qty
			from tabItem where name in ({0})""".format(", ".join(["%s"] * len(items))), items))

		itemwise_qty = frappe._dict()
		for d in self.get("items"):
			itemwise_qty.setdefault(d.item_code, 0)
			itemwise_qty[d.item_code] += flt(d.stock_qty)

		for item_code, qty in itemwise_qty.items():
			if flt(qty) < flt(itemwise_min_order_qty.get(item_code)):
				frappe.throw(_("Item {0}: Ordered qty {1} cannot be less than minimum order qty {2} (defined in Item).").format(item_code,
					qty, itemwise_min_order_qty.get(item_code)))

	def validate_bom_for_subcontracting_items(self):
		if self.is_subcontracted == "Yes":
			for item in self.items:
				if not item.bom:
					frappe.throw(_("BOM is not specified for subcontracting item {0} at row {1}")
						.format(item.item_code, item.idx))

	def get_schedule_dates(self):
		for d in self.get('items'):
			if d.material_request_item and not d.schedule_date:
				d.schedule_date = frappe.db.get_value("Material Request Item",
						d.material_request_item, "schedule_date")


	@frappe.whitelist()
	def get_last_purchase_rate(self):
		"""get last purchase rates for all items"""

		conversion_rate = flt(self.get('conversion_rate')) or 1.0
		for d in self.get("items"):
			if d.item_code:
				last_purchase_details = get_last_purchase_details(d.item_code, self.name)
				if last_purchase_details:
					d.base_price_list_rate = (last_purchase_details['base_price_list_rate'] *
						(flt(d.conversion_factor) or 1.0))
					d.discount_percentage = last_purchase_details['discount_percentage']
					d.base_rate = last_purchase_details['base_rate'] * (flt(d.conversion_factor) or 1.0)
					d.price_list_rate = d.base_price_list_rate / conversion_rate
					d.rate = d.base_rate / conversion_rate
					d.last_purchase_rate = d.rate
				else:

					item_last_purchase_rate = frappe.get_cached_value("Item", d.item_code, "last_purchase_rate")
					if item_last_purchase_rate:
						d.base_price_list_rate = d.base_rate = d.price_list_rate \
							= d.rate = d.last_purchase_rate = item_last_purchase_rate

	# Check for Closed status
	def check_on_hold_or_closed_status(self):
		check_list =[]
		for d in self.get('items'):
			if d.meta.get_field('material_request') and d.material_request and d.material_request not in check_list:
				check_list.append(d.material_request)
				check_on_hold_or_closed_status('Material Request', d.material_request)

	def update_requested_qty(self):
		material_request_map = {}
		for d in self.get("items"):
			if d.material_request_item:
				material_request_map.setdefault(d.material_request, []).append(d.material_request_item)

		for mr, mr_item_rows in material_request_map.items():
			if mr and mr_item_rows:
				mr_obj = frappe.get_doc("Material Request", mr)

				if mr_obj.status in ["Stopped", "Cancelled"]:
					frappe.throw(_("Material Request {0} is cancelled or stopped").format(mr), frappe.InvalidStatusError)

#				mr_obj.update_requested_qty(mr_item_rows)

	def update_ordered_qty(self, po_item_rows=None):
		"""update requested qty (before ordered_qty is updated)"""
		item_wh_list = []
		for d in self.get("items"):
			if (not po_item_rows or d.name in po_item_rows) \
				and [d.item_code, d.warehouse] not in item_wh_list \
				and frappe.get_cached_value("Item", d.item_code, "is_stock_item") \
				and d.warehouse and not d.delivered_by_supplier:
					item_wh_list.append([d.item_code, d.warehouse])
		for item_code, warehouse in item_wh_list:
			update_bin_qty(item_code, warehouse, {
				"ordered_qty": get_ordered_qty(item_code, warehouse)
			})

	def check_modified_date(self):
		mod_db = frappe.db.sql("select modified from `tabPurchase Order` where name = %s",
			self.name)
		date_diff = frappe.db.sql("select '%s' - '%s' " % (mod_db[0][0], cstr(self.modified)))

		if date_diff and date_diff[0][0]:
			msgprint(_("{0} {1} has been modified. Please refresh.").format(self.doctype, self.name),
				raise_exception=True)

	def update_status(self, status):
		self.check_modified_date()
		self.set_status(update=True, status=status)
		self.update_requested_qty()
		self.update_ordered_qty()
		if self.is_subcontracted == "Yes":
			self.update_reserved_qty_for_subcontract()

		self.notify_update()
		clear_doctype_notifications(self)

	def on_submit(self):
		if(self.naming_series=='PO-.YY.-'):
			message="Dear sir ,<br> PO has been Approved Against the MR <br>PO NO: "+str(self.name)+"<br>MR NO: "+str(self.material_series)+""
			password = None
			email_args = {
				"recipients": ["design-1@wttindia.com","design-2@wttindia.com","design-3@wttindia.com"],
				"message": message,
				"subject": "PO has been approved"
				}
			if not frappe.flags.in_test:
				enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
			else:
				frappe.sendmail(**email_args)
			
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
		super(PurchaseOrder, self).on_submit()

		if self.is_against_so():
			self.update_status_updater()

		self.update_prevdoc_status()
		self.update_requested_qty()
		self.update_ordered_qty()
		self.validate_budget()

		if self.is_subcontracted == "Yes":
			self.update_reserved_qty_for_subcontract()

		frappe.get_doc('Authorization Control').validate_approving_authority(self.doctype,
			self.company, self.base_grand_total)

		self.update_blanket_order()

		update_linked_doc(self.doctype, self.name, self.inter_company_order_reference)
		if(self.approved_date1==None):
			date1=frappe.get_doc("Purchase Order",self.name)
			date1.approved_date1=str(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d'))
			date1.approved_time1=str(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'))
			date1.approver=frappe.session.user
			date1.submit()

	def on_cancel(self):
		# if(self.rejected_reason_md==""):
		# 	frappe.throw("Kindly Give Reason for Rejection")
		# doc=frappe.db.sql("UPDATE `tabOrder Status` SET `po_status`='"+str(self.workflow_state)+"' WHERE po_no='"+str(self.name)+"'")
		super(PurchaseOrder, self).on_cancel()

		if self.is_against_so():
			self.update_status_updater()

		if self.has_drop_ship_item():
			self.update_delivered_qty_in_sales_order()

		if self.is_subcontracted == "Yes":
			self.update_reserved_qty_for_subcontract()

		self.check_on_hold_or_closed_status()

		frappe.db.set(self,'status','Cancelled')

		self.update_prevdoc_status()

		# Must be called after updating ordered qty in Material Request
		# bin uses Material Request Items to recalculate & update
		self.update_requested_qty()
		self.update_ordered_qty()

		self.update_blanket_order()

		unlink_inter_company_doc(self.doctype, self.name, self.inter_company_order_reference)

	def on_update(self):
		ar=[]
		for i in frappe.db.sql("SELECT DISTINCT(project)as project FROM `tabPurchase Order Item` WHERE parent='"+str(self.name)+"' ",as_dict=1):
			ar.append(i.project)
		if(len(ar)>1):
			frappe.throw("PO should not be raid for multiple Project")

	def update_status_updater(self):
		self.status_updater.append({
			'source_dt': 'Purchase Order Item',
			'target_dt': 'Sales Order Item',
			'target_field': 'ordered_qty',
			'target_parent_dt': 'Sales Order',
			'target_parent_field': '',
			'join_field': 'sales_order_item',
			'target_ref_field': 'stock_qty',
			'source_field': 'stock_qty'
		})

	def update_delivered_qty_in_sales_order(self):
		"""Update delivered qty in Sales Order for drop ship"""
		sales_orders_to_update = []
		for item in self.items:
			if item.sales_order and item.delivered_by_supplier == 1:
				if item.sales_order not in sales_orders_to_update:
					sales_orders_to_update.append(item.sales_order)

		for so_name in sales_orders_to_update:
			so = frappe.get_doc("Sales Order", so_name)
			so.update_delivery_status()
			so.set_status(update=True)
			so.notify_update()

	def has_drop_ship_item(self):
		return any(d.delivered_by_supplier for d in self.items)

	def is_against_so(self):
		return any(d.sales_order for d in self.items if d.sales_order)

	def set_received_qty_for_drop_ship_items(self):
		for item in self.items:
			if item.delivered_by_supplier == 1:
				item.received_qty = item.qty

	def update_reserved_qty_for_subcontract(self):
		for d in self.supplied_items:
			if d.rm_item_code:
				stock_bin = get_bin(d.rm_item_code, d.reserve_warehouse)
				stock_bin.update_reserved_qty_for_sub_contracting()

	def update_receiving_percentage(self):
		total_qty, received_qty = 0.0, 0.0
		for item in self.items:
			received_qty += item.received_qty
			total_qty += item.qty
		if total_qty:
			self.db_set("per_received", flt(received_qty/total_qty) * 100, update_modified=False)
		else:
			self.db_set("per_received", 0, update_modified=False)

def item_last_purchase_rate(name, conversion_rate, item_code, conversion_factor= 1.0):
	"""get last purchase rate for an item"""

	conversion_rate = flt(conversion_rate) or 1.0

	last_purchase_details =  get_last_purchase_details(item_code, name)
	if last_purchase_details:
		last_purchase_rate = (last_purchase_details['base_net_rate'] * (flt(conversion_factor) or 1.0)) / conversion_rate
		return last_purchase_rate
	else:
		item_last_purchase_rate = frappe.get_cached_value("Item", item_code, "last_purchase_rate")
		if item_last_purchase_rate:
			return item_last_purchase_rate

@frappe.whitelist()
def close_or_unclose_purchase_orders(names, status):
	if not frappe.has_permission("Purchase Order", "write"):
		frappe.throw(_("Not permitted"), frappe.PermissionError)

	names = json.loads(names)
	for name in names:
		po = frappe.get_doc("Purchase Order", name)
		if po.docstatus == 1:
			if status == "Closed":
				if po.status not in ( "Cancelled", "Closed") and (po.per_received < 100 or po.per_billed < 100):
					po.update_status(status)
			else:
				if po.status == "Closed":
					po.update_status("Draft")
			po.update_blanket_order()

	frappe.local.message_log = []

def set_missing_values(source, target):
	target.ignore_pricing_rule = 1
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
def make_purchase_invoice(source_name, target_doc=None):
	return get_mapped_purchase_invoice(source_name, target_doc)

@frappe.whitelist()
def make_purchase_invoice_from_portal(purchase_order_name):
	doc = get_mapped_purchase_invoice(purchase_order_name, ignore_permissions=True)
	if doc.contact_email != frappe.session.user:
		frappe.throw(_('Not Permitted'), frappe.PermissionError)
	doc.save()
	frappe.db.commit()
	frappe.response['type'] = 'redirect'
	frappe.response.location = '/purchase-invoices/' + doc.name

def get_mapped_purchase_invoice(source_name, target_doc=None, ignore_permissions=False):
	def postprocess(source, target):
		target.flags.ignore_permissions = ignore_permissions
		set_missing_values(source, target)
		#Get the advance paid Journal Entries in Purchase Invoice Advance

		if target.get("allocate_advances_automatically"):
			target.set_advances()

	def update_item(obj, target, source_parent):
		target.amount = flt(obj.amount) - flt(obj.billed_amt)
		target.base_amount = target.amount * flt(source_parent.conversion_rate)
		target.qty = target.amount / flt(obj.rate) if (flt(obj.rate) and flt(obj.billed_amt)) else flt(obj.qty)

		item = get_item_defaults(target.item_code, source_parent.company)
		item_group = get_item_group_defaults(target.item_code, source_parent.company)
		target.cost_center = (obj.cost_center
			or frappe.db.get_value("Project", obj.project, "cost_center")
			or item.get("buying_cost_center")
			or item_group.get("buying_cost_center"))

	fields = {
		"Purchase Order": {
			"doctype": "Purchase Invoice",
			"field_map": {
				"party_account_currency": "party_account_currency",
				"supplier_warehouse":"supplier_warehouse"
			},
			"validation": {
				"docstatus": ["=", 1],
			}
		},
		"Purchase Order Item": {
			"doctype": "Purchase Invoice Item",
			"field_map": {
				"name": "po_detail",
				"parent": "purchase_order",
				"rejected_qty":"qty_rejected",
				"accepted_qty":"qty_accepted"
			},
			"postprocess": update_item,
			"condition": lambda doc: (doc.base_amount==0 or abs(doc.billed_amt) < abs(doc.amount))
		},
		"Purchase Taxes and Charges": {
			"doctype": "Purchase Taxes and Charges",
			"add_if_empty": True
		},
	}

	if frappe.get_single("Accounts Settings").automatically_fetch_payment_terms == 1:
		fields["Payment Schedule"] = {
			"doctype": "Payment Schedule",
			"add_if_empty": True
		}

	doc = get_mapped_doc("Purchase Order", source_name,	fields,
		target_doc, postprocess, ignore_permissions=ignore_permissions)

	return doc

@frappe.whitelist()
def make_rm_stock_entry(purchase_order, rm_items):
	rm_items_list = rm_items

	if isinstance(rm_items, str):
		rm_items_list = json.loads(rm_items)
	elif not rm_items:
		frappe.throw(_("No Items available for transfer"))

	if rm_items_list:
		fg_items = list(set(d["item_code"] for d in rm_items_list))
	else:
		frappe.throw(_("No Items selected for transfer"))

	if purchase_order:
		purchase_order = frappe.get_doc("Purchase Order", purchase_order)

	if fg_items:
		items = tuple(set(d["rm_item_code"] for d in rm_items_list))
		item_wh = get_item_details(items)

		stock_entry = frappe.new_doc("Stock Entry")
		stock_entry.purpose = "Send to Subcontractor"
		stock_entry.purchase_order = purchase_order.name
		stock_entry.supplier = purchase_order.supplier
		stock_entry.supplier_name = purchase_order.supplier_name
		stock_entry.supplier_address = purchase_order.supplier_address
		stock_entry.address_display = purchase_order.address_display
		stock_entry.company = purchase_order.company
		stock_entry.to_warehouse = purchase_order.supplier_warehouse
		stock_entry.set_stock_entry_type()

		for item_code in fg_items:
			for rm_item_data in rm_items_list:
				if rm_item_data["item_code"] == item_code:
					rm_item_code = rm_item_data["rm_item_code"]
					items_dict = {
						rm_item_code: {
							"po_detail": rm_item_data.get("name"),
							"item_name": rm_item_data["item_name"],
							"description": item_wh.get(rm_item_code, {}).get('description', ""),
							'qty': rm_item_data["qty"],
							'from_warehouse': rm_item_data["warehouse"],
							'stock_uom': rm_item_data["stock_uom"],
							'serial_no': rm_item_data.get('serial_no'),
							'batch_no': rm_item_data.get('batch_no'),
							'main_item_code': rm_item_data["item_code"],
							'allow_alternative_item': item_wh.get(rm_item_code, {}).get('allow_alternative_item')
						}
					}
					stock_entry.add_to_stock_entry_detail(items_dict)
		return stock_entry.as_dict()
	else:
		frappe.throw(_("No Items selected for transfer"))
	return purchase_order.name

def get_item_details(items):
	item_details = {}
	for d in frappe.db.sql("""select item_code, description, allow_alternative_item from `tabItem`
		where name in ({0})""".format(", ".join(["%s"] * len(items))), items, as_dict=1):
		item_details[d.item_code] = d

	return item_details

def get_list_context(context=None):
	from erpnext.controllers.website_list_for_contact import get_list_context
	list_context = get_list_context(context)
	list_context.update({
		'show_sidebar': True,
		'show_search': True,
		'no_breadcrumbs': True,
		'title': _('Purchase Orders'),
	})
	return list_context

@frappe.whitelist()
def update_status(status, name):
	po = frappe.get_doc("Purchase Order", name)
	po.update_status(status)
	po.update_delivered_qty_in_sales_order()

@frappe.whitelist()
def make_inter_company_sales_order(source_name, target_doc=None):
	from erpnext.accounts.doctype.sales_invoice.sales_invoice import make_inter_company_transaction
	return make_inter_company_transaction("Purchase Order", source_name, target_doc)

@frappe.whitelist()
def get_materials_from_supplier(purchase_order, po_details):
	if isinstance(po_details, str):
		po_details = json.loads(po_details)

	doc = frappe.get_cached_doc('Purchase Order', purchase_order)
	doc.initialized_fields()
	doc.purchase_orders = [doc.name]
	doc.get_available_materials()

	if not doc.available_materials:
		frappe.throw(_('Materials are already received against the purchase order {0}')
			.format(purchase_order))

	return make_return_stock_entry_for_subcontract(doc.available_materials, doc, po_details)

def make_return_stock_entry_for_subcontract(available_materials, po_doc, po_details):
	ste_doc = frappe.new_doc('Stock Entry')
	ste_doc.purpose = 'Material Transfer'
	ste_doc.purchase_order = po_doc.name
	ste_doc.company = po_doc.company
	ste_doc.is_return = 1

	for key, value in available_materials.items():
		if not value.qty:
			continue

		if value.batch_no:
			for batch_no, qty in value.batch_no.items():
				if qty > 0:
					add_items_in_ste(ste_doc, value, value.qty, po_details, batch_no)
		else:
			add_items_in_ste(ste_doc, value, value.qty, po_details)

	ste_doc.set_stock_entry_type()
	ste_doc.calculate_rate_and_amount()

	return ste_doc

def add_items_in_ste(ste_doc, row, qty, po_details, batch_no=None):
	item = ste_doc.append('items', row.item_details)

	po_detail = list(set(row.po_details).intersection(po_details))
	item.update({
		'qty': qty,
		'batch_no': batch_no,
		'basic_rate': row.item_details['rate'],
		'po_detail': po_detail[0] if po_detail else '',
		's_warehouse': row.item_details['t_warehouse'],
		't_warehouse': row.item_details['s_warehouse'],
		'item_code': row.item_details['rm_item_code'],
		'subcontracted_item': row.item_details['main_item_code'],
		'serial_no': '\n'.join(row.serial_no) if row.serial_no else ''
	})
@frappe.whitelist()
def make_request(source_name, target_doc=None):
	def postprocess(source, target):
		target.purpose="Job Order",
		target.set_warehouse=source.to_warehouse
	doc = get_mapped_doc("Job Order Request", source_name, {
		"Job Order Request": {
			"doctype": "Purchase Order",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map": {
				"Job Order":"purpose",
				"to_warehouse":"target_warehouse",
				1:"is_subcontracted",
				"to_warehouse":"default_target_warehouse",
				# "JOB-.YY.-":"naming_series",
				"project":"project"
			}
		},
		"Job Order Table": {
			"doctype": "Purchase Order Item",
			"field_map": {
				"fg_item": "item_code",
				"fg_description":"description",
				"fg_technical_description":"technical_description",
				"fg_item_qty":"qty",
				"job_order_request":"parent",
				"job_order_request_item":"name",
				"uom":"stock_uom"
			}
		},
		"Raw Materials Job Order Request": {
			"doctype": "Raw Materials Purchase Order",
			"field_map": {
				"parent":"job_order_request",
				"uom":"uom",
				"name":"job_order_request_item"
			}
		}
	}, target_doc,postprocess)
	return doc

			
@frappe.whitelist()
def mr_func(arr):
	data=[]
	to_python = json.loads(arr)
	# arr3=['PENPVC-U PN10DN15-1/2INPE', 'PENPVC-U PN10DN20-3/4INPE', 'PENPVC-U PN10DN25-1INPE', 'PENPVC-U PN10DN50-2INPE', 'PENPVC-U PN10DN100-4INPE', 'ELENPVC-U PN10DN20-3/4IN90DEGSRMOSE', 'ELENPVC-U PN10DN25-1IN90DEGSRMOSE', 'ELENPVC-U PN10DN50-2IN90DEGSRMOSE', 'ELENPVC-U PN10DN80-3IN90DEGSRMOSE', 'ELENPVC-U PN10DN100-4IN90DEGSRMOSE', 'RDENPVC-U PN10DN40-DN25BTMOSE', 'RDENPVC-U PN10DN100-DN50BTMOSE', 'RDENPVC-U PN10DN100-DN50CRMOSE', 'MTAENPVC-U PN10DN15-1/2INBSPMO', 'MTAENPVC-U PN10DN20-3/4INBSPMO', 'MTAENPVC-U PN10DN50-2INBSPMO', 'MTAENPVC-U PN10DN80-3INBSPMO', 'UNENPVC-U PN10DN20-3/4INMOFS', 'CSENPVC-U PN10DN50-DN15MOFTE', 'FLENPVC-U PN10DN25-1INBR1585MM414MM', 'FLENPVC-U PN10DN50-2INBR19125MM417.5MM', 'FLENPVC-U PN10DN100-4INBR22180MM817MM', 'SEENPVC-U PN10DN25-1INSNFAMO', 'SEENPVC-U PN10DN50-2INSNFAMO', 'SEENPVC-U PN10DN100-4INSNFAMO', 'TEEENPVC-U PN10DN25-1INET90DEGMOSE', 'TEEENPVC-U PN10DN50-2INET90DEGMOSE', 'PENCPVCPN10DN15-1/2INPE', 'ELENCPVCPN10DN15-1/2IN90DEGSRMOSE', 'FLENCPVCPN10DN40-1 1/2INBR16110MM417.5MM', 'SEENCPVCPN10DN40-1 1/2INSNFAMO', 'UNENCPVCPN10DN15-1/2INMOFS', 'SPTPPN1645-5041D500ML', 'SPTPPN1645-5041D1000ML', 'PENPVC-U PN10DN40-1 1/2INPE', 'PENPVC-U PN10DN65-2 1/2INPE', 'ELENPVC-U PN10DN40-1 1/2IN90DEGSRMOSE', 'ELENPVC-U PN10DN65-2 1/2IN90DEGSRMOSE', 'FLENPVC-U PN10DN65-2 1/2INBR20145MM418MM', 'SEENPVC-U PN10DN65-2 1/2INSNFAMO', 'RDENPVC-U PN10DN40-DN32BTMOSE', 'RDENPVC-U PN10 DN50-DN40BTMOSE', 'MTAENPVC-U PN10DN32-1 1/4INBSPMO', 'MTAENPVC-U PN10DN40-1 1/2INBSPMO', 'PENPVC-U PN10DN32-1 1/4INPE', 'SEENPVC-U PN10DN32-1 1/4INSNFAMO', 'SEENPVC-U PN10DN40-1 1/2INSNFAMO', 'ELENPVC-U PN10DN15-1/2IN90DEGSRMOSE', 'ELENPVC-U PN10DN32-1 1/4IN90DEGSRMOSE', 'RDENPVC-U PN10DN40-DN20BTMOSE', 'RDENPVC-U PN10DN65-DN40BTMOSE', 'FTAENPVC-U PN10DN10-3/8INBSPMO', 'TEEENPVC-U PN10DN15-1/2INET90DEGMOSE', 'TEEENPVC-U PN10DN20-3/4INET90DEGMOSE', 'TEEENPVC-U PN10DN40-1 1/2INET90DEGMOSE', 'TEEENPVC-U PN10DN65-2 1/2INET90DEGMOSE', 'RDENPVC-U PN10DN50-DN32BTMOSE', 'RDENPVC-U PN10 DN32-DN20BTMOSE', 'COENPVC-U PN10DN40-1 1/2INSVST', 'COENPVC-U PN10DN100-4INSVST', 'FLENPVC-U PN10DN40-1 1/2INBR16110MM417.5MM', 'RDENPVC-U PN10DN65-DN50CRMOSE', 'RDENPVC-U PN10DN32-DN15BTMOSE', 'UNENPVC-U PN10DN20-3/4INMOSE', 'UNENPVC-U PN10DN25-1INMOSE', 'FLENPVC-U PN10DN50-2INBRSTD125MM417.5MM', 'FLENPVC-U PN10DN40-1 1/2INBRSTD110MM417.5MM', 'FLENPVC-U PN10DN32-1 1/4INBRSTD100MM417MM', 'FLENPVC-U PN10DN65-2 1/2INBRSTD145MM418MM', 'FLANSIPVC-U PN16DN80-3INBRSTD168.3MM822.225MM', 'FLANSIPVC-U PN16DN50-2INBRSTD127MM819.05MM', 'FLANSIPVC-U PN16DN40-1 1/2INBRSTD114.3MM422.225MM', 'FLENPVC-U PN10DN25-1INBRSTD85MM414MM']
	# arr4=[]
	for i in to_python:
	# 	if(i["item"] in arr3):
	# 		arr4.append({"idx":i["idx"],"ic":i["item"],"mr":i["parent"]})
	# frappe.msgprint(str(arr4))
		if(i['parent']!=None and i['child']!=None):		
			doc=frappe.db.sql("SELECT idx,parent,creation,qty FROM `tabMaterial Request Item` WHERE item_code='"+str(i["item"])+"' and parent='"+str(i["parent"])+"' and name='"+str(i["child"])+"' ",as_dict=1)
			if doc:
				for j in doc:
					data.append({
						"idx":i["idx"],
						"description":i["description"],
						"technical_description":i["technical_description"],
						"po_qty":i["qty"],
						"qty":j.qty,
						"rate":j.idx,
						"parent":j.parent,
						"status":frappe.db.get_value("Material Request",j.parent,"workflow_state")
						})
			else:
				data.append({
					"idx":i["idx"],
					"description":i["description"],
					"technical_description":i["technical_description"],
					"po_qty":j["qty"],
					"qty":"-",
					"rate":"-",
					"parent":"Not Linked",
					"status":"-"
					})
		else:
			doc=frappe.db.sql("SELECT idx,parent,creation,qty FROM `tabMaterial Request Item` WHERE item_code='"+str(i["item"])+"' ",as_dict=1)
			if doc:
				for j in doc:
					data.append({
						"idx":i["idx"],
						"description":i["description"],
						"technical_description":i["technical_description"],
						"po_qty":i["qty"],
						"qty":j.qty,
						"rate":j.idx,
						"parent":j.parent,
						"status":frappe.db.get_value("Material Request",j.parent,"workflow_state")
						})
			else:
				data.append({
					"idx":i["idx"],
					"description":i["description"],
					"technical_description":i["technical_description"],
					"po_qty":j["qty"],
					"qty":"-",
					"rate":"-",
					"parent":"Not Linked",
					"status":"-"
					})
	return data
@frappe.whitelist()
def download_mr_func(arr):
	data=[]
	to_python = json.loads(arr)
	
	for i in to_python:
		
		doc=frappe.db.sql("SELECT idx,parent,creation,qty FROM `tabMaterial Request Item` WHERE item_code='"+str(i["item"])+"' and parent='"+str(i["parent"])+"' and name='"+str(i["child"])+"' ",as_dict=1)
		if doc:
			for j in doc:
				data.append({
					"idx":i["idx"],
					"description":i["description"],
					"technical_description":i["technical_description"],
					"po_qty":i["qty"],
					"qty":j.qty,
					"rate":j.idx,
					"parent":j.parent,
					"status":frappe.db.get_value("Material Request",j.parent,"workflow_state")
					})
		else:
			data.append({
				"idx":i["idx"],
				"description":i["description"],
				"technical_description":i["technical_description"],
				"po_qty":j["qty"],
				"qty":"-",
				"rate":"-",
				"parent":"Not Linked",
				"status":"-"
				})
	ur=[]
	xl=[["DESCRIPTION","TECHNICAL DECRIPTION","PO QUANTITY","MR QUANTITY","RATE","MATERIAL REQUEST","STATUS"]]
	for i in data:
		xl.append([i["description"],i["technical_description"],i["po_qty"],i["qty"],i["rate"],i["parent"],i["status"]])
	
	xlsx_file = make_xlsx(xl, "MRPOLink")
	file_data = xlsx_file.getvalue()

	_file = frappe.get_doc({
	"doctype": "File",
	"file_name": "MRPOLink.xlsx",
	"folder": "Home/Attachments",
	"content": file_data})
	_file.save()
	ur.append({"url":_file.file_url})
	return ur


@frappe.whitelist()
def pr_func(arr):
	data=[]
	to_python = json.loads(arr)

	itc_arr=[]
	for i in to_python:
		itc_arr.append(i["item"])
		if(i['mr2']!=None):		
			doc=frappe.db.sql("SELECT idx,parent,creation,qty,material_request,material_request_item FROM `tabPurchase Receipt Item` WHERE item_code='"+str(i["item"])+"' and purchase_order='"+str(i["parent"])+"' and purchase_order_item='"+str(i["child"])+"' ",as_dict=1)
			if doc:
				for j in doc:
					# if(frappe.db.get_value("Purchase Receipt",j.parent,"status")!='Cancelled' and frappe.db.get_value("Purchase Receipt",j.parent,"status")!='Rejected'):
					data.append({
						"idx":i["idx"],
						"description":i["description"],
						"technical_description":i["technical_description"],
						"po_qty":i["qty"],
						"qty":j.qty,
						"rate":j.idx,
						"mr":j.material_request,
						"mr_row":frappe.db.get_value("Material Request Item",j.material_request_item,"idx"),
						"mr_qty":frappe.db.get_value("Material Request Item",j.material_request_item,"qty"),
						"parent":j.parent,
						"date":str(getdate(j.creation).strftime("%d-%m-%Y")),
						"status":frappe.db.get_value("Purchase Receipt",j.parent,"status"),
						"mr2":i["mr2"]
						})
			else:
				data.append({
					"idx":i["idx"],
					"description":i["description"],
					"technical_description":i["technical_description"],
					"po_qty":i["qty"],
					"qty":"-",
					"rate":"-",
					"mr_row":"-",
					"nr_qty":"-",
					"mr":"-",
					"parent":"Not Linked",
					"date":"",
					"status":"-",
					"mr2":i["mr2"]
					})
		else:
			data.append({
					"idx":i["idx"],
					"description":i["description"],
					"technical_description":i["technical_description"],
					"po_qty":i["qty"],
					"qty":"-",
					"rate":"-",
					"mr_row":"-",
					"nr_qty":"-",
					"mr":"-",
					"parent":"Not Linked",
					"date":"",
					"status":"-",
					"mr2":'-'
					})
	# frappe.msgprint(str(itc_arr))
	# console.log(str(itc_arr))
	return data


@frappe.whitelist()
def download_pr_func(arr):
	data=[]
	to_python = json.loads(arr)
	
	for i in to_python:
		
		doc=frappe.db.sql("SELECT idx,parent,creation,qty,material_request,material_request_item FROM `tabPurchase Receipt Item` WHERE item_code='"+str(i["item"])+"' and purchase_order='"+str(i["parent"])+"' and purchase_order_item='"+str(i["child"])+"' ",as_dict=1)
		if doc:
			for j in doc:
				if(frappe.db.get_value("Purchase Receipt",j.parent,"status")!='Cancelled' and frappe.db.get_value("Purchase Receipt",j.parent,"status")!='Rejected'):
					data.append({
						"idx":i["idx"],
						"description":i["description"],
						"technical_description":i["technical_description"],
						"po_qty":i["qty"],
						"qty":j.qty,
						"rate":j.idx,
						"mr":j.material_request,
						"mr_row":frappe.db.get_value("Material Request Item",j.material_request_item,"idx"),
						"mr_qty":frappe.db.get_value("Material Request Item",j.material_request_item,"qty"),
						"parent":j.parent,
						"status":frappe.db.get_value("Purchase Receipt",j.parent,"status"),
						"mr2":i["mr2"]
						})
		else:
			data.append({
				"idx":i["idx"],
				"description":i["description"],
				"technical_description":i["technical_description"],
				"po_qty":i["qty"],
				"qty":"-",
				"rate":"-",
				"mr_row":"-",
				"mr_qty":"-",
				"mr":"-",
				"parent":"Not Linked",
				"status":"-",
				"mr2":i["mr2"]
				})
	
	ur=[]
	xl=[["PO ROW","DESCRIPTION","TECHNICAL DECRIPTION","PO QUANTITY","PR QUANTITY","RATE","MR LINKED TO PR","MR ROW","MR QTY","PURCHASE RECEIPT","STATUS","MR"]]
	for i in data:
		xl.append([i["idx"],i["description"],i["technical_description"],i["po_qty"],i["qty"],i["rate"],i["mr"],i["mr_row"],i["mr_qty"],i["parent"],i["status"],i["mr2"]])
	
	xlsx_file = make_xlsx(xl, "POPRLink")
	file_data = xlsx_file.getvalue()

	_file = frappe.get_doc({
	"doctype": "File",
	"file_name": "POPRLink.xlsx",
	"folder": "Home/Attachments",
	"content": file_data})
	_file.save()
	ur.append({"url":_file.file_url})
	return ur























			# for i in self.get("items"):
			# 	doc.append("items",{
			# 		"s_warehouse1":self.source_warehouse,
			# 		"t_warehouse1":self.target_warehouse,
			# 		"item_code":i.item_code,
			# 		"qty":i.qty,
			# 		"item_name":i.item_name,
			# 		"description":i.description,
			# 		"technical_description":i.technical_description,
			# 		"conversion_factor":i.conversion_factor,
			# 		"stock_uom":i.stock_uom,
			# 		"transfer_qty":i.qty,
			# 		"basic_rate":i.rate,
			# 		"amount":i.amount,
			# 		"project":i.project,
			# 		"uom":i.uom
			# 		})

			# doc.total_qty=self.total_qty
			# doc.total=self.total
			# doc.tax=self.taxes_and_charges

			# for i in self.get("taxes"):
			# 	doc.append("tax_table",{
			# 		"category":i.category,
			# 		"add_deduct_tax":i.add_deduct_tax,
			# 		"charge_type":i.charge_type,
			# 		"account_head":i.account_head,
			# 		"description":i.description,
			# 		"rate":i.rate,
			# 		"tax_amount":i.tax_amount,
			# 		"total":i.total
			# 		})
			
			# doc.base_taxes_and_charges_added=self.base_taxes_and_charges_added
			# doc.base_taxes_and_charges_deducted=self.base_taxes_and_charges_deducted
			# doc.base_total_taxes_and_charges=self.base_total_taxes_and_charges
			# doc.taxes_and_charges_added=self.taxes_and_charges_added
			# doc.taxes_and_charges_deducted=self.taxes_and_charges_deducted
			# doc.total_taxes_and_charges=self.total_taxes_and_charges
			# doc.base_grand_total=self.base_grand_total
			# doc.base_rounding_adjustment=self.base_rounding_adjustment
			# doc.base_in_words=self.base_in_words
			# doc.base_rounded_total=self.base_rounded_total
			# doc.grand_total=self.grand_total
			# doc.rounding_adjustment=self.rounding_adjustment
			# doc.rounded_total=self.rounded_total
			# doc.disable_rounded_total=self.disable_rounded_total
			# doc.in_words=self.in_words


@frappe.whitelist()
def make_supplier_quote(source_name, target_doc=None):
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
			"postprocess": update_item
		},
		"SQ Combined Table":{
			"doctype":"PO Combined Table",
			"field_map": [
				["price_list_rate2","price_list_rate"],
				["discount_percentage2","discount_percentage"],
				["discount_amount2","discount_amount"],
				["rate2","rate"],
				["amount2","amount"],
				["name", "sq_combined_item"],
				["parent", "supplier_quotation"],
				["material_request", "material_request"],
				["material_request_item", "material_request_item"],
				["sales_order", "sales_order"]
			],
		},
		"Purchase Taxes and Charges": {
			"doctype": "Purchase Taxes and Charges",
		},
	}, target_doc, set_missing_values)

	return doclist

@frappe.whitelist()
def make_service_request(source_name, target_doc=None):
	doclist = get_mapped_doc("Service Request", source_name,{
		"Service Request": {
			"doctype": "Purchase Order",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Service Request Item": {
			"doctype": "Purchase Order Item",
			"field_map": [
 				["parent", "service_request"],
 				["name", "service_request_item"]
			]
		}
	},target_doc)
	return doclist


@frappe.whitelist()
def make_nesting(source_name, target_doc=None):
	doclist = get_mapped_doc("Nesting and Machining", source_name,{
		"Nesting and Machining": {
			"doctype": "Purchase Order",
			"validation": {
				"docstatus": ["=", 0]
			},
		},
		"Inward Job Order": {
			"doctype": "Purchase Order Item",
			"field_map": [
 				["parent", "nesting_and_machining"],
 				["name", "nesting_and_machining_name"],
 				["uom", "stock_uom"]
			]
		},
		"Outward Job Order": {
			"doctype": "Raw Materials Purchase Order",
		}
	},target_doc)
	return doclist



@frappe.whitelist()
def combine_items(arr):
	to_python = json.loads(arr)
	item=[]
	lst = []
	v=[]
	for i in to_python:
		if i["item_code"] not in lst:
			lst.append(i["item_code"])
			item.append(i)
		else:
			if(item[lst.index(i["item_code"])]["uom"] == i["uom"] and item[lst.index(i["item_code"])]["rate"] == i["rate"]):
				item[lst.index(i["item_code"])]["qty"] += i["qty"]
				item[lst.index(i["item_code"])]["stock_qty"] += i["stock_qty"]
			else:
				item.append({
					"item_code":i['item_code'],
					"item_name":i['item_name'],
					"description":i['description'],
					"technical_description":i['technical_description'],
					"supplier_description":i['supplier_description'],
					"qty":i['qty'],
					"stock_qty":i['stock_qty'],
					"rate":i['rate'],
					"amount":i['qty']*i['rate'],
					"uom":i['uom']
					})
	v=[]
	for q in item:
		v.append({
			"item_code":q['item_code'],
			"item_name":q['item_name'],
			"description":q['description'],
			"technical_description":q['technical_description'],
			"supplier_description":q['supplier_description'],
			"qty":q['qty'],
			"stock_qty":q['stock_qty'],
			"rate":q['rate'],
			"amount":q['qty']*q['rate'],
			"uom":q['uom']
			})
	return v


@frappe.whitelist()
def check_the_items_were_receipted(ar):
	to_python=json.loads(ar)
	for i in to_python:
		if frappe.db.sql("SELECT pr.name from `tabPurchase Receipt`as pr,`tabPurchase Receipt Item`as pri WHERE pri.parent=pr.name and pri.purchase_receipt_item='"+str(i)+"' and pr.docstatus=1 ",as_dict=1):
			frappe.throw("Item has Received")


@frappe.whitelist()
def approve_after_emergency_approval(nn):
	v=frappe.db.sql("UPDATE `tabPurchase Order` SET docstatus=1,workflow_state='Approved' WHERE name='"+str(nn)+"' ")
	return v



@frappe.whitelist()
def clientscript(lr):
	ar=[]
	doc=frappe.get_doc("Purchase Order",str(lr))
	if(doc.approved_date==None):
		dd=doc.modified
		d=dd.date()
	else:
		d=doc.approved_date
	
	diff=(date.today()-d).days
	if(diff>0):
		ar.append({"days":doc.workflow_state+" by "+str(diff)+" Days"})
	else:
		ar.append({"days":doc.workflow_state+" by Today"})
	# +frappe.get_value("User",doc.modified_by,"full_name")+" "
	for i in doc.items:
		ar.append(i)

	return ar

@frappe.whitelist()
def ot_details(lr):
	ar=[]
	doc=frappe.get_doc("OT Prior Information",str(lr))
	for i in doc.ot_table:
		ar.append(i)
	return ar

@frappe.whitelist()
def get_last_rate(arr):
	data=[]
	to_python = json.loads(arr)
	for i in to_python:
		if(i["model_no"]==""):
			doc=frappe.db.sql("SELECT model_no as 'Model No', (SELECT CONCAT(round(base_rate,2),' - ',parent) FROM `tabPurchase Order Item` WHERE item_code='"+str(i["item"])+"' and name!='"+str(i["nn"])+"' GROUP BY parent ORDER BY creation DESC LIMIT 1) as 'Rate1', (SELECT CONCAT(round(base_rate,2),' - ',parent) FROM `tabPurchase Order Item` WHERE item_code='"+str(i["item"])+"' and name!='"+str(i["nn"])+"' GROUP BY parent ORDER BY creation DESC LIMIT 1,1) as 'Rate2', (SELECT CONCAT(round(base_rate,2),' - ',parent) FROM `tabPurchase Order Item` WHERE item_code='"+str(i["item"])+"' and name!='"+str(i["nn"])+"' GROUP BY parent ORDER BY creation DESC LIMIT 2,1) as 'Rate3' FROM `tabPurchase Order Item` WHERE item_code='"+str(i["item"])+"' and name!='"+str(i["nn"])+"' GROUP BY parent ORDER BY creation DESC LIMIT 1",as_dict=1)
			if doc:
				for j in doc:
					data.append({
						"model_no":i["model_no"],
						"item_code":i["item"],
						"description":i["description"],
						"technical_description":i["technical_description"],
						"qty":i["qty"],
						"rate1":j.Rate1,
						"rate2":j.Rate2,
						"rate3":j.Rate3
						})
			else:
				data.append({
					"model_no":"-",
					"item_code":i["item"],
					"description":i["description"],
					"technical_description":i["technical_description"],
					"qty":i["qty"],
					"rate1":"-",
					"rate2":"-",
					"rate3":"-"
					})
		else:
			doc=frappe.db.sql("SELECT model_no as 'Model No', (SELECT CONCAT(round(base_rate,2),' - ',parent) FROM `tabPurchase Order Item` WHERE model_no='"+str(i["model_no"])+"' and name!='"+str(i["nn"])+"' GROUP BY parent ORDER BY creation DESC LIMIT 1) as 'Rate1', (SELECT CONCAT(round(base_rate,2),' - ',parent) FROM `tabPurchase Order Item` WHERE model_no='"+str(i["model_no"])+"' and name!='"+str(i["nn"])+"' GROUP BY parent ORDER BY creation DESC LIMIT 1,1) as 'Rate2', (SELECT CONCAT(round(base_rate,2),' - ',parent) FROM `tabPurchase Order Item` WHERE model_no='"+str(i["model_no"])+"' and name!='"+str(i["nn"])+"' GROUP BY parent ORDER BY creation DESC LIMIT 2,1) as 'Rate3' FROM `tabPurchase Order Item` WHERE model_no='"+str(i["model_no"])+"' and name!='"+str(i["nn"])+"' GROUP BY parent ORDER BY creation DESC LIMIT 1",as_dict=1)
			if doc:
				for j in doc:
					data.append({
						"model_no":i["model_no"],
						"item_code":i["item"],
						"description":i["description"],
						"technical_description":i["technical_description"],
						"qty":i["qty"],
						"rate1":j.Rate1,
						"rate2":j.Rate2,
						"rate3":j.Rate3
						})
			else:
				data.append({
						"model_no":i["model_no"],
						"item_code":i["item"],
						"description":i["description"],
						"technical_description":i["technical_description"],
						"qty":i["qty"],
						"rate1":"-",
						"rate2":"-",
						"rate3":"-"
					})
	return data
@frappe.whitelist()
def create_stock_entry(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		qty = (
			flt(obj.qty) - flt(obj.transfered_qty)
			if flt(obj.qty) > flt(obj.transfered_qty)
			else 0
		)
		target.qty = qty
	def update_item_parent(obj, target, source_parent):
		target.stock_entry_type = "Send to Subcontractor"

	doclist = get_mapped_doc(
		"Purchase Order",
		source_name,
		{
			"Purchase Order": {
				"doctype": "Stock Entry",
				"validation": {
					"docstatus": ["=", 1],
					"purpose": ["in", ["Job Order"]],
					"supplier":"supplier",
					"set_target_warehouse":"from_warehouse",
					"supplier_warehouse":"to_warehouse"
				},
				"postprocess": update_item_parent,
			},
			"Raw Materials Purchase Order": {
				"doctype": "Stock Entry Detail",
				"field_map": {
					"name": "po_job_order_item",
					"parent": "po_job_order",
					"uom": "uom",
					"job_card_item": "job_card_item",
					"finished_good":"subcontracted_item"
				},
				"postprocess": update_item,
				"condition": lambda doc: doc.transfered_qty < doc.qty,
			},
		},
		target_doc,
		# set_missing_values,
	)

	return doclist
@frappe.whitelist()
def receive_fg_items(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		qty = (
			flt(obj.qty) - flt(obj.fg_item_received_qty)
			if flt(obj.qty) > flt(obj.fg_item_received_qty)
			else 0
		)
		target.qty = qty
	def update_item_parent(obj, target, source_parent):
		target.stock_entry_type = "Send to Subcontractor"

	doclist = get_mapped_doc(
		"Purchase Order",
		source_name,
		{
			"Purchase Order": {
				"doctype": "Stock Entry",
				"validation": {
					"docstatus": ["=", 1],
					"purpose": ["in", ["Job Order"]],
					"set_target_warehouse":"from_warehouse",
					"supplier_warehouse":"to_warehouse"
				},
				"postprocess": update_item_parent,
			},
			"Purchase Order Item": {
				"doctype": "Stock Entry Detail",
				"field_map": {
					"fg_item":"item_code",
					"fg_description":"description",
					"fg_technical_description":"technical_description",
					"fg_item_qty":"qty",
					"name": "po_job_order_item",
					"parent": "po_job_order",
					1:"is_finished_item",
					"uom": "uom",
				},
				"postprocess": update_item,
				"condition": lambda doc: doc.fg_item_received_qty < doc.qty,
			},
		},
		target_doc,
		# set_missing_values,
	)

	return doclist

# def make_stock_entry(source_name, target_doc=None):
# 	def update_item(obj, target, source_parent):
# 		qty = (
# 			flt(flt(obj.stock_qty) - flt(obj.ordered_qty)) / target.conversion_factor
# 			if flt(obj.stock_qty) > flt(obj.ordered_qty)
# 			else 0
# 		)
# 		target.qty = qty
# 		target.transfer_qty = qty * obj.conversion_factor
# 		target.conversion_factor = obj.conversion_factor

# 		if (
# 			source_parent.material_request_type == "Material Transfer"
# 			or source_parent.material_request_type == "Customer Provided"
# 		):
# 			target.t_warehouse = obj.warehouse
# 		else:
# 			target.s_warehouse = obj.warehouse

# 		if source_parent.material_request_type == "Customer Provided":
# 			target.allow_zero_valuation_rate = 1

# 		if source_parent.material_request_type == "Material Transfer":
# 			target.s_warehouse = obj.from_warehouse

# 	def set_missing_values(source, target):
# 		target.purpose = source.material_request_type
# 		target.from_warehouse = source.set_from_warehouse
# 		target.to_warehouse = source.set_warehouse

# 		if source.job_card:
# 			target.purpose = "Material Transfer for Manufacture"

# 		if source.material_request_type == "Customer Provided":
# 			target.purpose = "Material Receipt"

# 		target.set_transfer_qty()
# 		target.set_actual_qty()
# 		target.calculate_rate_and_amount(raise_error_if_no_rate=False)
# 		target.stock_entry_type = target.purpose
# 		target.set_job_card_data()

# 	doclist = get_mapped_doc(
# 		"Material Request",
# 		source_name,
# 		{
# 			"Material Request": {
# 				"doctype": "Stock Entry",
# 				"validation": {
# 					"docstatus": ["=", 1],
# 					"material_request_type": ["in", ["Material Transfer", "Material Issue", "Customer Provided"]],
# 				},
# 			},
# 			"Material Request Item": {
# 				"doctype": "Stock Entry Detail",
# 				"field_map": {
# 					"name": "material_request_item",
# 					"parent": "material_request",
# 					"uom": "stock_uom",
# 					"job_card_item": "job_card_item",
# 				},
# 				"postprocess": update_item,
# 				"condition": lambda doc: doc.ordered_qty < doc.stock_qty,
# 			},
# 		},
# 		target_doc,
# 		set_missing_values,
# 	)

# 	return doclist


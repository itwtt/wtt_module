
from __future__ import unicode_literals
import frappe

from frappe.utils import flt, cint, nowdate
import calendar
from frappe import throw, _
import frappe.defaults
from frappe.utils import getdate
from erpnext.controllers.buying_controller import BuyingController
from erpnext.accounts.utils import get_account_currency
from frappe.desk.notifications import clear_doctype_notifications
from frappe.model.mapper import get_mapped_doc
from erpnext.buying.utils import check_on_hold_or_closed_status
from erpnext.assets.doctype.asset.asset import get_asset_account, is_cwip_accounting_enabled
from erpnext.assets.doctype.asset_category.asset_category import get_asset_category_account
from six import iteritems
from datetime import date,datetime,timedelta
import frappe
from frappe import _, throw
from frappe.desk.notifications import clear_doctype_notifications
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, flt, getdate, nowdate
from six import iteritems
from pytz import timezone 
import erpnext
from erpnext.accounts.utils import get_account_currency
from erpnext.assets.doctype.asset.asset import get_asset_account, is_cwip_accounting_enabled
from erpnext.assets.doctype.asset_category.asset_category import get_asset_category_account
from erpnext.buying.utils import check_on_hold_or_closed_status
from erpnext.controllers.buying_controller import BuyingController
from erpnext.stock.doctype.delivery_note.delivery_note import make_inter_company_transaction

from erpnext.stock.doctype.purchase_receipt.purchase_receipt import PurchaseReceipt

form_grid_templates = {
	"items": "templates/form_grid/item_grid.html"
}

class customPR(PurchaseReceipt):
	def validate(self):
		super().validate()
		if(self.shipment_arrived_within_an_acceptable_timeframe or self.shipment_not_arrived_within_an_acceptable_timeframe):
			pass
		else:
			frappe.throw("Vendor rating is Mandatory (Acceptable timeframe)")

		if(self.items_were_securely_and_appropriately_packaged or self.items_were_not_securely_and_appropriately_packaged):
			pass
		else:
			frappe.throw("Vendor rating is Mandatory (Securely and Appropriate Package)")

		if(self.materials_meet_specified_quality_standards or self.damage_materials or self.send_wrong_materials):
			pass
		else:
			frappe.throw("Vendor rating is Mandatory (Material Standards or Damage or Wrong Material)")

		if(self.communicated_effectively_throughout_the_shipping_process or self.poor_communication):
			pass
		else:
			frappe.throw("Vendor rating is Mandatory (Communication)")

		if(self.invoices_packing_lists_and_other_documentation_are_accurate or self.missing_documentation):
			pass
		else:
			frappe.throw("Vendor rating is Mandatory (Documentation)")

		if(self.overall_rating):
			pass
		else:
			frappe.throw("Vendor rating is Mandatory (Overall Rating)")

		ar=[]
		if(self.naming_series=='PR-.YY.-'):
			for i in frappe.db.sql("SELECT GROUP_CONCAT(DISTINCT(purchase_order))as po FROM `tabPurchase Receipt Item` WHERE parent='"+str(self.name)+"' ",as_dict=1):
				ar.append(i.po)
			self.purchase_series=ar[0]
		if(self.status=='Draft' and self.create_task==1):
			if(frappe.db.exists("Task Allocation", {"mr_inward": self.name})):
				pass
			else:

				df=datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
				dt=(datetime.now(timezone("Asia/Kolkata"))+timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
				datetime_format1 = datetime.strptime(df,"%Y-%m-%d %H:%M:%S")
				datetime_format2 = datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")
				end_time = datetime_format1.replace(hour=18,minute=00,second=00)
				if(self.employee_name=="WTT1348"):
					end_time = datetime_format1.replace(hour=19,minute=00,second=00)

				if(datetime_format2>end_time):
					dif = end_time - datetime_format1
					hr = dif.total_seconds() / 3600
					second_half = 8-hr
					next_day = datetime_format1+timedelta(days=1)
					weekday = calendar.day_name[next_day.weekday()]
					if(weekday=="Sunday"):
						next_day = datetime_format1+timedelta(days=2)
					datetime_format2 = (next_day.replace(hour=9,minute=00,second=00))+timedelta(hours=second_half)

				difference = datetime_format2-datetime_format1
				hrs = difference.total_seconds() / 3600
				# frappe.msgprint(str(df)+"and"+str(dt)+"and"+str(hrs))
				doc=frappe.new_doc("Task Allocation")
				doc.user=frappe.session.user
				doc.employee=self.to_be_inspected_by
				doc.mr_inward=self.name
				doc.append("works_table",{
					"type_of_work":str(self.name),
					"description":"Items to be Inspected",
					"from_time":datetime_format1,
					"to_time":datetime_format2,
					"hours":8
					})
				doc.save()
				frappe.db.commit()
				frappe.msgprint("Task Allocated for "+str(self.employee_name)+" Succesfully")
		
	def on_cancel(self):
		super().on_cancel()
		frappe.db.sql("UPDATE `tabItem Inspection` set workflow_state='Cancelled',docstatus=2 WHERE receipt_series='"+str(self.name)+"' ")

	def on_trash(self):
		frappe.db.sql("DELETE FROM `tabTask Allocation` WHERE mr_inward='"+str(self.name)+"' ",as_dict=1)

	def on_submit(self):
		super().on_submit()
		for i in self.get("items"):
			if(i.inspection_status):
				pass
			else:
				frappe.throw("Inspection status mandatory")
		# for i in self.get("items"):
		# 	if(i.item_inspection==None and self.is_return==0 and self.is_subcontracted==0):
		# 		frappe.throw('Receipt should be Inspected')

@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
	from erpnext.accounts.party import get_payment_terms_template
	from erpnext.stock.doctype.purchase_receipt.purchase_receipt import get_returned_qty_map,get_invoiced_qty_map

	doc = frappe.get_doc("Purchase Receipt", source_name)
	returned_qty_map = get_returned_qty_map(source_name)
	invoiced_qty_map = get_invoiced_qty_map(source_name)

	def set_missing_values(source, target):
		if len(target.get("items")) == 0:
			frappe.throw(_("All items have already been Invoiced/Returned"))

		doc = frappe.get_doc(target)
		doc.payment_terms_template = get_payment_terms_template(
			source.supplier, "Supplier", source.company
		)
		doc.run_method("onload")
		doc.run_method("set_missing_values")
		doc.run_method("calculate_taxes_and_totals")
		doc.set_payment_schedule()

	def update_item(source_doc, target_doc, source_parent):
		target_doc.qty, returned_qty = get_pending_qty(source_doc)
		if frappe.db.get_single_value(
			"Buying Settings", "bill_for_rejected_quantity_in_purchase_invoice"
		):
			target_doc.rejected_qty = 0
		target_doc.stock_qty = flt(target_doc.qty) * flt(
			target_doc.conversion_factor, target_doc.precision("conversion_factor")
		)
		returned_qty_map[source_doc.name] = returned_qty

	def get_not_received_item(source_doc,target_doc,source_parent):
		ar=[]
		for i in source_doc.not_received_items:
			target_doc.append("items",{
				"item_code":i.item_code,
				"item_name":i.item_name,
				"description":i.description,
				"technical_description":i.technical_description,
				"qty":i.received_qty,
				"uom":i.uom,
				"price_list_rate":i.price_list_rate,
				"discount_percentage":i.discount_percentage,
				"descount_amount":i.discount_amount,
				"expence_account":target_doc.expense_head,
				"project":target_doc.project,
				"rate":i.rate,
				"amount":i.amount
				})
		# 	ar.append(i)
		# frappe.msgprint("test")
		return ar

	def get_pending_qty(item_row):
		qty = item_row.qty
		if frappe.db.get_single_value(
			"Buying Settings", "bill_for_rejected_quantity_in_purchase_invoice"
		):
			qty = item_row.received_qty
		pending_qty = qty - invoiced_qty_map.get(item_row.name, 0)
		returned_qty = flt(returned_qty_map.get(item_row.name, 0))
		if returned_qty:
			if returned_qty >= pending_qty:
				pending_qty = 0
				returned_qty -= pending_qty
			else:
				pending_qty -= returned_qty
				returned_qty = 0
		return pending_qty, returned_qty

	doclist = get_mapped_doc(
		"Purchase Receipt",
		source_name,
		{
			"Purchase Receipt": {
				"doctype": "Purchase Invoice",
				"field_map": {
					"supplier_warehouse": "supplier_warehouse",
					"is_return": "is_return",
					"bill_date": "bill_date",
				},
				"validation": {
					"docstatus": ["=", 1],
				},
				"postprocess": get_not_received_item,
			},
			"Purchase Receipt Item": {
				"doctype": "Purchase Invoice Item",
				"field_map": {
					"name": "pr_detail",
					"parent": "purchase_receipt",
					"purchase_order_item": "po_detail",
					"purchase_order": "purchase_order",
					"is_fixed_asset": "is_fixed_asset",
					"asset_location": "asset_location",
					"asset_category": "asset_category",
				},
				"postprocess": update_item,
				"filter": lambda d: get_pending_qty(d)[0] <= 0
				if not doc.get("is_return")
				else get_pending_qty(d)[0] > 0,
			},
			"Purchase Taxes and Charges": {"doctype": "Purchase Taxes and Charges", "add_if_empty": True},
		},
		target_doc,
		set_missing_values,
	)

	doclist.set_onload("ignore_price_list", True)
	return doclist
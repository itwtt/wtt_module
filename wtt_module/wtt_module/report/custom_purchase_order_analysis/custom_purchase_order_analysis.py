# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import copy

import frappe
from frappe import _
from frappe.utils import date_diff, flt, getdate


def execute(filters=None):
	if not filters:
		return [], []

	validate_filters(filters)

	columns = get_columns(filters)
	conditions = get_conditions(filters)

	data = get_data(conditions, filters)

	if not data:
		return [], [], None, []

	data = prepare_data(data, filters)

	return columns, data, None

def validate_filters(filters):
	from_date, to_date = filters.get("from_date"), filters.get("to_date")

	if not from_date and to_date:
		frappe.throw(_("From and To Dates are required."))
	elif date_diff(to_date, from_date) < 0:
		frappe.throw(_("To Date cannot be before From Date."))

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date") and filters.get("to_date"):
		conditions += " and po.transaction_date between %(from_date)s and %(to_date)s"

	for field in ['company', 'name']:
		if filters.get(field):
			conditions += f" and po.{field} = %({field})s"

	if filters.get('status'):
		conditions += " and po.status in %(status)s"

	if filters.get('project'):
		conditions += " and poi.project = %(project)s"

	return conditions

def get_data(conditions, filters):
	data = frappe.db.sql("""
		SELECT
			po.transaction_date as date,
			poi.schedule_date as required_date,
			poi.project,
			poi.description,poi.technical_description,poi.supplier_description,
			po.name as purchase_order,
			po.status, po.supplier, poi.item_code,
			poi.qty, poi.received_qty,
			poi.uom as uom,
			(poi.qty - poi.received_qty) AS pending_qty,
			IFNULL(pii.qty, 0) as billed_qty,
			poi.base_amount as amount,
			poi.price_list_rate as price,
			poi.discount_percentage as discount,
			poi.discount_amount as discount_amount,
			(poi.received_qty * poi.base_rate) as received_qty_amount,
			(poi.billed_amt * IFNULL(po.conversion_rate, 1)) as billed_amount,
			(poi.base_amount - (poi.billed_amt * IFNULL(po.conversion_rate, 1))) as pending_amount,
			po.set_warehouse as warehouse,
			po.company, poi.name
		FROM
			`tabPurchase Order` po,
			`tabPurchase Order Item` poi
		LEFT JOIN `tabPurchase Invoice Item` pii
			ON pii.po_detail = poi.name
		WHERE
			poi.parent = po.name
			and po.status not in ('Stopped', 'Closed')
			and po.docstatus = 1
			{0}
		GROUP BY poi.name
		ORDER BY po.transaction_date ASC
	""".format(conditions), filters, as_dict=1)

	return data

def prepare_data(data, filters):
	completed, pending = 0, 0
	pending_field =  "pending_amount"
	completed_field = "billed_amount"

	if filters.get("group_by_po"):
		purchase_order_map = {}

	for row in data:
		# sum data for chart
		completed += row[completed_field]
		pending += row[pending_field]

		# prepare data for report view
		row["qty_to_bill"] = flt(row["qty"]) - flt(row["billed_qty"])

		if filters.get("group_by_po"):
			po_name = row["purchase_order"]

			if not po_name in purchase_order_map:
				# create an entry
				row_copy = copy.deepcopy(row)
				purchase_order_map[po_name] = row_copy
			else:
				# update existing entry
				po_row = purchase_order_map[po_name]
				po_row["required_date"] = min(getdate(po_row["required_date"]), getdate(row["required_date"]))

				# sum numeric columns
				fields = ["description","technical_description","qty","price","discount","discount_amount", "received_qty", "pending_qty", "billed_qty", "qty_to_bill", "amount",
					"received_qty_amount", "billed_amount", "pending_amount"]
				for field in fields:
					po_row[field] = flt(row[field]) + flt(po_row[field])

	

	if filters.get("group_by_po"):
		data = []
		for po in purchase_order_map:
			data.append(purchase_order_map[po])
		return data, chart_data

	return data

def get_columns(filters):
	columns = [
		{
			"label":_("Date"),
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 90
		},
		{
			"label":_("Required By"),
			"fieldname": "required_date",
			"fieldtype": "Date",
			"width": 90
		},
		{
			"label": _("Purchase Order"),
			"fieldname": "purchase_order",
			"fieldtype": "Link",
			"options": "Purchase Order",
			"width": 160
		},
		{
			"label":_("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 130
		},
		{
			"label": _("Supplier"),
			"fieldname": "supplier",
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 130
		},{
			"label": _("Project"),
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",
			"width": 130
		}]

	if not filters.get("group_by_po"):
		columns.append({
			"label":_("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 100
		})

	columns.extend([
		{
			"label": _("Description"),
			"fieldname": "description",
			"fieldtype": "Small Text",
			"width": 120,
			"convertible": "description"
		},
		{
			"label": _("Technical Description"),
			"fieldname": "technical_description",
			"fieldtype": "Small Text",
			"width": 120,
			"convertible": "technical_description"
		},
		{
			"label": _("Supplier Description"),
			"fieldname": "supplier_description",
			"fieldtype": "Small Text",
			"width": 120,
			"convertible": "supplier_description"
		},
		{
			"label": _("Qty"),
			"fieldname": "qty",
			"fieldtype": "Float",
			"width": 120,
			"convertible": "qty"
		},
		{
			"label": _("UOM"),
			"fieldname": "uom",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Price"),
			"fieldname": "price",
			"fieldtype": "Float",
			"width": 120,
			"convertible": "price"
		},
		{
			"label": _("Discount"),
			"fieldname": "discount",
			"fieldtype": "Percentage",
			"width": 120,
			"convertible": "discount"
		},
		{
			"label": _("Discount Amount"),
			"fieldname": "discount_amount",
			"fieldtype": "Float",
			"width": 120,
			"convertible": "discount_amount"
		},
		{
			"label": _("Received Qty"),
			"fieldname": "received_qty",
			"fieldtype": "Float",
			"width": 120,
			"convertible": "qty"
		},
		{
			"label": _("Pending Qty"),
			"fieldname": "pending_qty",
			"fieldtype": "Float",
			"width": 80,
			"convertible": "qty"
		},
		{
			"label": _("Billed Qty"),
			"fieldname": "billed_qty",
			"fieldtype": "Float",
			"width": 80,
			"convertible": "qty"
		},
		{
			"label": _("Qty to Bill"),
			"fieldname": "qty_to_bill",
			"fieldtype": "Float",
			"width": 80,
			"convertible": "qty"
		},
		{
			"label": _("Amount"),
			"fieldname": "amount",
			"fieldtype": "Currency",
			"width": 110,
			"options": "Company:company:default_currency",
			"convertible": "rate"
		},
		{
			"label": _("Billed Amount"),
			"fieldname": "billed_amount",
			"fieldtype": "Currency",
			"width": 110,
			"options": "Company:company:default_currency",
			"convertible": "rate"
		},
		{
			"label": _("Pending Amount"),
			"fieldname": "pending_amount",
			"fieldtype": "Currency",
			"width": 130,
			"options": "Company:company:default_currency",
			"convertible": "rate"
		},
		{
			"label": _("Received Qty Amount"),
			"fieldname": "received_qty_amount",
			"fieldtype": "Currency",
			"width": 130,
			"options": "Company:company:default_currency",
			"convertible": "rate"
		},
		{
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 100
		},
		{
			"label": _("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 100
		}
	])

	return columns

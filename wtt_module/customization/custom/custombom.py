# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import functools
from collections import deque
from operator import itemgetter
from typing import List

import frappe
from frappe import _
from frappe.core.doctype.version.version import get_diff
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, cstr, flt, today
from frappe.website.website_generator import WebsiteGenerator
import json
import erpnext
from erpnext.setup.utils import get_exchange_rate
from erpnext.stock.doctype.item.item import get_item_details
from erpnext.stock.get_item_details import get_conversion_factor, get_price_list_rate

from erpnext.manufacturing.doctype.bom.bom import BOM

form_grid_templates = {
	"items": "templates/form_grid/item_grid.html"
}


class custombom(BOM):
	pass





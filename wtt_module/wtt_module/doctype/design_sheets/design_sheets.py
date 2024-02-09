# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt
import frappe
from frappe.utils.nestedset import NestedSet, get_root_of
from erpnext.utilities.transaction_base import delete_events
class DesignSheets(NestedSet):
	pass
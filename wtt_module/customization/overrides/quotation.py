from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate, nowdate
from num2words import num2words


from erpnext.selling.doctype.quotation.quotation import Quotation
form_grid_templates = {"items": "templates/form_grid/item_grid.html"}


class customQuotation(Quotation):
	def validate(self):
		pass
		# super().validate()
		# if(self.rounded_total!=None):
		# 	valword=num2words(self.rounded_total, lang='en_IN')
		# 	self.amount_in_words=valword.capitalize()
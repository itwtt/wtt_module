# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class NationalHolidayList(Document):
	def on_submit(self):
		doc=frappe.new_doc("Holiday List")
		doc.holiday_list_name=self.holiday_list_name
		doc.from_date=self.from_date
		doc.to_date=self.to_date
		doc.total_holidays=self.total_holidays
		for i in self.get("holidays"):
			doc.append("holidays",{
					"holiday_date":i.holiday_date,
					"description":i.description
					})
		doc.save()
		frappe.db.commit()

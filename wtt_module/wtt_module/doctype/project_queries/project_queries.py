import frappe
from frappe.model.document import Document

class ProjectQueries(Document):
	def validate(self):
		doc=frappe.new_doc("Query Reply")
		doc.query=self.name
		doc.reply_to=self.employee
		doc.reply_name=self.employee_name
		doc.query_against=self.query_against
		doc.project=self.project
		doc.system_1=self.system_1
		doc.system_2=self.system_2
		doc.queries=self.queries
		doc.employee=""

		doc.save(ignore_permissions=True)
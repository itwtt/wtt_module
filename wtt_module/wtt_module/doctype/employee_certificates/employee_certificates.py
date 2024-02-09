import frappe
from frappe.model.document import Document

class EmployeeCertificates(Document):
	def on_submit(self):
		for i in self.get("certificates"):
			gug=frappe.get_doc("Employee",self.employee)
			gug.append("certificates",{
				"certificate_name":i.certificate_name,
				"attachment":i.attachment
				})
			gug.save()
			frappe.db.commit()
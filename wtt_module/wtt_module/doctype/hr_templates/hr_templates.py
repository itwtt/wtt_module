import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class HRTemplates(Document):
	pass
@frappe.whitelist()
def get_candidate(source_name, target_doc=None):
	def postprocess(source, target):
		pass
	doc = get_mapped_doc("Job App", source_name, {
		"Job App": {
			"doctype": "HR Templates",
			"field_map": {
				"applicant_name":"candidate_name",
				"email_id":"mail",
				"name":"job_id",
				"applying_post":"position",
				"other_post":"position_name"
			}
		}
	}, target_doc,postprocess)
	return doc
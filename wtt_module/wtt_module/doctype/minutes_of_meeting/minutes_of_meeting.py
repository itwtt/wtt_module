import frappe
from datetime import date
from frappe.model.document import Document

class MinutesofMeeting(Document):
	pass

@frappe.whitelist()
def get_participants(conference_hall_booking):
	query = frappe.db.sql("""
	SELECT GROUP_CONCAT(CONCAT(employee_name, ' - ', status)) AS emp
	FROM `tabParticipants`
	WHERE parent = %s
	GROUP BY parent
	""", (conference_hall_booking,), as_dict=1)

	doc = frappe.get_doc("Meeting Slot Booking", conference_hall_booking)

	response = [{
	"participants": query[0].emp if query else "",
	"project": doc.project,
	"review_no": doc.review_no,
	"from_time": doc.from_time,
	"to_time": doc.to_time,
	"venue":doc.venue
	}]

	return response

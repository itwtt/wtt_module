frappe.views.calendar["Leave Table"] = {
	field_map: {
		"start": "from_date",
		"end": "to_date",
		"id": "name",
		"title": "employee",
		"allDay": "allDay",
		"progress": "progress"
	}
	get_events_method: "frappe.desk.calendar.get_events"
}
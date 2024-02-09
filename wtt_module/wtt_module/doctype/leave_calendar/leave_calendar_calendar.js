frappe.views.calendar["Leave Calendar"] = {
        field_map: {
                "start": "from_date",
                "end": "to_date",
                "id": "employee",
                "title": "employee_name",
                "status": "status",
                "color":"color"
        },
        get_events_method: "wtt_module.wtt_module.doctype.leave_calendar.leave_calendar.get_calendar",
}
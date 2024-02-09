# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeaveCalendar(Document):
	pass
@frappe.whitelist()
def get_calendar(start, end):
        if not frappe.has_permission("Leave Calendar", "read"):
                raise frappe.PermissionError

        return frappe.db.sql("""select
                from_date,
                to_date,
                employee_name,
                leave_type,
                request_number,
                reason,
                status,
                color,
                0 as all_day
        from `tabLeave Calendar`""",as_dict=True)
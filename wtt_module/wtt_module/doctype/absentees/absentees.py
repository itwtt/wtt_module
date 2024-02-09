# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Absentees(Document):
	pass
@frappe.whitelist()
def get_calendar(start, end):
        if not frappe.has_permission("Absentees", "read"):
                raise frappe.PermissionError

        return frappe.db.sql("""select
                date,
                employee_name,
                title,
                status,
                reason,
                color,
                name,
                0 as all_day
        from `tabAbsentees` ORDER BY status""",as_dict=True)
        # GROUP_CONCAT(distinct(employee_name))as employee_name,
from __future__ import unicode_literals

import frappe

def get_context(context):
	# do your magic here
	pass
@frappe.whitelist()
def checkprev(name,email,dob,father,arr):
	to_python = json.loads(arr)
	# frappe.db.sql("DELETE FROM `tabJob App` WHERE applicant_name='"+str(name)+"' and fathers_name='"+str(father)+"' and email_id='"+str(email)+"' and date_of_birth='"+str(dob)+"' ",as_dict=1)	
	return True

import frappe
from frappe.model.document import Document
from frappe import _
from docx import Document as dd
from datetime import date
from frappe.utils.background_jobs import enqueue
import subprocess
import pdfplumber
import traceback
import pyotp

class VerifyOTP(Document):
	def validate(self):
		proposal=frappe.db.sql("SELECT * from `tabProposal` where secret_key='"+str(self.otp)+"' ORDER BY creation DESC LIMIT 1",as_dict=1)
		if(proposal):
			for val in proposal:
				cap='V1'
				if(val.capacity=='AQUANZER V2 - 50 KLD'):
					cap='V2'
				elif(val.capacity=='AQUANZER V3 - 75 KLD'):
					cap='V3'
				elif(val.capacity=='AQUANZER V1 - 25 KLD'):
					cap='V1'
				elif(val.capacity=='AQUANZER V4 - 100 KLD'):
					cap='V4'
				message='<html><head><link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet"></head><body>'
				message+='<p style="font-family: Roboto;color: #2f5597;">Dear '+str(val.client_name)+',<br><br>Have a Happy Day..<br><br>Greetings from <span style="color:#012673"><b>WTT</b></span> <span style="color:darkorange"><b>INTERNATIONAL</b></span> !!!<br><br>	'
				message+='&emsp;&emsp;&emsp;We feel delighted to launch our new product AQUANZER. This is our innovative solution and it has been tailored to provide an effluent treatment plant in a small footprint.<br><br>'
				message+='&emsp;&emsp;&emsp;We are pleased to share our proposal for a Containerized ETP, with a plant capacity of '+str(val.capacity)+', we believe that it will be perfectly suits to your needs for an efficient and compact <br>effluent treatment plant.<br>'
				message+='<br>&emsp;&emsp;&emsp;If you have any questions or would like to place an order, please don\'t hesitate to get in touch with our customer service team, who will be happy to assist you.</body></html>'
				filename = '8388ae662e'
				file_doc = frappe.get_doc('File', filename)
				if file_doc:
					try:
						file_path = frappe.utils.file_manager.get_file_path(file_doc.file_url)

						with open(file_path, 'rb') as file:
							pdf = pdfplumber.open(file)
							page_content = []
							for page in pdf.pages:
								text = page.extract_text()
								page_content.append(text)
							pdf.close()

							email_args = {
								"sender":'noreply@wttindia.com',
								"recipients": [val.email],
								"message": message,
								"subject": 'Techno-Commercial proposal for AQUANZER '+str(cap),
								"attachments": [{'fcontent': file_doc.get_content(),'content_type':'application/pdf', 'fname': 'Techno-Commercial Proposal.pdf'}],
							}

							frappe.sendmail(**email_args)
					except Exception as e:
						frappe.msgprint(f"Error: {str(e)}")
						traceback.print_exc()
				else:
					frappe.msgprint(f"File '{filename}' not found.")


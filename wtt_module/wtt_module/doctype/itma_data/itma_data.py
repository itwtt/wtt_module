# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe.model.document import Document
import traceback
import pyotp
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from email.mime.base import MIMEBase
from email import encoders
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes
import smtplib

class ITMAData(Document):
	def validate(self):
		pass
		# for i in self.itma_details:
		# 	if(i.wa==0):
		# 		url = "https://api.ultramsg.com/instance49474/messages/chat"
		# 		payload = "token=q41sf53o0nu6bske&to="+str(i.col4)+"&body=Hello "+str(i.col0)+",\n\n Greetings from WTT INTERNATIONAL!\n\nThanks for sparing your valuable time to visit us at ITMA\n\nWe are all set to serve your WTP, ETP and Zero Liquid Discharge requirement."
		# 		payload = payload.encode('utf8').decode('iso-8859-1')
		# 		headers = {'content-type': 'application/x-www-form-urlencoded'}
		# 		response = requests.request("POST", url, data=payload, headers=headers)
		# 		# frappe.msgprint(str(response.text))
		# 		i.wa=1
		# 	else:
		# 		pass
@frappe.whitelist()
def send_bang(client_name,phone,pic):
	url = "https://api.ultramsg.com/instance76643/messages/image"
	payload = "token=vzf53zhuj3vgwnby&to="+str(phone)+"&image=https://erp.wttindia.com"+str(pic)+"&caption=Dear "+str(client_name)+",\n\nHappy Greetings from *WTT INTERNATIONAL PVT LTD!*\n\nThank you so much for visiting us at the *DTG Exhibition*\n\nIt was a pleasure meeting you and discussing our products. We appreciate your interest and hope you found our offerings Interesting. If you have any further questions or require additional information, feel free to reach us.\n\nWe look forward to the possibility of working with your esteemed organization.\n\nShare with us your valuable Enquiries through the link below\nhttps://bit.ly/WTT-NewPlant\n\nBest regards,\n*D.Venkatesh (CEO/MD)*\nWTT INTERNATIONAL PVT. LTD.\nhttps://www.wttint.com/"
	payload = payload.encode('utf8').decode('iso-8859-1')
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	response = requests.request("POST", url, data=payload, headers=headers)
	frappe.msgprint(str(response.text))
	return response

@frappe.whitelist()
def bang_broucher_only(phone):
	url = "https://api.ultramsg.com/instance76643/messages/document"
	payload = "token=vzf53zhuj3vgwnby&to="+str(phone)+"&filename=WTT-BROCHURE.pdf&document=https://erp.wttindia.com/files/WTTBROCHURE2024.pdf&caption=WTT INTERNATIONAL"
	payload = payload.encode('utf8').decode('iso-8859-1')
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	response = requests.request("POST", url, data=payload, headers=headers)
	return response

@frappe.whitelist()
def send_message(client_name,phone):
	url = "https://api.ultramsg.com/instance49474/messages/chat"
	payload = "token=q41sf53o0nu6bske&to="+str(phone)+"&body=Dear "+str(client_name)+",\n\nHappy Greetings from *WTT INTERNATIONAL PVT LTD!*\n\nWe are delighted to meet you in *ITMA-2023*\n\nThank you for listening us and your most valuable enquiries. Kindly keep in touch with us for an accurate solution for your requirements. Meantime, Kindly go through with our brochure.\n\n*We are all set to serve your Water Treatment Needs.*\n\nEnquiry Form Link:\nhttps://bit.ly/3VEFuFZ\n\nThanks and regards.\n*Venkatesh D*"
	payload = payload.encode('utf8').decode('iso-8859-1')
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	response = requests.request("POST", url, data=payload, headers=headers)
	return response

@frappe.whitelist()
def send_pic(client_name,phone,pic):
	url = "https://api.ultramsg.com/instance49474/messages/image"
	payload = "token=q41sf53o0nu6bske&to="+str(phone)+"&image=https://erp.wttindia.com"+str(pic)+"&caption=Dear "+str(client_name)+",\n\nHappy Greetings from *WTT INTERNATIONAL PVT LTD!*\n\nWe are delighted to meet you in *ITMA-2023*\n\nThank you for listening us and your most valuable enquiries. Kindly keep in touch with us for an accurate solution for your requirements. Meantime, Kindly go through with our brochure.\n\n*We are all set to serve your Water Treatment Needs.*\n\nEnquiry Form Link:\nhttps://bit.ly/3VEFuFZ\n\nThanks and regards.\n*Venkatesh D*"
	payload = payload.encode('utf8').decode('iso-8859-1')
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	response = requests.request("POST", url, data=payload, headers=headers)
	frappe.msgprint(str(response.text))
	return response

@frappe.whitelist()
def send_bro(client_name,phone,broucher):
	url = "https://api.ultramsg.com/instance49474/messages/document"
	payload = "token=q41sf53o0nu6bske&to="+str(phone)+"&filename=WTT-BROCHURE.pdf&document=https://erp.wttindia.com"+str(broucher)+"&caption=Dear "+str(client_name)+",\n\nHappy Greetings from *WTT INTERNATIONAL PVT LTD!*\n\nWe are delighted to meet you in *ITMA-2023*\n\nThank you for listening us and your most valuable enquiries. Kindly keep in touch with us for an accurate solution for your requirements.\n\nMeantime, Kindly go through with our brochure.\n\n*We are all set to serve your Water Treatment Needs.*\n\nEnquiry Form Link:\nhttps://bit.ly/3VEFuFZ\n\nThanks and regards.\n*Venkatesh D*"
	payload = payload.encode('utf8').decode('iso-8859-1')
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	response = requests.request("POST", url, data=payload, headers=headers)
	return response

@frappe.whitelist()
def broucher_only(phone,broucher):
	url = "https://api.ultramsg.com/instance49474/messages/document"
	payload = "token=q41sf53o0nu6bske&to="+str(phone)+"&filename=WTT-BROCHURE.pdf&document=https://erp.wttindia.com"+str(broucher)+"&caption=WTT INTERNATIONAL"
	payload = payload.encode('utf8').decode('iso-8859-1')
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	response = requests.request("POST", url, data=payload, headers=headers)
	return response

@frappe.whitelist()
def send_mail(client_name,email):
	msg = MIMEMultipart('alternative')
	msg['From'] = 'WTT INTERNATIONAL'
	msg['To'] = str(email)
	msg['Subject'] = 'WTT INTERNATIONAL - ITMA 2023'
	html = "<i style='font-family:Roboto;font-size:15px;'>Dear "+str(client_name)+",<br><br>Happy Greetings from <b style='color:#2A375A'>WTT</b> <b style='color:#F26836'>INTERNATIONAL</b> <b>PVT LTD!</b><br><br>We are delighted to meet you in <b>ITMA-2023</b>.<br>Thank you for listening us and your most valuable enquiries. Kindly keep in touch with us for an accurate solution for your requirements.<br><br><b>We are all set to serve your Water Treatment Needs.</b><br><br>Enquiry Form Link:<br>https://bit.ly/3VEFuFZ<br><br>Thanks and regards.<br>RaghulRaj D</i>"
	msg.attach(MIMEText(html, 'html'))
	s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	s.login("enquiry@wttint.com", "stdpguzdqvbcgdqn")
	s.sendmail('enquiry@wttint.com',str(email), msg.as_string())
	s.quit()
	return msg

@frappe.whitelist()
def mail_broucher_content(client_name,email):
	fromaddr = "enquiry@wttint.com"
	toaddr = str(email)
	msg = MIMEMultipart()
	msg['From'] = 'WTT INTERNATIONAL'
	msg['To'] = toaddr
	msg['Subject'] = "WTT INTERNATIONAL - ITMA 2023"
	html = "<i style='font-family:Roboto;font-size:15px;'>Dear "+str(client_name)+",<br><br>Happy Greetings from <b style='color:#2A375A'>WTT</b> <b style='color:#F26836'>INTERNATIONAL</b> <b>PVT LTD!</b><br><br>We are delighted to meet you in <b>ITMA-2023</b>.<br>Thank you for listening us and your most valuable enquiries. Kindly keep in touch with us for an accurate solution for your requirements.<br><br><b>We are all set to serve your Water Treatment Needs.</b><br><br>Enquiry Form Link:<br>https://bit.ly/3VEFuFZ<br><br>Thanks and regards.<br>RaghulRaj D</i>"
	msg.attach(MIMEText(html, 'html'))
	filename = "/home/erp/erpnext14/sites/erp.wttindia.com/public/files/WTT.pdf"
	attachment = open(filename, "rb")
	p = MIMEBase('application', 'octet-stream')
	p.set_payload((attachment).read())
	encoders.encode_base64(p)
	p.add_header('Content-Disposition', "attachment; filename= %s" % 'WTT-BROCHURE.pdf')
	msg.attach(p)
	s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	# s.starttls()
	s.login(fromaddr, "stdpguzdqvbcgdqn")
	s.sendmail('enquiry@wttint.com',str(email), msg.as_string())
	s.quit()
	return msg

@frappe.whitelist()
def send_all(status):
	# filename = "/home/erp/erpnext14/sites/erp.wttindia.com/public/files/wttthanks.jpg"
	# url = "https://api.ultramsg.com/instance49474/messages/image"
	# payload = "token=q41sf53o0nu6bske&to=9698109426&image=https://erp.wttindia.com/files/wttthanks.jpg&caption=Dear Sathish\nGreetings from *WTT International*\n\nWe would like to express our sincere gratitude for making our *ITMA 2023* campaign a Great Success.\n\nWe are all set to serve your Water Treatment Needs,\n*Share with us your valuable Enquiries !!*\n\nThanks and Regards\nD.Venkatesh\nManaging Director\nWTT International\n\nhttps://wttint.com/"
	# payload = payload.encode('utf8').decode('iso-8859-1')
	# headers = {'content-type': 'application/x-www-form-urlencoded'}
	# response = requests.request("POST", url, data=payload, headers=headers)
	# frappe.msgprint(str(response.text))
	# return response
	for i in frappe.db.sql("SELECT client_name,phone_no FROM `tabITMA Data` WHERE phone_no!=''",as_dict=1):
		filename = "/home/erp/erpnext14/sites/erp.wttindia.com/public/files/wttthanks.jpg"
		url = "https://api.ultramsg.com/instance49474/messages/image"
		payload = "token=q41sf53o0nu6bske&to="+str(i.phone_no)+"&image=https://erp.wttindia.com/files/wttthanks.jpg&caption=Dear "+str(i.client_name)+"\nGreetings from *WTT International*\n\nWe would like to express our sincere gratitude for making our *ITMA 2023* campaign a Great Success.\n\nWe are all set to serve your Water Treatment Needs,\n*Share with us your valuable Enquiries !!*\n\nThanks and Regards\nD.Venkatesh\nManaging Director\nWTT International\n\nhttps://wttint.com/"
		payload = payload.encode('utf8').decode('iso-8859-1')
		headers = {'content-type': 'application/x-www-form-urlencoded'}
		response = requests.request("POST", url, data=payload, headers=headers)

@frappe.whitelist()
def send_all_mail(status):
	for i in frappe.db.sql("SELECT name,client_name,email,already_sent FROM `tabITMA Data` WHERE email!=''",as_dict=1):
		if(i.already_sent!='sent'):
			frappe.db.sql("UPDATE `tabITMA Data` SET already_sent = 'sent' WHERE email = '"+str(i.email)+"'")
			client =str(i.client_name)
			email_user = str(i.email)
			msg = EmailMessage()
			msg['Subject'] = 'WTT INTERNATIONAL - ITMA 2023'
			msg['From'] = 'WTT INTERNATIONAL'
			msg['To'] = email_user
			msg.set_content('')
			image_cid = make_msgid(domain='smtp.gmail.com')
			msg.add_alternative("""\
			<html>
			<body>
			<p>Dear """+str(client)+"""<br>Greetings from <b>WTT International</b><br><br>We would like to express our sincere gratitude for making our <b>ITMA 2023</b> campaign a Great Success.<br><br>We are all set to serve your Water Treatment Needs,<br><b>Share with us your valuable Enquiries !!</b><br><br>Thanks and Regards<br>D.Venkatesh<br>Managing Director<br>
			</p>
			<img style="width:50%" src="cid:{image_cid}">
			</body>
			</html>
			""".format(image_cid=image_cid[1:-1]), subtype='html')
			with open('/home/erp/erpnext14/sites/erp.wttindia.com/public/files/wttthanks.jpg', 'rb') as img:
				maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')
				msg.get_payload()[1].add_related(img.read(), 
				maintype=maintype, 
				subtype=subtype, 
				cid=image_cid)
				s = smtplib.SMTP('smtp.gmail.com', 587)
				s.starttls()
				s.login("enquiry@wttint.com", "stdpguzdqvbcgdqn")
				text = msg.as_string()
				s.sendmail('enquiry@wttint.com',email_user, text)
				s.quit()
			# doc = frappe.get_doc('ITMA Data', "ITMA-DET-00207")
			# doc.already_sent = 'work'
			# doc.save()

@frappe.whitelist()
def send_bakrid_wish(status):
	pass
	# for i in frappe.db.sql("SELECT name1,phone_no,status FROM `tabBangalesh leads` WHERE phone_no!=''",as_dict=1):
	# 	if(i.status != "sent"):
	# 		url = "https://api.ultramsg.com/instance49474/messages/image"
	# 		payload = "token=q41sf53o0nu6bske&to="+str(i.phone_no)+"&image=https://erp.wttindia.com/files/wtteid.png&caption=Dear "+str(i.name1)+"\n*Greetings on Eid-ul-Adha.* May this day bring happiness and prosperity to everyone. May it also uphold the spirit of togetherness and harmony in our society. *Eid Mubarak!*\n\nBest Regards\nD.Venkatesh\nManaging Director\n*WTT International*"
	# 		payload = payload.encode('utf8').decode('iso-8859-1')
	# 		headers = {'content-type': 'application/x-www-form-urlencoded'}
	# 		response = requests.request("POST", url, data=payload, headers=headers)

# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe.model.document import Document

class ITMAEnquiry(Document):
	def on_submit(self):
		if(self.send_wa==0):
			if(self.visitor_photo):
				url = "https://api.ultramsg.com/instance49474/messages/image"
				payload = "token=q41sf53o0nu6bske&to="+str(self.telephone)+"&image=https://erp.wttindia.com"+str(self.visitor_photo)+"&caption=Hello "+str(self.client_name)+",\n\n Greetings from WTT INTERNATIONAL!\n\nThanks for sparing your valuable time to visit us at ITMA\n\nWe are all set to serve your WTP, ETP and Zero Liquid Discharge requirement."
				payload = payload.encode('utf8').decode('iso-8859-1')
				headers = {'content-type': 'application/x-www-form-urlencoded'}
				response = requests.request("POST", url, data=payload, headers=headers)
				print(response.text)
			else:
				url = "https://api.ultramsg.com/instance49474/messages/chat"
				payload = "token=q41sf53o0nu6bske&to="+str(self.telephone)+"&body=Hello "+str(self.client_name)+",\n\n Greetings from WTT INTERNATIONAL!\n\nThanks for sparing your valuable time to visit us at ITMA\n\nWe are all set to serve your WTP, ETP and Zero Liquid Discharge requirement."
				payload = payload.encode('utf8').decode('iso-8859-1')
				headers = {'content-type': 'application/x-www-form-urlencoded'}
				response = requests.request("POST", url, data=payload, headers=headers)
				print(response.text)
				self.send_wa=1
		else:
			pass

# @frappe.whitelist()
# def send_message(st,client_name,phone,pic):
# 	if(st==0):
# 		if(pic):
# 			url = "https://api.ultramsg.com/instance44396/messages/image"
# 			payload = "token=a031eq5bfqqqxd1h&to="+str(phone)+"&image=https://erp.wttindia.com"+str(pic)+"&caption=Hello "+str(client_name)+",\n\n Greetings from WTT INTERNATIONAL!\n\nThanks for sparing your valuable time to visit us at ITMA\n\nWe are all set to serve your WTP, ETP and Zero Liquid Discharge requirement Kindly provide us your valuable enquiry by filling the Enquiry Sheet\n\nEnquiry Sheet Link: \nbit.ly/WTT-NewPlant"
# 			payload = payload.encode('utf8').decode('iso-8859-1')
# 			headers = {'content-type': 'application/x-www-form-urlencoded'}
# 			response = requests.request("POST", url, data=payload, headers=headers)
# 			frappe.msgprint(str(response.text))
# 		else:
# 			url = "https://api.ultramsg.com/instance44396/messages/chat"
# 			payload = "token=a031eq5bfqqqxd1h&to="+str(phone)+"&body=Hello "+str(client_name)+",\n\n Greetings from WTT INTERNATIONAL!\n\nThanks for sparing your valuable time to visit us at ITMA\n\nWe are all set to serve your WTP, ETP and Zero Liquid Discharge requirement Kindly provide us your valuable enquiry by filling the Enquiry Sheet\n\nEnquiry Sheet Link: \nbit.ly/WTT-NewPlant"
# 			payload = payload.encode('utf8').decode('iso-8859-1')
# 			headers = {'content-type': 'application/x-www-form-urlencoded'}
# 			response = requests.request("POST", url, data=payload, headers=headers)
# 			frappe.msgprint(str(response.text))
# 	else:
# 		pass
import frappe
from frappe import _, scrub, throw
from datetime import date,datetime,timedelta
from erpnext.hr.doctype.employee.employee import Employee

class customEmployee(Employee):
	def validate(self):
		super().validate()

		if(self.experience=='Experienced'):
			arr=[]
			arr2=[]
			for i in self.get('external_work_history'):
				arr.append(str(i.from_time))
				arr2.append(str(i.to_time))
			aa = str(arr[0])
			cc=len(arr2)-1
			bb = str(arr2[cc])
			datea=datetime.strptime(aa,'%Y-%m-%d')
			dateb=datetime.strptime(bb,'%Y-%m-%d')
			dif=dateb-datea
			diff = (dif.days + dif.seconds/86400)/365.2425
			self.total_work_experience=str(diff)
		
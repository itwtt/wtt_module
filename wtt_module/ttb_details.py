import frappe
@frappe.whitelist()
def ttb(aa):
	arr=[]
	vv=frappe.db.sql("""SELECT distinct(`tabPosition Specific`.`criteria`)as "criteria",
		`tabTechnical Criteria`.`employee`as "employee",`tabTechnical Criteria`.`employee_name` as "employee_name",
		(SELECT cc.`hod_points` FROM `tabPosition Specific`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabPosition Specific`.`criteria` and pp.`month`='December' and pp.`employee`='"""+str(aa)+"""') as 'dec',
		(SELECT cc.`name` FROM `tabPosition Specific`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabPosition Specific`.`criteria` and pp.`month`='December' and pp.`employee`='"""+str(aa)+"""') as 'dec_ref',
		(SELECT cc.`management_points` FROM `tabPosition Specific`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabPosition Specific`.`criteria` and pp.`month`='January' and pp.`employee`='"""+str(aa)+"""') as 'jan',
		(SELECT cc.`name` FROM `tabPosition Specific`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabPosition Specific`.`criteria` and pp.`month`='January' and pp.`employee`='"""+str(aa)+"""') as 'jan_ref',
		(SELECT cc.`management_points` FROM `tabPosition Specific`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabPosition Specific`.`criteria` and pp.`month`='February' and pp.`employee`='"""+str(aa)+"""') as 'feb',
		(SELECT cc.`name` FROM `tabPosition Specific`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabPosition Specific`.`criteria` and pp.`month`='February' and pp.`employee`='"""+str(aa)+"""') as 'feb_ref'
		FROM `tabPosition Specific` INNER JOIN `tabTechnical Criteria` ON `tabTechnical Criteria`.`name`=`tabPosition Specific`.`parent`
		where `tabTechnical Criteria`.`docstatus`!=2 and `tabTechnical Criteria`.`employee`='"""+str(aa)+"""' and `tabTechnical Criteria`.`month`='February'""",as_dict=1)
	for i in vv:
		arr.append({
			'employee':i.employee,
			'employee_name':i.employee_name,
			'criteria_type':"Position",
			'criteria':i.criteria,
			'dec':i.dec,
			'dec_ref':i.dec_ref,
			'jan':i.jan,
			'jan_ref':i.jan_ref,
			'feb':i.feb,
			'feb_ref':i.feb_ref
			})

	uu=frappe.db.sql("""SELECT distinct(`tabIndustry Specific`.`criteria`)as "criteria",
		`tabTechnical Criteria`.`employee`as "employee",`tabTechnical Criteria`.`employee_name` as "employee_name",
		(SELECT cc.`hod_points` FROM `tabIndustry Specific`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabIndustry Specific`.`criteria` and pp.`month`='December' and pp.`employee`='"""+str(aa)+"""') as 'dec',
		(SELECT cc.`name` FROM `tabIndustry Specific`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabIndustry Specific`.`criteria` and pp.`month`='December' and pp.`employee`='"""+str(aa)+"""') as 'dec_ref',
		(SELECT cc.`management_points` FROM `tabIndustry Specific`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabIndustry Specific`.`criteria` and pp.`month`='January' and pp.`employee`='"""+str(aa)+"""') as 'jan',
		(SELECT cc.`name` FROM `tabIndustry Specific`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabIndustry Specific`.`criteria` and pp.`month`='January' and pp.`employee`='"""+str(aa)+"""') as 'jan_ref',
		(SELECT cc.`management_points` FROM `tabIndustry Specific`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabIndustry Specific`.`criteria` and pp.`month`='February' and pp.`employee`='"""+str(aa)+"""') as 'feb',
		(SELECT cc.`name` FROM `tabIndustry Specific`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabIndustry Specific`.`criteria` and pp.`month`='February' and pp.`employee`='"""+str(aa)+"""') as 'feb_ref'
		FROM `tabIndustry Specific` INNER JOIN `tabTechnical Criteria` ON `tabTechnical Criteria`.`name`=`tabIndustry Specific`.`parent`
		where `tabTechnical Criteria`.`docstatus`!=2 and `tabTechnical Criteria`.`employee`='"""+str(aa)+"""' and `tabTechnical Criteria`.`month`='February'""",as_dict=1)
	for i in uu:
		arr.append({
			'employee':i.employee,
			'employee_name':i.employee_name,
			'criteria_type':"Industry",
			'criteria':i.criteria,
			'dec':i.dec,
			'dec_ref':i.dec_ref,
			'jan':i.jan,
			'jan_ref':i.jan_ref,
			'feb':i.feb,
			'feb_ref':i.feb_ref
			})
	ww=frappe.db.sql("""SELECT distinct(`tabCommon Skills`.`criteria`)as "criteria",
		`tabTechnical Criteria`.`employee`as "employee",`tabTechnical Criteria`.`employee_name` as "employee_name",
		(SELECT cc.`hod_points` FROM `tabCommon Skills`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabCommon Skills`.`criteria` and pp.`month`='December' and pp.`employee`='"""+str(aa)+"""') as 'dec',
		(SELECT cc.`name` FROM `tabCommon Skills`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabCommon Skills`.`criteria` and pp.`month`='December' and pp.`employee`='"""+str(aa)+"""') as 'dec_ref',
		(SELECT cc.`management_points` FROM `tabCommon Skills`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabCommon Skills`.`criteria` and pp.`month`='January' and pp.`employee`='"""+str(aa)+"""') as 'jan',
		(SELECT cc.`name` FROM `tabCommon Skills`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabCommon Skills`.`criteria` and pp.`month`='January' and pp.`employee`='"""+str(aa)+"""') as 'jan_ref',
		(SELECT cc.`management_points` FROM `tabCommon Skills`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabCommon Skills`.`criteria` and pp.`month`='February' and pp.`employee`='"""+str(aa)+"""') as 'feb',
		(SELECT cc.`name` FROM `tabCommon Skills`as cc INNER JOIN `tabTechnical Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabCommon Skills`.`criteria` and pp.`month`='February' and pp.`employee`='"""+str(aa)+"""') as 'feb_ref'
		FROM `tabCommon Skills` INNER JOIN `tabTechnical Criteria` ON `tabTechnical Criteria`.`name`=`tabCommon Skills`.`parent`
		where `tabTechnical Criteria`.`docstatus`!=2 and `tabTechnical Criteria`.`employee`='"""+str(aa)+"""' and `tabTechnical Criteria`.`month`='February'""",as_dict=1)
	for i in ww:
		arr.append({
			'employee':i.employee,
			'employee_name':i.employee_name,
			'criteria_type':"Common",
			'criteria':i.criteria,
			'dec':i.dec,
			'dec_ref':i.dec_ref,
			'jan':i.jan,
			'jan_ref':i.jan_ref,
			'feb':i.feb,
			'feb_ref':i.feb_ref
			})
	aa=frappe.db.sql("""SELECT distinct(`tabAttitude Table`.`criteria`)as "criteria","Attitude" as "criteria_type",
		`tabBehavioural Criteria`.`employee`as "employee",`tabBehavioural Criteria`.`employee_name` as "employee_name",
		(SELECT cc.`hod_points` FROM `tabAttitude Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabAttitude Table`.`criteria` and pp.`month`='December' and pp.`employee`='WTT1351') as 'dec',
		(SELECT cc.`name` FROM `tabAttitude Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabAttitude Table`.`criteria` and pp.`month`='December' and pp.`employee`='WTT1351') as 'dec_ref',
		(SELECT cc.`management_points` FROM `tabAttitude Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabAttitude Table`.`criteria` and pp.`month`='January' and pp.`employee`='WTT1351') as 'jan',
		(SELECT cc.`name` FROM `tabAttitude Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabAttitude Table`.`criteria` and pp.`month`='January' and pp.`employee`='WTT1351') as 'jan_ref',
		(SELECT cc.`management_points` FROM `tabAttitude Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabAttitude Table`.`criteria` and pp.`month`='February' and pp.`employee`='WTT1351') as 'feb',
		(SELECT cc.`name` FROM `tabAttitude Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabAttitude Table`.`criteria` and pp.`month`='February' and pp.`employee`='WTT1351') as 'feb_ref'
		FROM `tabAttitude Table` INNER JOIN `tabBehavioural Criteria` ON `tabBehavioural Criteria`.`name`=`tabAttitude Table`.`parent`
		where `tabBehavioural Criteria`.`docstatus`!=2 and `tabBehavioural Criteria`.`employee`='WTT1351' and `tabBehavioural Criteria`.`month`='February' union
		SELECT distinct(`tabPersonal Table`.`criteria`)as "criteria","Personal" as "criteria_type",
		`tabBehavioural Criteria`.`employee`as "employee",`tabBehavioural Criteria`.`employee_name` as "employee_name",
		(SELECT cc.`hod_points` FROM `tabPersonal Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabPersonal Table`.`criteria` and pp.`month`='December' and pp.`employee`='WTT1351') as 'dec',
		(SELECT cc.`name` FROM `tabPersonal Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabPersonal Table`.`criteria` and pp.`month`='December' and pp.`employee`='WTT1351') as 'dec_ref',
		(SELECT cc.`management_points` FROM `tabPersonal Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabPersonal Table`.`criteria` and pp.`month`='January' and pp.`employee`='WTT1351') as 'jan',
		(SELECT cc.`name` FROM `tabPersonal Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabPersonal Table`.`criteria` and pp.`month`='January' and pp.`employee`='WTT1351') as 'jan_ref',
		(SELECT cc.`management_points` FROM `tabPersonal Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabPersonal Table`.`criteria` and pp.`month`='February' and pp.`employee`='WTT1351') as 'feb',
		(SELECT cc.`name` FROM `tabPersonal Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabPersonal Table`.`criteria` and pp.`month`='February' and pp.`employee`='WTT1351') as 'feb_ref'
		FROM `tabPersonal Table` INNER JOIN `tabBehavioural Criteria` ON `tabBehavioural Criteria`.`name`=`tabPersonal Table`.`parent`
		where `tabBehavioural Criteria`.`docstatus`!=2 and `tabBehavioural Criteria`.`employee`='WTT1351' and `tabBehavioural Criteria`.`month`='February' union
		SELECT distinct(`tabSkill Table`.`criteria`)as "criteria","Skill" as "criteria_type",
		`tabBehavioural Criteria`.`employee`as "employee",`tabBehavioural Criteria`.`employee_name` as "employee_name",
		(SELECT cc.`hod_points` FROM `tabSkill Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabSkill Table`.`criteria` and pp.`month`='December' and pp.`employee`='WTT1351') as 'dec',
		(SELECT cc.`name` FROM `tabSkill Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabSkill Table`.`criteria` and pp.`month`='December' and pp.`employee`='WTT1351') as 'dec_ref',
		(SELECT cc.`management_points` FROM `tabSkill Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabSkill Table`.`criteria` and pp.`month`='January' and pp.`employee`='WTT1351') as 'jan',
		(SELECT cc.`name` FROM `tabSkill Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabSkill Table`.`criteria` and pp.`month`='January' and pp.`employee`='WTT1351') as 'jan_ref',
		(SELECT cc.`management_points` FROM `tabSkill Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabSkill Table`.`criteria` and pp.`month`='February' and pp.`employee`='WTT1351') as 'feb',
		(SELECT cc.`name` FROM `tabSkill Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabSkill Table`.`criteria` and pp.`month`='February' and pp.`employee`='WTT1351') as 'feb_ref'
		FROM `tabSkill Table` INNER JOIN `tabBehavioural Criteria` ON `tabBehavioural Criteria`.`name`=`tabSkill Table`.`parent`
		where `tabBehavioural Criteria`.`docstatus`!=2 and `tabBehavioural Criteria`.`employee`='WTT1351' and `tabBehavioural Criteria`.`month`='February' union
		SELECT distinct(`tabTeam Table`.`criteria`)as "criteria","Team" as "criteria_type",
		`tabBehavioural Criteria`.`employee`as "employee",`tabBehavioural Criteria`.`employee_name` as "employee_name",
		(SELECT cc.`hod_points` FROM `tabTeam Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabTeam Table`.`criteria` and pp.`month`='December' and pp.`employee`='WTT1351') as 'dec',
		(SELECT cc.`name` FROM `tabTeam Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabTeam Table`.`criteria` and pp.`month`='December' and pp.`employee`='WTT1351') as 'dec_ref',
		(SELECT cc.`management_points` FROM `tabTeam Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabTeam Table`.`criteria` and pp.`month`='January' and pp.`employee`='WTT1351') as 'jan',
		(SELECT cc.`name` FROM `tabTeam Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabTeam Table`.`criteria` and pp.`month`='January' and pp.`employee`='WTT1351') as 'jan_ref',
		(SELECT cc.`management_points` FROM `tabTeam Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabTeam Table`.`criteria` and pp.`month`='February' and pp.`employee`='WTT1351') as 'feb',
		(SELECT cc.`name` FROM `tabTeam Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabTeam Table`.`criteria` and pp.`month`='February' and pp.`employee`='WTT1351') as 'feb_ref'
		FROM `tabTeam Table` INNER JOIN `tabBehavioural Criteria` ON `tabBehavioural Criteria`.`name`=`tabTeam Table`.`parent`
		where `tabBehavioural Criteria`.`docstatus`!=2 and `tabBehavioural Criteria`.`employee`='WTT1351' and `tabBehavioural Criteria`.`month`='February' union
		SELECT distinct(`tabSkill Table`.`criteria`)as "criteria","Skill" as "criteria_type",
		`tabBehavioural Criteria`.`employee`as "employee",`tabBehavioural Criteria`.`employee_name` as "employee_name",
		(SELECT cc.`hod_points` FROM `tabSkill Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabSkill Table`.`criteria` and pp.`month`='December' and pp.`employee`='WTT1351') as 'dec',
		(SELECT cc.`name` FROM `tabSkill Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabSkill Table`.`criteria` and pp.`month`='December' and pp.`employee`='WTT1351') as 'dec_ref',
		(SELECT cc.`management_points` FROM `tabSkill Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabSkill Table`.`criteria` and pp.`month`='January' and pp.`employee`='WTT1351') as 'jan',
		(SELECT cc.`name` FROM `tabSkill Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabSkill Table`.`criteria` and pp.`month`='January' and pp.`employee`='WTT1351') as 'jan_ref',
		(SELECT cc.`management_points` FROM `tabSkill Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabSkill Table`.`criteria` and pp.`month`='February' and pp.`employee`='WTT1351') as 'feb',
		(SELECT cc.`name` FROM `tabSkill Table`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabSkill Table`.`criteria` and pp.`month`='February' and pp.`employee`='WTT1351') as 'feb_ref'
		FROM `tabSkill Table` INNER JOIN `tabBehavioural Criteria` ON `tabBehavioural Criteria`.`name`=`tabSkill Table`.`parent`
		where `tabBehavioural Criteria`.`docstatus`!=2 and `tabBehavioural Criteria`.`employee`='WTT1351' and `tabBehavioural Criteria`.`month`='February' union
		SELECT distinct(`tabWork performance`.`criteria`)as "criteria","performance" as "criteria_type",
		`tabBehavioural Criteria`.`employee`as "employee",`tabBehavioural Criteria`.`employee_name` as "employee_name",
		(SELECT cc.`hod_points` FROM `tabWork performance`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabWork performance`.`criteria` and pp.`month`='December' and pp.`employee`='WTT1351') as 'dec',
		(SELECT cc.`name` FROM `tabWork performance`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabWork performance`.`criteria` and pp.`month`='December' and pp.`employee`='WTT1351') as 'dec_ref',
		(SELECT cc.`management_points` FROM `tabWork performance`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabWork performance`.`criteria` and pp.`month`='January' and pp.`employee`='WTT1351') as 'jan',
		(SELECT cc.`name` FROM `tabWork performance`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabWork performance`.`criteria` and pp.`month`='January' and pp.`employee`='WTT1351') as 'jan_ref',
		(SELECT cc.`management_points` FROM `tabWork performance`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabWork performance`.`criteria` and pp.`month`='February' and pp.`employee`='WTT1351') as 'feb',
		(SELECT cc.`name` FROM `tabWork performance`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabWork performance`.`criteria` and pp.`month`='February' and pp.`employee`='WTT1351') as 'feb_ref'
		FROM `tabWork performance` INNER JOIN `tabBehavioural Criteria` ON `tabBehavioural Criteria`.`name`=`tabWork performance`.`parent`
		where `tabBehavioural Criteria`.`docstatus`!=2 and `tabBehavioural Criteria`.`employee`='WTT1351' and `tabBehavioural Criteria`.`month`='February' union
		SELECT distinct(`tabWork knowledge`.`criteria`)as "criteria","knowledge" as "criteria_type",
		`tabBehavioural Criteria`.`employee`as "employee",`tabBehavioural Criteria`.`employee_name` as "employee_name",
		(SELECT cc.`hod_points` FROM `tabWork knowledge`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabWork knowledge`.`criteria` and pp.`month`='December' and pp.`employee`='WTT1351') as 'dec',
		(SELECT cc.`name` FROM `tabWork knowledge`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabWork knowledge`.`criteria` and pp.`month`='December' and pp.`employee`='WTT1351') as 'dec_ref',
		(SELECT cc.`management_points` FROM `tabWork knowledge`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabWork knowledge`.`criteria` and pp.`month`='January' and pp.`employee`='WTT1351') as 'jan',
		(SELECT cc.`name` FROM `tabWork knowledge`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabWork knowledge`.`criteria` and pp.`month`='January' and pp.`employee`='WTT1351') as 'jan_ref',
		(SELECT cc.`management_points` FROM `tabWork knowledge`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabWork knowledge`.`criteria` and pp.`month`='February' and pp.`employee`='WTT1351') as 'feb',
		(SELECT cc.`name` FROM `tabWork knowledge`as cc INNER JOIN `tabBehavioural Criteria`as pp ON pp.`name`=cc.`parent`
		where cc.`criteria`=`tabWork knowledge`.`criteria` and pp.`month`='February' and pp.`employee`='WTT1351') as 'feb_ref'
		FROM `tabWork knowledge` INNER JOIN `tabBehavioural Criteria` ON `tabBehavioural Criteria`.`name`=`tabWork knowledge`.`parent`
		where `tabBehavioural Criteria`.`docstatus`!=2 and `tabBehavioural Criteria`.`employee`='WTT1351' and `tabBehavioural Criteria`.`month`='February'""",as_dict=1)
	for i in aa:
		arr.append({
			'employee':i.employee,
			'employee_name':i.employee_name,
			'criteria_type':i.criteria_type,
			'criteria':i.criteria,
			'dec':i.dec,
			'dec_ref':i.dec_ref,
			'jan':i.jan,
			'jan_ref':i.jan_ref,
			'feb':i.feb,
			'feb_ref':i.feb_ref
			})



	return arr

@frappe.whitelist()
def update_marks(aa,bb,cc):
	tab=''
	if(cc=="Position"):
		frappe.db.sql("UPDATE `tabPosition Specific` set management_points='"+str(aa)+"' where name='"+str(bb)+"' ")
		tab='`tabPosition Specific`'
	elif(cc=="Industry"):
		frappe.db.sql("UPDATE `tabIndustry Specific` set management_points='"+str(aa)+"' where name='"+str(bb)+"' ")
		tab='`tabIndustry Specific`'
	elif(cc=="Common"):
		frappe.db.sql("UPDATE `tabCommon Skills` set management_points='"+str(aa)+"' where name='"+str(bb)+"' ")
		tab='`tabCommon Skills`'
	elif(cc=="Attitude"):
		frappe.db.sql("UPDATE `tabAttitude Table` set management_points='"+str(aa)+"' where name='"+str(bb)+"' ")
		tab='`tabAttitude Table`'
	elif(cc=="Personal"):
		frappe.db.sql("UPDATE `tabPersonal Table` set management_points='"+str(aa)+"' where name='"+str(bb)+"' ")
		tab='`tabPersonal Table`'
	elif(cc=="Team"):
		frappe.db.sql("UPDATE `tabTeam Table` set management_points='"+str(aa)+"' where name='"+str(bb)+"' ")
		tab='`tabTeam Table`'
	elif(cc=="Skill"):
		frappe.db.sql("UPDATE `tabSkill Table` set management_points='"+str(aa)+"' where name='"+str(bb)+"' ")
		tab='`tabSkill Table`'
	elif(cc=="performance"):
		frappe.db.sql("UPDATE `tabWork performance` set management_points='"+str(aa)+"' where name='"+str(bb)+"' ")
		tab='`tabWork performance`'
	elif(cc=="knowledge"):
		frappe.db.sql("UPDATE `tabWork knowledge` set management_points='"+str(aa)+"' where name='"+str(bb)+"' ")
		tab='`tabWork knowledge`'
	return frappe.db.sql("SELECT * from "+tab+" where name='"+str(bb)+"' ")

@frappe.whitelist()
def test_doc():
	frappe.msgprint("done")
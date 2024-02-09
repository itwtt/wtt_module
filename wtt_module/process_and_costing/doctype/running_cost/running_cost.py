# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from datetime import datetime
import traceback

class RunningCost(Document):
	def validate(self):
		pass
	# def validate(self):
	# 	try:
	# 		flow=frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"flow")
	# 		total_diffusers=frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"total_diffusers")
	# 		total_modules=frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"total_modules")
	# 		ovivo_no_module_required=frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"ovivo_no_module_required")
	# 		ovivo_no_of_stacks_required=frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"ovivo_no_of_stacks_required")
	# 		mbr_cts_no_module_required=frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"cts_ovivo_no_module_required")
	# 		mbr_cts_no_of_stacks_required=frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"cts_ovivo_no_of_stacks_required")
	# 		design_no_module_required=frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"design_no_module_required")
	# 		loop_operation=frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"loop_operation")
	# 		mbr_type=frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"mbr_type")
	# 		mbr_operate=frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"mbr_sludge_pump_operating_hours")
	# 		cts_capacity = frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"cts_capacity")
			
	# 		dgtro1=0
	# 		dgtro2=0
	# 		dgtro3=0
	# 		dgtro4=0
	# 		for i in frappe.db.sql("SELECT * FROM `tabRO Standard Items` WHERE name='"+str(self.ro_template)+"'",as_dict=1):
	# 			self.ro_degt_membrane1=i.ro_membrane_1
	# 			self.ro_degt_membrane2=i.ro_membrane_2
	# 			self.ro_degt_membrane3=i.ro_membrane_3
	# 			self.ro_degt_membrane4=i.ro_membrane_4
	# 			self.ro_degt_membrane5=i.ro_membrane_5
				
	# 			self.ro_membrane1=i.ro_membrane_1
	# 			self.ro_membrane2=i.ro_membrane_2
	# 			self.ro_membrane3=i.ro_membrane_3
	# 			self.ro_membrane4=i.ro_membrane_4
	# 			self.ro_membrane5=i.ro_membrane_5
				
	# 		for i in frappe.db.sql("SELECT * FROM `tabRO Standard Items` WHERE name='"+str(self.rro_template)+"'",as_dict=1):
	# 			self.rro_membrane=i.rro_membrane_1
	# 			self.rro_membrane1=i.rro_membrane_2
	# 			self.rro_membrane02=i.rro_membrane_3
			
	# 		if(self.ro_template is not None):
	# 			dgtro1=frappe.db.get_value('RO Items', {'parent': self.ro_template,'item_description':'MEMBRANE-1'}, "w_qty")
	# 			if(dgtro1 is None):
	# 				dgtro1=0
	# 			dgtro2=frappe.db.get_value('RO Items', {'parent': self.ro_template,'item_description':'MEMBRANE-2'}, "w_qty")
	# 			if(dgtro2 is None):
	# 				dgtro2=0
	# 			dgtro3=frappe.db.get_value('RO Items', {'parent': self.ro_template,'item_description':'MEMBRANE-3'}, "w_qty")
	# 			if(dgtro3 is None):
	# 				dgtro3=0
	# 			dgtro4=frappe.db.get_value('RO Items', {'parent': self.ro_template,'item_description':'MEMBRANE-4'}, "w_qty")
	# 			if(dgtro4 is None):
	# 				dgtro4=0
	# 			dgtro5=frappe.db.get_value('RO Items', {'parent': self.ro_template,'item_description':'MEMBRANE-5'}, "w_qty")
	# 			if(dgtro5 is None):
	# 				dgtro5=0
				
	# 		rro=0
	# 		rro1=0
	# 		rro2=0
	# 		if(self.rro_template is not None):
	# 			rro=frappe.db.get_value('RO Items', {'parent': self.rro_template,'item_description':'MEMBRANE-1'}, "w_qty")
	# 			if(rro is None):
	# 				rro=0
	# 			rro1=frappe.db.get_value('RO Items', {'parent': self.rro_template,'item_description':'MEMBRANE-2'}, "w_qty")
	# 			if(rro1 is None):
	# 				rro1=0
	# 			rro2=frappe.db.get_value('RO Items', {'parent': self.rro_template,'item_description':'MEMBRANE-3'}, "w_qty")
	# 			if(rro2 is None):
	# 				rro2=0
					
	# 		working_days=350
	# 		if(self.bio_membrane=="DIFFUSER MEMBRANE"):
	# 			self.bio_actual_qty=round(total_diffusers) if total_diffusers!=None else 0
	# 		if(self.mf_membrane=="MF MEMBRANE"):
	# 			self.mf_actual_qty=round(total_modules) if total_modules!=None else 0
	# 		if(self.ovivo_membrane=="MBR OVIVO"):
	# 			self.ovivo_actual_qty=round(ovivo_no_module_required) if ovivo_no_module_required!=None else 0
	# 			self.ovivo_no_of_stacks=round(ovivo_no_of_stacks_required) if ovivo_no_of_stacks_required!=None else 0
	# 		if(self.mbr_cts_membrane=="MBR OVIVO"):
	# 			self.mbr_cts_actual_qty=round(mbr_cts_no_module_required) if mbr_cts_no_module_required!=None else 0
	# 			self.mbr_cts_no_of_stacks=round(mbr_cts_no_of_stacks_required) if mbr_cts_no_of_stacks_required!=None else 0
	# 		if(self.koch_membrane in ["MBR MODULE - S - 36", "MBR MODULE - S - 40", "MBR MODULE - S - 44", "MBR MODULE - S - 16", "MBR MODULE - S - 8"]):
	# 			self.koch_actual_qty=round(design_no_module_required) if design_no_module_required!=None else 0
			
	# 		self.ro_actual_qty1 = dgtro1
	# 		self.ro_actual_qty2 = dgtro2
	# 		self.ro_actual_qty3 = dgtro3
	# 		self.ro_actual_qty_4 = dgtro4
	# 		self.ro_actual_qty_5 = dgtro5
			
	# 		self.actual_qty=rro
	# 		self.actual_qty1=rro1
	# 		self.rroactual_qty_2=rro2
			
	# 		mem=[self.mf_membrane, self.koch_membrane, self.ovivo_membrane+" MODULES", self.ovivo_membrane+" STACKS", self.mbr_cts_membrane+" MODULES", self.mbr_cts_membrane+" STACKS", self.bio_membrane]	
	# 		ssname=["MF","MBR(K)","MBR(O)","MBR(O)", "CTS MBR","CTS MBR","BIO"]
	# 		qty=[self.mf_actual_qty, self.koch_actual_qty, self.ovivo_actual_qty, self.ovivo_no_of_stacks, self.mbr_cts_actual_qty, self.mbr_cts_no_of_stacks, self.bio_actual_qty]
	# 		lt=[self.mf_life_time, self.koch_life_time, self.ovivo_life_time, self.ovivo_life_time, self.mbr_cts_life_time, self.mbr_cts_life_time, self.bio_life_time]
	# 		spare=[self.mf_spares, self.koch_spares, self.ovivo_spares, self.ovivo_spares, self.mbr_cts_spares, self.mbr_cts_spares, self.bio_spares]
			
	# 		if(self.ro_without_dgt == 0):
	# 			mem.extend([self.ro_membrane1, self.ro_membrane2, self.ro_membrane3, self.ro_membrane4,self.ro_membrane5])
	# 			ssname.extend(["RO-W","RO-W","RO-W","RO-W","RO-W"])
	# 			qty.extend([self.ro_actual_qty1, self.ro_actual_qty2, self.ro_actual_qty3, self.ro_actual_qty_4,self.ro_actual_qty_5])
	# 			lt.extend([self.ro_life_time1, self.ro_life_time2, self.ro_life_time3, self.ro_life_time4,self.ro_life_time5])
	# 			spare.extend([self.ro_spares1, self.ro_spares2, self.ro_spares3, self.ro_spares4,self.ro_spares5])
	# 		else:
	# 			mem.extend([self.ro_degt_membrane1, self.ro_degt_membrane2, self.ro_degt_membrane3, self.ro_degt_membrane4,self.ro_degt_membrane5])
	# 			ssname.extend(["RO-WO","RO-WO","RO-WO","RO-WO","RO-WO"])
	# 			qty.extend([self.ro_dgt_actual_qty1, self.ro_dgt_actual_qty2, self.ro_dgt_actual_qty3, self.ro_dgt_actual_qty4,self.ro_dgt_actual_qty5])
	# 			lt.extend([self.ro_dgt_life_time1, self.ro_dgt_life_time2, self.ro_dgt_life_time3, self.ro_dgt_life_time4,self.ro_dgt_life_time5])
	# 			spare.extend([self.ro_dgt_spares1, self.ro_dgt_spares2, self.ro_dgt_spares3, self.ro_dgt_spares4,self.ro_dgt_spares5])
			
	# 		mem.extend([self.rro_membrane,self.rro_membrane1,self.rro_membrane02])
	# 		ssname.extend(["RRO","RRO","RRO"])
	# 		qty.extend([self.actual_qty,self.actual_qty1,self.rroactual_qty_2])
	# 		lt.extend([self.life_time_years,self.life_time_years1,self.rrolife_time2])
	# 		spare.extend([self.rro_spares,self.rro_spares1,self.rrospares_2])
			
	# 		membrane=["DIFFUSER MEMBRANE", "UF  MEMBRANE-MAX80", "UF MEMBRANE-I", "UF MEMBRANE-D", "MF MEMBRANE", "SOFTNER RESIN", "BELT - 8","MBR OVIVO", "MBR OVIVO MODULES","MBR OVIVO STACKS", "MBR MODULE - S - 36", "MBR MODULE - S - 40", "MBR MODULE - S - 44", "MBR MODULE - S - 16", "MBR MODULE - S - 8", "MBR MODULE - S - 2", "MBR MODULE - H - 50", "MBR MODULE - H - 46", "MBR MODULE -H - 42", "MBR MODULE - H - 38", "NF MEMBRANE -D", "RO BW MEMBRANE -B", "RO BW MEMBRANE -BX", "RO BW MEMBRANE -4", "RO HP MEMBRANE", "RO HP MEMBRANE - 4", "RO BW MEMBRANE - F", "RO SW MEMBRANE - F7", "RO SW MEMBRANE - F8", "RO SW MEMBRANE - S", "RO SW MEMBRANE - 400", "RO SW MEMBRANE - 4", "RO BW MEMBRANE -EP2", "RO BW MEMBRANE - CP40", "RO BW MEMBRANE - CP80", "RO BW MEMBRANE - HL", "RO SW MEMBRANE - SW40", "RO SW MEMBRANE - SW80", "RO SW MEMBRANE - PL1", "RO SW MEMBRANE - XP1", "RO BW MEMBRANE -L4"]
	# 		cost=[962, 230580, 144936, 146400, 155672, 379, 3258376,280600, 210000,76000,5075200, 5368000, 5660800, 2976800, 1464000, 244000, 10337231, 9931849, 9339368, 8726099, 60122, 44798, 48312, 18788, 166408, 131760, 50530, 51386, 55339, 57438, 56120, 30598, 47024, 48312, 41663, 43310, 22814, 46885, 55734, 196981, 13272]
	# 		self.replacement_cost=[]
	# 		for i in range(len(mem)):
	# 			if(spare[i]==None):spare[i]=0
	# 			if(lt[i]==None):lt[i]=0
	# 			if(qty[i]==None):qty[i]=0
	# 			rate=0
	# 			for mc in range(len(membrane)):
	# 				if(mem[i]==membrane[mc]):
	# 					rate=cost[mc]
	# 			if(qty[i] is None):qty[i]=0
	# 			spare_qty=qty[i]*spare[i]/100
	# 			if(mem[i]):
	# 				self.append("replacement_cost",{
	# 					"membrane":mem[i],
	# 					"actual_qty":qty[i],
	# 					"spare_qty":spare_qty,
	# 					"qty":qty[i]+spare_qty,
	# 					"system":ssname[i],
	# 					"rate":rate,
	# 					"amount":rate*(qty[i]+spare_qty),
	# 					"flow":flow,
	# 					"flow_100":(rate*(qty[i]+spare_qty))/(working_days*(flow)*lt[i]),
	# 					"flow_90":(rate*(qty[i]+spare_qty))/(working_days*(flow*0.9)*lt[i]),
	# 					"flow_80":(rate*(qty[i]+spare_qty))/(working_days*(flow*0.8)*lt[i]),
	# 					"flow_70":(rate*(qty[i]+spare_qty))/(working_days*(flow*0.7)*lt[i]),
	# 					"flow_60":(rate*(qty[i]+spare_qty))/(working_days*(flow*0.6)*lt[i]),
	# 					"flow_50":(rate*(qty[i]+spare_qty))/(working_days*(flow*0.5)*lt[i])
	# 				})
	# 		ro_flow_100=0
	# 		ro_flow_90=0
	# 		ro_flow_80=0
	# 		ro_flow_70=0
	# 		ro_flow_60=0
	# 		ro_flow_50=0
			
	# 		rro_flow_100=0
	# 		rro_flow_90=0
	# 		rro_flow_80=0
	# 		rro_flow_70=0
	# 		rro_flow_60=0
	# 		rro_flow_50=0
			
	# 		sys=''
	# 		svs=''
	# 		for i in self.replacement_cost:
	# 			if(i.system == 'RO-W'):
	# 				sys='RO-W'
	# 				ro_flow_100=ro_flow_100+float(i.flow_100)
	# 				ro_flow_90=ro_flow_90+float(i.flow_90)
	# 				ro_flow_80=ro_flow_80+float(i.flow_80)
	# 				ro_flow_70=ro_flow_70+float(i.flow_70)
	# 				ro_flow_60=ro_flow_60+float(i.flow_60)
	# 				ro_flow_50=ro_flow_50+float(i.flow_50)
	# 			elif(i.system == 'RO-WO'):
	# 				sys='RO-WO'
	# 				ro_flow_100=ro_flow_100+float(i.flow_100)
	# 				ro_flow_90=ro_flow_90+float(i.flow_90)
	# 				ro_flow_80=ro_flow_80+float(i.flow_80)
	# 				ro_flow_70=ro_flow_70+float(i.flow_70)
	# 				ro_flow_60=ro_flow_60+float(i.flow_60)
	# 				ro_flow_50=ro_flow_50+float(i.flow_50)
					
	# 		for i in self.replacement_cost:
	# 			if(i.system == 'RRO'):
	# 				svs='RRO'
	# 				rro_flow_100=rro_flow_100+float(i.flow_100)
	# 				rro_flow_90=rro_flow_90+float(i.flow_90)
	# 				rro_flow_80=rro_flow_80+float(i.flow_80)
	# 				rro_flow_70=rro_flow_70+float(i.flow_70)
	# 				rro_flow_60=rro_flow_60+float(i.flow_60) 
	# 				rro_flow_50=rro_flow_50+float(i.flow_50)
			
	# 		self.reference_replacment_cost=[]
	# 		ar1,ar2,ar3,ar4,ar5,ar6=[],[],[],[],[],[]
	# 		br1,br2,br3,br4,br5,br6=[],[],[],[],[],[]
	# 		sys_list=[]
	# 		for i in self.replacement_cost:
	# 			if(i.system=="MBR(O)"):
	# 				ar1.append(i.flow_100)
	# 				ar2.append(i.flow_90)
	# 				ar3.append(i.flow_80)
	# 				ar4.append(i.flow_70)
	# 				ar5.append(i.flow_60)
	# 				ar6.append(i.flow_50)
	# 			elif(i.system=="CTS MBR"):
	# 				br1.append(i.flow_100)
	# 				br2.append(i.flow_90)
	# 				br3.append(i.flow_80)
	# 				br4.append(i.flow_70)
	# 				br5.append(i.flow_60)
	# 				br6.append(i.flow_50)
	# 		for i in self.replacement_cost:
	# 			if(i.system not in sys_list):
	# 				sys_list.append(i.system)
	# 				if(i.system == "MF" or i.system == 'MBR(K)' or i.system == "BIO"):
	# 					self.append("reference_replacment_cost",{
	# 						"system":i.system,
	# 						"flow_100":i.flow_100,
	# 						"flow_90":i.flow_90,
	# 						"flow_80":i.flow_80,
	# 						"flow_70":i.flow_70,
	# 						"flow_60":i.flow_60,
	# 						"flow_50":i.flow_50
	# 					});
	# 				elif(i.system == "MBR(O)"):
	# 					self.append("reference_replacment_cost",{
	# 						"system":i.system,
	# 						"flow_100":sum(ar1),
	# 						"flow_90":sum(ar2),
	# 						"flow_80":sum(ar3),
	# 						"flow_70":sum(ar4),
	# 						"flow_60":sum(ar5),
	# 						"flow_50":sum(ar6)
	# 					});
	# 				elif(i.system == "CTS MBR"):
	# 					self.append("reference_replacment_cost",{
	# 						"system":i.system,
	# 						"flow_100":sum(br1),
	# 						"flow_90":sum(br2),
	# 						"flow_80":sum(br3),
	# 						"flow_70":sum(br4),
	# 						"flow_60":sum(br5),
	# 						"flow_50":sum(br6)
	# 					});
	# 		self.append("reference_replacment_cost",{
	# 				"system":sys,
	# 				"flow_100":ro_flow_100,
	# 				"flow_90":ro_flow_90,
	# 				"flow_80":ro_flow_80,
	# 				"flow_70":ro_flow_70,
	# 				"flow_60":ro_flow_60,
	# 				"flow_50":ro_flow_50
	# 			});
				
	# 		self.append("reference_replacment_cost",{
	# 				"system":svs,
	# 				"flow_100":rro_flow_100,
	# 				"flow_90":rro_flow_90,
	# 				"flow_80":rro_flow_80,
	# 				"flow_70":rro_flow_70,
	# 				"flow_60":rro_flow_60,
	# 				"flow_50":rro_flow_50
	# 			});
			
	# 		total_100=0
	# 		total_90=0
	# 		total_80=0
	# 		total_70=0
	# 		total_60=0
	# 		total_50=0
			
	# 		for i in self.reference_replacment_cost:
	# 			if(i.system == 'MF'):
	# 				if(self.mf_select == 1):
	# 					total_100 = total_100+i.flow_100
	# 					total_90 = total_90+i.flow_90
	# 					total_80 = total_80+i.flow_80
	# 					total_70 = total_70+i.flow_70
	# 					total_60 = total_60+i.flow_60
	# 					total_50 = total_50+i.flow_50
	# 			elif(i.system == 'MBR(K)'):
	# 				if(self.mbrk_select == 1):
	# 					total_100 = total_100+i.flow_100
	# 					total_90 = total_90+i.flow_90
	# 					total_80 = total_80+i.flow_80
	# 					total_70 = total_70+i.flow_70
	# 					total_60 = total_60+i.flow_60
	# 					total_50 = total_50+i.flow_50
	# 			elif(i.system == 'MBR(O)'):
	# 				if(self.mbrk_select == 1):
	# 					total_100 = total_100+i.flow_100
	# 					total_90 = total_90+i.flow_90
	# 					total_80 = total_80+i.flow_80
	# 					total_70 = total_70+i.flow_70
	# 					total_60 = total_60+i.flow_60
	# 					total_50 = total_50+i.flow_50
	# 			elif(i.system == 'CTS MBR'):
	# 				if(self.cts_mbr_select == 1):
	# 					total_100 = total_100+i.flow_100
	# 					total_90 = total_90+i.flow_90
	# 					total_80 = total_80+i.flow_80
	# 					total_70 = total_70+i.flow_70
	# 					total_60 = total_60+i.flow_60
	# 					total_50 = total_50+i.flow_50
	# 			elif(i.system == 'BIO'):
	# 				if(self.bio_select == 1):
	# 					total_100 = total_100+i.flow_100
	# 					total_90 = total_90+i.flow_90
	# 					total_80 = total_80+i.flow_80
	# 					total_70 = total_70+i.flow_70
	# 					total_60 = total_60+i.flow_60
	# 					total_50 = total_50+i.flow_50
	# 			elif(i.system == 'RO-WO' or i.system == 'RO-W'):
	# 				if(self.ro_select == 1):
	# 					total_100 = total_100+i.flow_100
	# 					total_90 = total_90+i.flow_90
	# 					total_80 = total_80+i.flow_80
	# 					total_70 = total_70+i.flow_70
	# 					total_60 = total_60+i.flow_60
	# 					total_50 = total_50+i.flow_50
	# 			elif(i.system == 'RRO'):
	# 				if(self.rro_select == 1):
	# 					total_100 = total_100+i.flow_100
	# 					total_90 = total_90+i.flow_90
	# 					total_80 = total_80+i.flow_80
	# 					total_70 = total_70+i.flow_70
	# 					total_60 = total_60+i.flow_60
	# 					total_50 = total_50+i.flow_50
						
	# 		self.total_cost_for_100_flow = total_100
	# 		self.total_cost_for_90_flow = total_90
	# 		self.total_cost_for_80_flow = total_80
	# 		self.total_cost_for_70_flow = total_70
	# 		self.total_cost_for_60_flow = total_60
	# 		self.total_cost_for_50_flow = total_50
			
	# 		#Energy cost
	# 		if(self.edit_energy == 1):
	# 			for i in self.mf:
	# 				i.kw_per_day= i.absorbed_power/i.running_hours
	# 				i.cost_per_day = (i.absorbed_power/i.running_hours)*self.electricity_cost_per_unit
	# 				i.kw_m3 = (i.absorbed_power/i.running_hours)/flow
	# 				i.kw_m3_90 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_80 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_70 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_60 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_50 = i.absorbed_power*i.running_hours
				
	# 			for i in self.mbr:
	# 				i.kw_per_day= i.absorbed_power/i.running_hours
	# 				i.cost_per_day = (i.absorbed_power/i.running_hours)*self.electricity_cost_per_unit
	# 				i.kw_m3 = (i.absorbed_power/i.running_hours)/flow
	# 				i.kw_m3_90 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_80 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_70 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_60 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_50 = i.absorbed_power*i.running_hours
				
	# 			for i in self.mbr_ovivo:
	# 				i.kw_per_day= i.absorbed_power/i.running_hours
	# 				i.cost_per_day = (i.absorbed_power/i.running_hours)*self.electricity_cost_per_unit
	# 				i.kw_m3 = (i.absorbed_power/i.running_hours)/flow
	# 				i.kw_m3_90 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_80 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_70 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_60 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_50 = i.absorbed_power*i.running_hours
				
	# 			for i in self.biot:
	# 				i.kw_per_day= i.absorbed_power/i.running_hours
	# 				i.cost_per_day = (i.absorbed_power/i.running_hours)*self.electricity_cost_per_unit
	# 				i.kw_m3 = (i.absorbed_power/i.running_hours)/flow
	# 				i.kw_m3_90 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_80 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_70 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_60 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_50 = i.absorbed_power*i.running_hours
					
	# 			for i in self.dgt:
	# 				i.kw_per_day= i.absorbed_power/i.running_hours
	# 				i.cost_per_day = (i.absorbed_power/i.running_hours)*self.electricity_cost_per_unit
	# 				i.kw_m3 = (i.absorbed_power/i.running_hours)/flow
	# 				i.kw_m3_90 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_80 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_70 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_60 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_50 = i.absorbed_power*i.running_hours
				
	# 			for i in self.ro:
	# 				i.kw_per_day= i.absorbed_power/i.running_hours
	# 				i.cost_per_day = (i.absorbed_power/i.running_hours)*self.electricity_cost_per_unit
	# 				i.kw_m3 = (i.absorbed_power/i.running_hours)/flow
	# 				i.kw_m3_90 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_80 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_70 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_60 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_50 = i.absorbed_power*i.running_hours
					
	# 			for i in self.cts:
	# 				i.kw_per_day= i.absorbed_power/i.running_hours
	# 				i.cost_per_day = (i.absorbed_power/i.running_hours)*self.electricity_cost_per_unit
	# 				i.kw_m3 = (i.absorbed_power/i.running_hours)/flow
	# 				i.kw_m3_90 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_80 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_70 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_60 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_50 = i.absorbed_power*i.running_hours
					
	# 			for i in self.sbrs:
	# 				i.kw_per_day= i.absorbed_power/i.running_hours
	# 				i.cost_per_day = (i.absorbed_power/i.running_hours)*self.electricity_cost_per_unit
	# 				i.kw_m3 = (i.absorbed_power/i.running_hours)/flow
	# 				i.kw_m3_90 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_80 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_70 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_60 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_50 = i.absorbed_power*i.running_hours
					
	# 			for i in self.rro:
	# 				i.kw_per_day= i.absorbed_power/i.running_hours
	# 				i.cost_per_day = (i.absorbed_power/i.running_hours)*self.electricity_cost_per_unit
	# 				i.kw_m3 = (i.absorbed_power/i.running_hours)/flow
	# 				i.kw_m3_90 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_80 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_70 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_60 = i.absorbed_power*i.running_hours
	# 				i.kw_m3_50 = i.absorbed_power*i.running_hours
				
	# 		else:
	# 			selected_s=[]
	# 			for v in frappe.db.sql("SELECT selected_system_name FROM `tabSelected Process System` where parent='"+str(self.startup_sheet)+"'",as_dict=1):
	# 				selected_s.append(v.selected_system_name)
	# 			ss = frappe.get_doc("Cost Working Tool",self.cost_working_tool)
	# 			self.mf=[]
	# 			self.mbr=[]
	# 			self.mbr_ovivo=[]
	# 			self.biot=[]
	# 			self.cts=[]
	# 			self.dgt=[]
	# 			if("Micro Filtration - ASAHI" in selected_s):
	# 				for ii in ss.mf_electrical_items:
	# 					if(ii.item_description not in ["PLC","PANEL"]):
	# 						rcost=20
	# 						if(ii.item_description == 'PRE-FILTER'):
	# 							rcost=22
	# 						elif(ii.item_description == 'FEED PUMP'):
	# 							rcost=22
	# 						elif(ii.item_description == 'BACKWASH PUMP'):
	# 							if(loop_operation == 'Single'):
	# 								rcost=24
	# 							else:
	# 								rcost=3
	# 						elif(ii.item_description == 'CIP PUMP'):
	# 							rcost=0.5
	# 						elif(ii.item_description == 'SULPHUR BLACK SLUDGE PUMP'):
	# 							rcost=20
	# 						elif(ii.item_description == 'CIP DOSING PUMP-1'):
	# 							rcost=0.25
	# 						elif(ii.item_description == 'CIP DOSING PUMP-2'):
	# 							rcost=0.25
	# 						elif(ii.item_description == 'CIP DOSING PUMP-3'):
	# 							rcost=0.25
	# 						elif(ii.item_description == 'SULPHUR BLACK DOSING PUMP'):
	# 							rcost=22
	# 						else:
	# 							rcost=20
								
	# 						ins_pwr=float(ii.kw)*float(ii.w_qty+ii.sb_qty)
	# 						abs_pwr=float(ii.kw)*float(ii.w_qty)
	# 						self.append("mf",{
	# 							"item_description":ii.item_description,
	# 							"w_qty":ii.w_qty,
	# 							"sb_qty":ii.sb_qty,
	# 							"kw":ii.kw,
	# 							"running_hours":rcost,
	# 							"installed_hours":ins_pwr,
	# 							"absorbed_power":abs_pwr,
	# 							"kw_per_day":abs_pwr*rcost,
	# 							"cost_per_day":(abs_pwr*rcost)*self.electricity_cost_per_unit,
	# 							"kw_m3":(abs_pwr*rcost)/flow,
	# 							"kw_m3_90":(abs_pwr*rcost)/(flow*0.9),
	# 							"kw_m3_80":(abs_pwr*rcost)/(flow*0.8),
	# 							"kw_m3_70":(abs_pwr*rcost)/(flow*0.7),
	# 							"kw_m3_60":(abs_pwr*rcost)/(flow*0.6),
	# 							"kw_m3_50":(abs_pwr*rcost)/(flow*0.5)
	# 						})
				
	# 			if("Submerged MBR system - KOCH" in selected_s):
	# 				for ii in ss.mbr_electrical_items:
	# 					if(ii.item_description not in ["PLC","PANEL"]):
	# 						rhours=20
	# 						if(ii.item_description == 'PERMEATE/BACKWASH/CIP PUMP'):
	# 							rhours=24
	# 						elif(ii.item_description == 'MBR BLOWER'):
	# 							if(mbr_type == 'SUB-UF'):
	# 								rhours=4
	# 							else:
	# 								rhours=22
	# 						elif(ii.item_description == 'SLUDGE EXTRACT PUMP'):
	# 							rhours=4
	# 						elif(ii.item_description == 'SULPHUR BLACK SLUDGE PUMP'):
	# 							rhours=mbr_operate
	# 						elif(ii.item_description == 'SULPHUR BLACK DOSING PUMP'):
	# 							rhours=frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"mbr_lamella_operating_hours")
	# 						elif(ii.item_description == 'CIP DOSING PUMP-1'):
	# 							rhours=0.1
	# 						elif(ii.item_description == 'CIP DOSING PUMP-2'):
	# 							rhours=0.1
	# 						elif(ii.item_description == 'CIP DOSING PUMP-3'):
	# 							rhours=0.1
	# 						else:
	# 							rhours=20
	# 						ins_pwr=float(ii.kw)*float(ii.w_qty+ii.sb_qty)
	# 						abs_pwr=float(ii.kw)*float(ii.w_qty)
	# 						self.append("mbr",{
	# 							"item_description":ii.item_description,
	# 							"w_qty":ii.w_qty,
	# 							"sb_qty":ii.sb_qty,
	# 							"kw":ii.kw,
	# 							"running_hours":rhours,
	# 							"installed_hours":ins_pwr,
	# 							"absorbed_power":abs_pwr,
	# 							"kw_per_day":abs_pwr*rhours,
	# 							"cost_per_day":(abs_pwr*rhours)*self.electricity_cost_per_unit,
	# 							"kw_m3":(abs_pwr*rhours)/flow,
	# 							"kw_m3_90":(abs_pwr*rhours)/(flow*0.9),
	# 							"kw_m3_80":(abs_pwr*rhours)/(flow*0.8),
	# 							"kw_m3_70":(abs_pwr*rhours)/(flow*0.7),
	# 							"kw_m3_60":(abs_pwr*rhours)/(flow*0.6),
	# 							"kw_m3_50":(abs_pwr*rhours)/(flow*0.5)
	# 						})
				
	# 			if("Submerged MBR system - OVIVO" in selected_s):
	# 				for ii in ss.ovivo_electrical_items:
	# 					if(ii.item_description not in ["PLC","PANEL"]):
	# 						rhours=20
	# 						if(ii.item_description == 'PERMEATE PUMP'):
	# 							rhours=22
	# 						elif(ii.item_description == 'BACKWASH/CIP PUMP'):
	# 							rhours=2
	# 						elif(ii.item_description == 'MBR BLOWER'):
	# 							rhours=2
	# 						elif(ii.item_description == 'SLUDGE EXTRACT PUMP'):
	# 							rhours=20
	# 						elif(ii.item_description == 'SULPHUR BLACK SLUDGE PUMP'):
	# 							rhours=frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"mbro_sludge_pump_operating_hours")
	# 						elif(ii.item_description == 'SULPHUR BLACK DOSING PUMP'):
	# 							rhours=frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"mbro_lamella_operating_hours")
	# 						elif(ii.item_description == 'SPRINKLER PUMP'):
	# 							rhours=2
	# 						elif(ii.item_description == 'CIP DOSING PUMP-1'):
	# 							rhours=0.1
	# 						elif(ii.item_description == 'CIP DOSING PUMP-2'):
	# 							rhours=0.1
	# 						elif(ii.item_description == 'CIP DOSING PUMP-3'):
	# 							rhours=0.1
	# 						else:
	# 							rhours=20
								
	# 						ins_pwr=float(ii.kw)*float(ii.w_qty+ii.sb_qty)
	# 						abs_pwr=float(ii.kw)*float(ii.w_qty)
	# 						self.append("mbr_ovivo",{
	# 							"item_description":ii.item_description,
	# 							"w_qty":ii.w_qty,
	# 							"sb_qty":ii.sb_qty,
	# 							"kw":ii.kw,
	# 							"running_hours":rhours,
	# 							"installed_hours":ins_pwr,
	# 							"absorbed_power":abs_pwr,
	# 							"kw_per_day":abs_pwr*rhours,
	# 							"cost_per_day":(abs_pwr*rhours)*self.electricity_cost_per_unit,
	# 							"kw_m3":(abs_pwr*rhours)/flow,
	# 							"kw_m3_90":(abs_pwr*rhours)/(flow*0.9),
	# 							"kw_m3_80":(abs_pwr*rhours)/(flow*0.8),
	# 							"kw_m3_70":(abs_pwr*rhours)/(flow*0.7),
	# 							"kw_m3_60":(abs_pwr*rhours)/(flow*0.6),
	# 							"kw_m3_50":(abs_pwr*rhours)/(flow*0.5)
	# 						})
				
	# 			if("Biological Oxidation System" in selected_s):
	# 				for ii in ss.bio_electrical_items:
	# 					if(ii.item_description not in ["PLC","PANEL"]):
	# 						rhours=20
	# 						if(ii.item_description == 'ROTARY BRUSH SCREENER'):
	# 							rhours=22
	# 						elif(ii.item_description == 'DRUM SCREENER'):
	# 							rhours=24
	# 						elif(ii.item_description == 'LIFTING SUMP PUMP'):
	# 							rhours=24
	# 						elif(ii.item_description == 'DAF SCRAPPER'):
	# 							rhours=24
	# 						elif(ii.item_description == 'DAF SLUDGE PUMP'):
	# 							rhours=20
	# 						elif(ii.item_description == 'DAF BUBBLE GENERATION PUMP'):
	# 							rhours=24
	# 						elif(ii.item_description == 'EQT BLOWER'):
	# 							rhours=24
	# 						elif(ii.item_description == 'NT PUMP'):
	# 							rhours=24
	# 						elif(ii.item_description == 'NT DOSING PUMP'):
	# 							rhours=24
	# 						elif(ii.item_description == 'COOLING TOWER'):
	# 							rhours=24
	# 						elif(ii.item_description == 'DNT PUMP'):
	# 							rhours=24
	# 						elif(ii.item_description == 'DNT FLOW MIXER'):
	# 							rhours=24
	# 						elif(ii.item_description == 'BIO BLOWER'):
	# 							rhours=24
	# 						elif(ii.item_description == 'CIRCULAR CLARIFIER SYSTEM'):
	# 							rhours=24
	# 						elif(ii.item_description == 'SRS PUMP'):
	# 							rhours=24
	# 						elif(ii.item_description == 'SLUDGE THICKENER WITH MECH'):
	# 							rhours=20
	# 						elif(ii.item_description == 'BELT PRESS'):
	# 							rhours=20
	# 						elif(ii.item_description == 'BELT POLY UNIT MODEL'):
	# 							rhours=20
	# 						elif(ii.item_description == 'BELT FEED PUMP'):
	# 							rhours=20
	# 						elif(ii.item_description == 'BELT WASHING PUMP'):
	# 							rhours=16
	# 						elif(ii.item_description == 'BELT PRESS AGITATOR'):
	# 							rhours=20
	# 						elif(ii.item_description == 'SCREW PRESS'):
	# 							rhours=20
	# 						elif(ii.item_description == 'SCREW POLY UNIT MODEL'):
	# 							rhours=20
	# 						elif(ii.item_description == 'SCREW FEED PUMP'):
	# 							rhours=20
	# 						elif(ii.item_description == 'SCREW PRESS AGITATOR'):
	# 							rhours=20
	# 						else:
	# 							rhours=20
								
	# 						ins_pwr=float(ii.kw)*float(ii.w_qty+ii.sb_qty)
	# 						abs_pwr=float(ii.kw)*float(ii.w_qty)
	# 						self.append("biot",{
	# 							"item_description":ii.item_description,
	# 							"w_qty":ii.w_qty,
	# 							"sb_qty":ii.sb_qty,
	# 							"kw":ii.kw,
	# 							"running_hours":rhours,
	# 							"installed_hours":ins_pwr,
	# 							"absorbed_power":abs_pwr,
	# 							"kw_per_day":abs_pwr*rhours,
	# 							"cost_per_day":(abs_pwr*rhours)*self.electricity_cost_per_unit,
	# 							"kw_m3":(abs_pwr*rhours)/flow,
	# 							"kw_m3_90":(abs_pwr*rhours)/(flow*0.9),
	# 							"kw_m3_80":(abs_pwr*rhours)/(flow*0.8),
	# 							"kw_m3_70":(abs_pwr*rhours)/(flow*0.7),
	# 							"kw_m3_60":(abs_pwr*rhours)/(flow*0.6),
	# 							"kw_m3_50":(abs_pwr*rhours)/(flow*0.5)
	# 						})
	# 			if("Hardness and Color Removal System" in selected_s):
	# 				for ii in ss.cts_electrical_items:
	# 					if(ii.item_description not in ["PLC","PANEL"]):
	# 						rhours=21
	# 						if(ii.item_description == 'FEED PUMP'):
	# 							rhours=21
	# 						elif(ii.item_description == 'SLUDGE PUMP'):
	# 							rhours=21
	# 						elif(ii.item_description == 'DOSING PUMP-1'):
	# 							rhours=21
	# 						elif(ii.item_description == 'DOSING PUMP-2'):
	# 							rhours=21
	# 						elif(ii.item_description == 'DOSING PUMP-3'):
	# 							rhours=21
	# 						elif(ii.item_description == 'DOSING PUMP-4'):
	# 							rhours=21
	# 						elif(ii.item_description == 'DOSING PUMP-5'):
	# 							rhours=21
	# 						elif(ii.item_description == 'AGITATOR'):
	# 							rhours=21
	# 						else:
	# 							rhours=21
	# 						ins_pwr=float(ii.kw)*float(ii.w_qty+ii.sb_qty)
	# 						abs_pwr=float(ii.kw)*float(ii.w_qty)
	# 						self.append("cts",{
	# 							"item_description":ii.item_description,
	# 							"w_qty":ii.w_qty,
	# 							"sb_qty":ii.sb_qty,
	# 							"kw":ii.kw,
	# 							"running_hours":rhours,
	# 							"installed_hours":ins_pwr,
	# 							"absorbed_power":abs_pwr,
	# 							"kw_per_day":abs_pwr*rhours,
	# 							"cost_per_day":(abs_pwr*rhours)*self.electricity_cost_per_unit,
	# 							"kw_m3":(abs_pwr*rhours)/flow,
	# 							"kw_m3_90":(abs_pwr*rhours)/(flow*0.9),
	# 							"kw_m3_80":(abs_pwr*rhours)/(flow*0.8),
	# 							"kw_m3_70":(abs_pwr*rhours)/(flow*0.7),
	# 							"kw_m3_60":(abs_pwr*rhours)/(flow*0.6),
	# 							"kw_m3_50":(abs_pwr*rhours)/(flow*0.5)
	# 						})
	# 			if("Degasser System" in selected_s):
	# 				for ii in ss.dgt_electrical_items:
	# 					if(ii.item_description not in ["PLC","PANEL"]):
	# 						ins_pwr=float(ii.kw)*float(ii.w_qty+ii.sb_qty)
	# 						abs_pwr=float(ii.kw)*float(ii.w_qty)
	# 						self.append("dgt",{
	# 							"item_description":ii.item_description,
	# 							"w_qty":ii.w_qty,
	# 							"sb_qty":ii.sb_qty,
	# 							"kw":ii.kw,
	# 							"running_hours":22,
	# 							"installed_hours":ins_pwr,
	# 							"absorbed_power":abs_pwr,
	# 							"kw_per_day":abs_pwr*22,
	# 							"cost_per_day":(abs_pwr*22)*self.electricity_cost_per_unit,
	# 							"kw_m3":(abs_pwr*22)/flow,
	# 							"kw_m3_90":(abs_pwr*22)/(flow*0.9),
	# 							"kw_m3_80":(abs_pwr*22)/(flow*0.8),
	# 							"kw_m3_70":(abs_pwr*22)/(flow*0.7),
	# 							"kw_m3_60":(abs_pwr*22)/(flow*0.6),
	# 							"kw_m3_50":(abs_pwr*22)/(flow*0.5)
	# 						})
	# 			if("Reverse Osmosis" in selected_s):
	# 				self.ro=[]
	# 				ro=frappe.get_doc("RO Standard Items",str(self.ro_template))
	# 				for ii in ro.ro_electrical_items:
	# 					if(ii.item_description not in ["PLC","PANEL"]):
	# 						rhours = frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"ro_operating_hours")
	# 						if(ii.item_description == 'CIP PUMP-1'):
	# 							rhours=0.25
	# 						elif(ii.item_description == 'CIP PUMP-2'):
	# 							rhours=0.25
	# 						elif(ii.item_description == 'CAUSTIC DOSING'):
	# 							rhours=0.1
	# 						else:
	# 							rhours = frappe.db.get_value("Startup Sheet",str(self.startup_sheet),"ro_operating_hours")
	# 						if(ii.kw==None or ii.kw==''):ii.kw=0
	# 						ins_pwr=float(ii.kw)*float(ii.w_qty+ii.sb_qty)
	# 						abs_pwr=float(ii.kw)*float(ii.w_qty)
	# 						self.append("ro",{
	# 							"item_description":ii.item_description,
	# 							"w_qty":ii.w_qty,
	# 							"sb_qty":ii.sb_qty,
	# 							"kw":ii.kw,
	# 							"running_hours":rhours,
	# 							"installed_hours":ins_pwr,
	# 							"absorbed_power":abs_pwr,
	# 							"kw_per_day":abs_pwr*rhours,
	# 							"cost_per_day":(abs_pwr*rhours)*self.electricity_cost_per_unit,
	# 							"kw_m3":(abs_pwr*rhours)/flow,
	# 							"kw_m3_90":(abs_pwr*rhours)/(flow*0.9),
	# 							"kw_m3_80":(abs_pwr*rhours)/(flow*0.8),
	# 							"kw_m3_70":(abs_pwr*rhours)/(flow*0.7),
	# 							"kw_m3_60":(abs_pwr*rhours)/(flow*0.6),
	# 							"kw_m3_50":(abs_pwr*rhours)/(flow*0.5)
	# 						})							
	# 		#chemical_cost
	# 		self.mbr_cip=self.flow*(0.7/100)
	# 		self.mbr_ovivo_cip_tank = self.ovivo_actual_qty * 116/1000
	# 		self.cts_mbr_cip_tank = self.mbr_cts_actual_qty * 116/1000
	# 		for i in self.cleaning_chemical:
	# 			if(i.system == 'MF'):
	# 				i.consumption = i.concentration * self.mf_cip_tank / 1000
	# 			elif(i.system == 'MBR (KOCH)'):
	# 				i.consumption = i.concentration * self.mbr_cip / 1000
	# 			elif(i.system == 'RO'):
	# 				if(i.chemical_name == 'HCl - 33%' or i.chemical_name == 'Citric acid - CG' or i.chemical_name=='OSMOCHEM - 7525'):
	# 					i.consumption = i.concentration * (self.ro_1_cip_tank_1 + self.ro_1_cip_tank_2) / 1000
	# 				else:
	# 					i.consumption = i.concentration * self.ro_1_cip_tank_1 / 1000
	# 			elif(i.system == 'RO WO DGT'):
	# 				if(i.chemical_name == 'HCl - 33%' or i.chemical_name == 'Citric acid - CG' or i.chemical_name=='OSMOCHEM - 7525'):
	# 					i.consumption = i.concentration * (self.ro_1_cip_tank_1 + self.ro_1_cip_tank_2) / 1000
	# 				else:
	# 					i.consumption = i.concentration * self.ro_1_cip_tank_1 / 1000
	# 			elif(i.system == 'R. MF'):
	# 				i.consumption = i.concentration * self.ruf_cip_tank / 1000
	# 			elif(i.system == 'R.RO'):
	# 				i.consumption = i.concentration * self.ro_2_cip_tank_1 / 1000
				
	# 			for j in frappe.db.sql("SELECT rate FROM `tabState rate chemical` WHERE system='"+str(i.chemical_name)+"' and state='"+str(self.state)+"'",as_dict=1):
	# 				i.unit_cost=j.rate * (1+(self.transport_per/100))
	# 			i.consumption = 0 if i.consumption==None else i.consumption
	# 			i.cleaning_frequencyday = 0 if i.cleaning_frequencyday==None else i.cleaning_frequencyday
	# 			i.total_cost = i.consumption * i.unit_cost
	# 			i.cost_day = i.total_cost/i.cleaning_frequencyday if i.cleaning_frequencyday>0 else 0
	# 			i.consumption_day=i.cost_day/i.unit_cost if i.unit_cost>0 else 0
	# 			i.cost_m3=i.cost_day/self.flow
	# 		mfcost=0
	# 		mbrcost=0
	# 		ovivocost=0
	# 		ctsmbrcost=0
	# 		rocost=0
	# 		rowocost=0
	# 		rmfcost=0
	# 		rrocost=0
	# 		total_m3=0
	# 		for i in self.cleaning_chemical:
	# 			if(i.system == 'MF'):
	# 				mfcost=mfcost+i.cost_m3
	# 			elif(i.system == 'MBR (KOCH)'):
	# 				mbrcost=mbrcost+i.cost_m3
	# 			elif(i.system == 'RO'):
	# 				rocost=rocost+i.cost_m3
	# 			elif(i.system == 'RO WO DGT'):
	# 				rowocost=rowocost+i.cost_m3
	# 			elif(i.system == 'R. MF'):
	# 				rmfcost=rmfcost+i.cost_m3
	# 			elif(i.system == 'R.RO'):
	# 				rrocost=rrocost+i.cost_m3
	# 			elif(i.system == 'MBR (OVIVO)'):
	# 				ovivocost=ovivocost+i.cost_m3
	# 			elif(i.system == 'CTS MBR'):
	# 				ctsmbrcost=ctsmbrcost+i.cost_m3
	# 			total_m3=total_m3+i.cost_m3
	# 		self.total_mbr_ovivo = ovivocost
	# 		self.total_cts_mbr = ctsmbrcost
	# 		self.total_cost_m3=total_m3
	# 		self.total_mf=mfcost
	# 		self.total_mbr=mbrcost
	# 		self.total_ro_wo_dgt=rowocost
	# 		self.total_ro=rocost
	# 		self.total_r_mf=rmfcost
	# 		self.total_r_ro=rrocost
			
	# 		conro=0
	# 		conrwo=0
	# 		conrro=0
	# 		if(self.consumables):
	# 			for i in self.consumables:
	# 				ro_recovery=frappe.db.get_value("RO Standard Items",str(self.ro_template),"ro_recovery")
	# 				if(i.system == 'R.RO'):
	# 					i.feed_flow=(float(self.flow) * (1-(float(ro_recovery)/100)) * 1.05)
	# 					if(i.size == 40):
	# 						i.no_of_filter = int(-1 * (i.feed_flow * 0.001657867) // 1 * -1)
	# 					elif(i.size == 32):
	# 						i.no_of_filter = int(-1 * (i.feed_flow * 0.004282824) // 1 * -1)
	# 				else:
	# 					i.feed_flow=self.flow
	# 					if(i.size == 40):
	# 						i.no_of_filter = int(-1 * (i.feed_flow * 0.001657867) // 1 * -1)
	# 					elif(i.size == 32):
	# 						i.no_of_filter = int(-1 * (i.feed_flow * 0.004282824) // 1 * -1)
	# 				for j in frappe.db.sql("SELECT rate FROM `tabState rate chemical` WHERE system='"+str(i.prefilter)+"' and state='"+str(self.state)+"'",as_dict=1):
	# 					i.unit_cost=j.rate * (1+(self.transport_per/100))
	# 				i.cost_day = i.no_of_filter * (i.unit_cost/i.replacing_fre)
	# 				i.cost_m3 = i.cost_day/self.flow
					
	# 				if(i.system == 'RO'):
	# 					conro=conro+i.cost_m3
	# 				elif(i.system == 'RO WO'):
	# 					conrwo=conrwo+i.cost_m3
	# 				elif(i.system == 'R.RO'):
	# 					conrro=conrro+i.cost_m3
	# 			self.total_ro_consumables=conro
	# 			self.total_ro_wo_consumables=conrwo
	# 			self.total_r_ro_consumables=conrro
				
	# 		for i in self.running_chemical:
	# 			ro_recovery=frappe.db.get_value("RO Standard Items",str(self.ro_template),"ro_recovery")
	# 			if(i.system == 'CTS' or i.system=='CTS WO DGT' or i.system=='CHLORINATION' or i.system=='R. DGT' or i.system=='R.RO'):
	# 				i.system_feed=(float(self.flow) * (1-(float(ro_recovery)/100)) * 1.05)
	# 			else:
	# 				i.system_feed=self.flow
	# 			i.consumption = i.concentration * self.flow / 1000
	# 			if(i.system=="CTS MBR"):
	# 				i.consumption = i.concentration * float(cts_capacity) / 1000
	# 			for j in frappe.db.sql("SELECT rate FROM `tabState rate chemical` WHERE system='"+str(i.chemical_name)+"' and state='"+str(self.state)+"'",as_dict=1):
	# 				i.unit_cost=j.rate * (1+(self.transport_per/100))
	# 			i.chemical_cost_day = i.unit_cost * i.consumption
	# 			i.chemical_cost_m3 = i.chemical_cost_day/self.flow
				
	# 		rumdaf=0
	# 		runro=0
	# 		runrowo=0
	# 		runcts=0
	# 		runctswo=0
	# 		runchro=0
	# 		runrro=0
	# 		for i in self.running_chemical:
	# 			if(i.system == 'DAF'):
	# 				rumdaf=rumdaf+i.chemical_cost_m3
	# 			elif(i.system == 'RO'):
	# 				runro=runro+i.chemical_cost_m3
	# 			elif(i.system == 'RO WO DGT'):
	# 				runrowo=runrowo+i.chemical_cost_m3
	# 			elif(i.system == 'CTS'):
	# 				runcts=runcts+i.chemical_cost_m3
	# 			elif(i.system == 'CTS WO DGT'):
	# 				runctswo=runctswo+i.chemical_cost_m3
	# 			elif(i.system == 'CHLORINATION'):
	# 				runchro=runchro+i.chemical_cost_m3
	# 			elif(i.system == 'R.RO'):
	# 				runrro=runrro+i.chemical_cost_m3
			
	# 		for i in self.running_chemical:
	# 			for j in self.final_chemical:
	# 				if(i.system == j.system):
	# 					if(i.system not in ['DAF','RO','RO WO DGT','CTS','CTS WO DGT','CHLORINATION','R.RO']):
	# 						j.running = i.chemical_cost_m3
	# 		for i in self.final_chemical:
	# 			if(i.system =='RO'):
	# 				i.consumables = self.total_ro_consumables
	# 				i.cleaning = self.total_ro
	# 				i.running = runro
	# 			elif(i.system == 'RO WO DGT'):
	# 				i.consumables = self.total_ro_wo_consumables
	# 				i.cleaning = self.total_ro_wo_dgt
	# 				i.running = runrowo
	# 			elif(i.system == 'R.RO'):
	# 				i.consumables = self.total_r_ro_consumables
	# 				i.cleaning = self.total_r_ro
	# 				i.running = runrro
	# 			elif(i.system == 'MBR'):
	# 				i.cleaning = self.total_mbr
	# 			elif(i.system == 'MF'):
	# 				i.cleaning = self.total_mf
	# 			elif(i.system == 'R. MF'):
	# 				i.cleaning = self.total_r_mf
	# 			elif(i.system == 'DAF'):
	# 				i.running = rumdaf
	# 			elif(i.system == 'CTS'):
	# 				i.running = runcts
	# 			elif(i.system == 'CTS WO DGT'):
	# 				i.running = runctswo
	# 			elif(i.system == 'CHLORINATION'):
	# 				i.running = runchro
					
	# 		for i in self.final_chemical:
	# 			if(i.running is None):
	# 				i.running=0
	# 			if(i.consumables is None):
	# 				i.consumables=0
	# 			if(i.cleaning is None):
	# 				i.cleaning=0
	# 			i.per100 = i.consumables + i.cleaning + i.running
	# 			i.per90 = (i.running + ((i.cleaning + i.consumables)/0.9))
	# 			i.per80 = (i.running + ((i.cleaning + i.consumables)/0.8))
	# 			i.per70 = (i.running + ((i.cleaning + i.consumables)/0.7))
	# 			i.per60 = (i.running + ((i.cleaning + i.consumables)/0.6))
	# 		ar=[]	
	# 		for i in self.running_chemical:
	# 			ar.append({
	# 				i.chemical_name:i.chemical_cost_m3
	# 			})
	# 		arr=[]	
	# 		for i in self.cleaning_chemical:
	# 			arr.append({
	# 				i.chemical_name:i.cost_m3
	# 			})
			
	# 		dict1 =ar
	# 		final = {}
	# 		for d in dict1:
	# 			for k in d.keys():
	# 				final[k] = final.get(k,0) + d[k]
			
	# 		dict2 =arr
	# 		arrfinal = {}
	# 		for d in dict2:
	# 			for k in d.keys():
	# 				arrfinal[k] = arrfinal.get(k,0) + d[k]
			
	# 		ar=[]
	# 		ar.append(final)
	# 		ar.append(arrfinal)
	# 		vfinal = {}
	# 		for d in ar:
	# 			for k in d.keys():
	# 				vfinal[k] = vfinal.get(k,0) + d[k]
			
	# 		self.chemical_consumption_per_day=[]
	# 		for j in vfinal:
	# 			self.append('chemical_consumption_per_day',{
	# 				"chemical":j,
	# 				})
	# 		for i in self.chemical_consumption_per_day:
	# 			for j in vfinal:
	# 				if(i.chemical == j):
	# 					i.kg=vfinal[i.chemical]
	# 			for j in frappe.db.sql("SELECT rate FROM `tabState rate chemical` WHERE system='"+str(i.chemical)+"' and state='"+str(self.state)+"'",as_dict=1):
	# 				i.unitcost=j.rate * (1+(self.transport_per/100))
	# 			i.rsday = i.kg * i.unitcost
			
	# 		che_100=0
	# 		che_90=0
	# 		for i in self.final_chemical:
	# 			che_100=che_100+float(i.per100)
	# 			che_90=che_90+float(i.per90)
	# 		self.total_chemical_100 = che_100
	# 		self.total_chemical_90 = che_90
	# 	except Exception as e:
	# 		error_message = f"An error occurred: {str(e)} (Line {traceback.extract_tb(e.__traceback__)[0].lineno})"
	# 		frappe.throw(str(error_message))
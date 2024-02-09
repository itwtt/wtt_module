# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from datetime import datetime
import traceback
from frappe.model.mapper import get_mapped_doc
from frappe.utils.file_manager import save_file
from frappe.utils.pdf import get_pdf
from pdfkit import from_file

class CostWorkingTool(Document):
    def validate(self):
        try:
            if(self.name not in ["COSTING-WTT-0614-405", "COSTING-WTT-0591-419", "COSTING-WTT-0591-420", "COSTING-WTT-0576-428", "COSTING-WTT-0576-429", "COSTING-WTT-0526-416", "COSTING-WTT-0596-376", "COSTING-WTT-0523-374", "COSTING-WTT-0609-373", "COSTING-WTT-0609-361"]):
                ##bio pipe escalation
                systems_list=["Lifting sump", "DAF (Dissolved Air Flotation)", "Equalization System", "Neutralization System", "Cooling Tower", "De-Nitrification System", "Distribution system", "Biological Oxidation System", "Clarifier Feed Tank", "SRS System", "Belt Press", "Screw Press", "Drum Screener", "Lamella Settler", "DO increase system","Ammonia Striper"]
                pipe_percentage=[2, 7, 5, 5, 1, 5, 2, 10, 1, 5, 10, 10, 1, 1, 5,5]
                if(self.pipe_escalation==[]):
                    for pipe_esc in range(len(systems_list)):
                        self.append("pipe_escalation",{
                            "system_name":systems_list[pipe_esc],
                            "default_pipe_escalation":pipe_percentage[pipe_esc]
                        })
                ##bio pipe escalation
                ##list bio_full_system
                selected_s=[]
                self.selected_process_system=[]
                for v in frappe.db.sql("SELECT selected_system_name,selected_type FROM `tabSelected Process System` where parent='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    selected_s.append(v.selected_system_name)
                    self.append("selected_process_system",v)
                dd=frappe.db.get_value("Startup Sheet",self.project_startup_sheet,'clarifier_diameter')
                ar=["Chlorination system", "Sand Filter", "Reverse Osmosis", "Hardness and Color Removal System", "Crystallizer", "Hardness and Silica Removal System", "Self-Cleaning Filter", "Reject Reverse Osmosis", "Degasser System", "Nano Filtration", "Care system", "Evaporator", "Agitated Thin film dryer", "Activated Carbon Filter", "Sulphur Black Removal System", "Centrifuge", "Micro Filtration - ASAHI","Submerged MBR system - OVIVO","Submerged MBR system - KOCH","Rewolutte RO","CTS MBR"]
                ar2=[]
                if(self.edit_bio_full_system!=1):
                    self.bio_full_system=[]
                    for i in range(len(selected_s)):
                        if(selected_s[i] not in ar):
                            system=str(selected_s[i])
                            qt=0
                            parameter=''
                            value=''
                            pipe_percent=0
                            for pe in range(len(systems_list)):
                                if(selected_s[i]==systems_list[pe]):
                                    pipe_percent=pipe_percentage[pe]
                            if(system=="Circular Clarifier System"):
                                parameter="DIAMETER"
                                value=int(dd)
                                # value=str(16)
                            elif(system=="Degasser System"):
                                parameter="DIAMETER"
                                if(self.flow>=400 and self.flow<=600):value=1
                                elif(self.flow>600 and self.flow<=1000):value=1.4
                                elif(self.flow>1000 and self.flow<=1600):value=1.8
                                elif(self.flow>1600 and self.flow<=2500):value=2.2
                                elif(self.flow>2500):value=3
                            elif(system=="Rotary Brush Screener"):
                                parameter="WIDTH"
                                if(self.flow>=0 and self.flow<=2150):value=600
                                elif(self.flow>2150 and self.flow<=4600):value=800
                                elif(self.flow>4600 and self.flow<=7000):value=1200
                                elif(self.flow>7000):value=2.2
                            elif(system=="Cooling Tower"):
                                parameter="FLOW"
                                if(self.flow>0 and self.flow<=750):value=750
                                elif(self.flow>750):value=1500
                            elif(system=="Belt Press"):
                                parameter="EDOM"
                                if(self.withcheck==1):
                                    if(self.with_b>0 and self.with_b<=2.5):value=500
                                    elif(self.with_b>2.5 and self.with_b<=4.5):value=800
                                    elif(self.with_b>4.5):value=1300
                                else:
                                    if(self.without>0 and self.without<=2.5):value=500
                                    elif(self.without>2.5 and self.without<=4.5):value=800
                                    elif(self.without>4.5):value=1300
                            elif(system=="Screw Press"):
                                parameter="FLOW / HR"
                                if(self.withcheck==1):
                                    if(self.with_b>0 and self.with_b<=2):value=2
                                    elif(self.with_b>2 and self.with_b<=3):value=3
                                    elif(self.with_b>3 and self.with_b<=5):value=5
                                    elif(self.with_b>5):value=10
                                else:
                                    if(self.without>0 and self.without<=2):value=2
                                    elif(self.without>2 and self.without<=3):value=3
                                    elif(self.without>3 and self.without<=5):value=5
                                    elif(self.without>5):value=10
                            elif(system=="Self-Cleaning Filter"):
                                parameter=="FLOW / HR"
                                ts=self.flow/20
                                if(ts>0 and ts<=30):value=30
                                elif(ts>30 and ts<=41):value=41
                                elif(ts>41 and ts<=82):value=82
                                elif(ts>82):value=90
                            elif(system=="DAF (Dissolved Air Flotation)"):
                                parameter="DIMENSION"
                                if(self.flow>0 and self.flow<=1152):value="2X5"
                                elif(self.flow>1152 and self.flow<=1728):value="3X5"
                                elif(self.flow>1728 and self.flow<=2300):value="2X5"
                                elif(self.flow>2300):value="3X5"
                            elif(system=="Drum Screener"):
                                parameter="SIZE"
                                value=600
                            elif(system=="Sludge Thickener with mech"):
                                parameter="DIAMETER"
                                if(self.with_b>=0 and self.with_b<=14):value=5
                                elif(self.with_b>14):value=10
                                if(self.with_b>50):qt=2
                            self.append("bio_full_system",{
                                "item_description":system,
                                "parameter":parameter,
                                "range":value,
                                "pipes_per":pipe_percent
                                })
                ##list bio_full_system
                ##list electrical items
                mf_ele=["PRE-FILTER","FEED PUMP", "BACKWASH PUMP", "CIP PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2","CIP DOSING PUMP-3"]
                sel_system=[]
                for v in frappe.db.sql("SELECT selected_system_name FROM `tabSelected Process System` where parent='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    sel_system.append(v.selected_system_name)
                
                if("Sulphur Black Removal System" in sel_system):
                    mf_ele.extend(["SULPHUR BLACK SLUDGE PUMP","SULPHUR BLACK DOSING PUMP"])
                # mf_ele.extend(["PANEL","PLC"])
                
                item37=["PRE-FILTER"]
                item18=["SULPHUR BLACK SLUDGE PUMP"]
                item19=["SULPHUR BLACK DOSING PUMP","CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3"]
                plc=["PANEL","PLC"]
                kw=0.18
                self.mf_electrical_items=[]
                for i in range(len(mf_ele)):
                    if(mf_ele[i] in item37):kw=0.37
                    elif(mf_ele[i] in item18):kw=0.18
                    elif(mf_ele[i] in item19):kw=0.37
                    elif(mf_ele[i] in plc):kw=1
                    tt="DOL FEEDER"
                    if(kw>5.5):tt="S/D FEEDER"
                    if(mf_ele[i]=="BACKWASH PUMP"):
                        if(frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"loop_operation")=="Single"):
                            mf_ele[i]="FEED/BW PUMP"
                        self.append("mf_electrical_items",{
                            "item_description":mf_ele[i],
                            "kw":kw,
                            "type":tt,
                            "vfd_type":"VFD FEEDER"
                        })
                    elif(mf_ele[i]=="FEED PUMP"):
                        if(frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"loop_operation")=="Double"):
                            self.append("mf_electrical_items",{
                                "item_description":mf_ele[i],
                                "kw":kw,
                                "type":tt
                            })
                    else:
                        self.append("mf_electrical_items",{
                            "item_description":mf_ele[i],
                            "kw":kw,
                            "type":tt
                        })
                
                mbr_ele=["PERMEATE/BACKWASH/CIP PUMP","MBR BLOWER"]
                mb_type = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbr_type")
                if(mb_type == 'SUB-UF'):
                    mbr_ele.append("SLUDGE EXTRACT PUMP")
                else:
                    mbr_ele.append("SLUDGE RECIRCULATION PUMP")
                
                sel_system=[]
                for v in frappe.db.sql("SELECT selected_system_name FROM `tabSelected Process System` where parent='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    sel_system.append(v.selected_system_name)
                
                if("Sulphur Black Removal System" in sel_system):
                    mbr_ele.extend(["SULPHUR BLACK SLUDGE PUMP","SULPHUR BLACK DOSING PUMP"])
                
                mbr_ele.extend(["CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3"])
                items018=["CIP DOSING PUMP-1","CIP DOSING PUMP-2","CIP DOSING PUMP-3","SULPHUR BLACK DOSING PUMP"]
                items037=["PRE-FILTER"]
                plc=["PANEL","PLC"]
                kw=0.18
                self.mbr_electrical_items=[]
                for i in range(len(mbr_ele)):
                    if(mbr_ele[i] in item37):kw=0.37
                    elif(mbr_ele[i] in item18):kw=0.18
                    elif(mbr_ele[i] in items018):kw=0.37
                    elif(mbr_ele[i] in plc):kw=1
                    tt="DOL FEEDER"
                    if(kw>5.5):tt="S/D FEEDER"
                    if(mbr_ele[i]=="PERMEATE/BACKWASH/CIP PUMP"):
                        self.append("mbr_electrical_items",{
                            "item_description":mbr_ele[i],
                            "kw":kw,
                            "type":tt,
                            "vfd_type":"VFD FEEDER"
                        })
                    elif(mbr_ele[i]=="MBR BLOWER"):
                        mbr_blower_flow=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbr_blower__train1")
                        flow3min = mbr_blower_flow * 0.588578
                        mbr_range = 0.45
                        inchh2 = mbr_range * 401.865
                        power = ((flow3min * inchh2)/(6356 * 0.67))/1.34
                        if(power<=0.045):kw=0.045
                        elif(power<=0.18):kw=0.18
                        elif(power<=0.37):kw=0.37
                        elif(power<=0.55):kw=0.55
                        elif(power<=0.75):kw=0.75
                        elif(power<=1.1):kw=1.1
                        elif(power<=1.5):kw=1.5
                        elif(power<=2.2):kw=2.2
                        elif(power<=3.7):kw=3.7
                        elif(power<=4):kw=4
                        elif(power<=5.5):kw=5.5
                        elif(power<=7.5):kw=7.5
                        elif(power<=11):kw=11
                        elif(power<=15):kw=15
                        elif(power<=18.5):kw=18.5
                        elif(power<=22):kw=22
                        elif(power<=30):kw=30
                        elif(power<=37):kw=37
                        elif(power<=45):kw=45
                        elif(power<=55):kw=55
                        elif(power<=75):kw=75
                        elif(power<=90):kw=90
                        elif(power<=110):kw=110
                        elif(power<=160):kw=160
                        elif(power>160):kw=0
                        if(kw>5.5):tt="S/D FEEDER"
                        self.append("mbr_electrical_items",{
                            "item_description":mbr_ele[i],
                            "kw":kw,
                            "type":tt
                        })
                    else:
                        self.append("mbr_electrical_items",{
                            "item_description":mbr_ele[i],
                            "kw":kw,
                            "type":tt
                        })
                
                ovivo_ele=["PERMEATE PUMP","BACKWASH/CIP PUMP","MBR BLOWER"]
                for i in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    if(i.ovivo_type == 'S-UF'):
                        ovivo_ele.append("SLUDGE EXTRACT PUMP")
                    else:
                        ovivo_ele.append("SLUDGE RECIRCULATION PUMP")
                        
                sel_system=[]
                for v in frappe.db.sql("SELECT selected_system_name FROM `tabSelected Process System` where parent='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    sel_system.append(v.selected_system_name)
                
                if("Sulphur Black Removal System" in sel_system):
                    ovivo_ele.extend(["SULPHUR BLACK SLUDGE PUMP","SULPHUR BLACK DOSING PUMP"])
                    
                ovivo_ele.extend(["SPRINKLER PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3"])
                mbr_ovivo_dos=["CIP DOSING PUMP-1","CIP DOSING PUMP-2","CIP DOSING PUMP-3","SULPHUR BLACK DOSING PUMP"]
                items037=["PRE-FILTER"]
                plc=["PANEL","PLC"]
                kw=0.18
                self.ovivo_electrical_items=[]
                for i in range(len(ovivo_ele)):
                    if(ovivo_ele[i] in item37):kw=0.37
                    elif(ovivo_ele[i] in item18):kw=0.18
                    elif(ovivo_ele[i] in mbr_ovivo_dos):kw=0.37
                    elif(ovivo_ele[i] in plc):kw=1
                    tt="DOL FEEDER"
                    if(kw>5.5):tt="S/D FEEDER"
                    if(ovivo_ele[i]=="BACKWASH/CIP PUMP" or ovivo_ele[i]=="SPRINKLER PUMP"):
                        self.append("ovivo_electrical_items",{
                            "item_description":ovivo_ele[i],
                            "kw":kw,
                            "type":tt,
                            "vfd_type":"VFD FEEDER"
                        })
                    elif(ovivo_ele[i]=="MBR BLOWER"):
                        ovivo_blower=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"ovivo_blower")
                        flow3min = ovivo_blower * 0.588578
                        mbr_range = 0.45
                        inchh2 = mbr_range * 401.865
                        power = ((flow3min * inchh2)/(6356 * 0.67))/1.34
                        if(power<=0.045):kw=0.045
                        elif(power<=0.18):kw=0.18
                        elif(power<=0.37):kw=0.37
                        elif(power<=0.55):kw=0.55
                        elif(power<=0.75):kw=0.75
                        elif(power<=1.1):kw=1.1
                        elif(power<=1.5):kw=1.5
                        elif(power<=2.2):kw=2.2
                        elif(power<=3.7):kw=3.7
                        elif(power<=4):kw=4
                        elif(power<=5.5):kw=5.5
                        elif(power<=7.5):kw=7.5
                        elif(power<=11):kw=11
                        elif(power<=15):kw=15
                        elif(power<=18.5):kw=18.5
                        elif(power<=22):kw=22
                        elif(power<=30):kw=30
                        elif(power<=37):kw=37
                        elif(power<=45):kw=45
                        elif(power<=55):kw=55
                        elif(power<=75):kw=75
                        elif(power<=90):kw=90
                        elif(power<=110):kw=110
                        elif(power<=160):kw=160
                        elif(power>160):kw=0
                        if(kw>5.5):tt="S/D FEEDER"
                        self.append("ovivo_electrical_items",{
                            "item_description":ovivo_ele[i],
                            "kw":kw,
                            "type":tt,
                            "w_qty":1
                        })
                    else:
                        self.append("ovivo_electrical_items",{
                            "item_description":ovivo_ele[i],
                            "kw":kw,
                            "type":tt
                        })
                
                mbr_cts_ele=["PERMEATE PUMP","BACKWASH/CIP PUMP","MBR BLOWER"]
                for i in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    if(i.cts_ovivo_type == 'S-UF'):
                        mbr_cts_ele.append("SLUDGE EXTRACT PUMP")
                    else:
                        mbr_cts_ele.append("SLUDGE RECIRCULATION PUMP")
                        
                sel_system=[]
                for v in frappe.db.sql("SELECT selected_system_name FROM `tabSelected Process System` where parent='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    sel_system.append(v.selected_system_name)
                
                if("Sulphur Black Removal System" in sel_system):
                    mbr_cts_ele.extend(["SULPHUR BLACK SLUDGE PUMP","SULPHUR BLACK DOSING PUMP"])
                
                mbr_cts_ele.extend(["SPRINKLER PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3"])
                mbr_cts_ovivo_dos=["CIP DOSING PUMP-1","CIP DOSING PUMP-2","CIP DOSING PUMP-3","SULPHUR BLACK DOSING PUMP"]
                items037=["PRE-FILTER"]
                plc=["PANEL","PLC"]
                kw=0.18
                self.mbr_cts_electrical_items=[]
                for i in range(len(mbr_cts_ele)):
                    if(mbr_cts_ele[i] in item37):kw=0.37
                    elif(mbr_cts_ele[i] in mbr_cts_ovivo_dos):kw=0.37
                    elif(mbr_cts_ele[i] in plc):kw=1
                    tt="DOL FEEDER"
                    if(kw>5.5):tt="S/D FEEDER"
                    if(mbr_cts_ele[i]=="BACKWASH/CIP PUMP"):
                        self.append("mbr_cts_electrical_items",{
                            "item_description":mbr_cts_ele[i],
                            "kw":kw,
                            "type":tt,
                            "vfd_type":"VFD FEEDER"
                        })
                    elif(ovivo_ele[i]=="MBR BLOWER"):
                        ovivo_blower=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"cts_ovivo_blower")
                        flow3min = ovivo_blower * 0.588578
                        mbr_range = 0.45
                        inchh2 = mbr_range * 401.865
                        power = ((flow3min * inchh2)/(6356 * 0.67))/1.34
                        if(power<=0.045):kw=0.045
                        elif(power<=0.18):kw=0.18
                        elif(power<=0.37):kw=0.37
                        elif(power<=0.55):kw=0.55
                        elif(power<=0.75):kw=0.75
                        elif(power<=1.1):kw=1.1
                        elif(power<=1.5):kw=1.5
                        elif(power<=2.2):kw=2.2
                        elif(power<=3.7):kw=3.7
                        elif(power<=4):kw=4
                        elif(power<=5.5):kw=5.5
                        elif(power<=7.5):kw=7.5
                        elif(power<=11):kw=11
                        elif(power<=15):kw=15
                        elif(power<=18.5):kw=18.5
                        elif(power<=22):kw=22
                        elif(power<=30):kw=30
                        elif(power<=37):kw=37
                        elif(power<=45):kw=45
                        elif(power<=55):kw=55
                        elif(power<=75):kw=75
                        elif(power<=90):kw=90
                        elif(power<=110):kw=110
                        elif(power<=160):kw=160
                        elif(power>160):kw=0
                        if(kw>5.5):tt="S/D FEEDER"
                        self.append("mbr_cts_electrical_items",{
                            "item_description":ovivo_ele[i],
                            "kw":kw,
                            "type":tt,
                            "w_qty":1
                        })
                    else:
                        self.append("mbr_cts_electrical_items",{
                            "item_description":mbr_cts_ele[i],
                            "kw":kw,
                            "type":tt
                        })
                
                sel_system=[]
                for v in frappe.db.sql("SELECT selected_system_name FROM `tabSelected Process System` where parent='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    sel_system.append(v.selected_system_name)
                bio_ele=[]
                bio_sys=[]
                if "Rotary Brush Screener" in sel_system:
                    bio_ele.append("ROTARY BRUSH SCREENER")
                    bio_sys.append("Rotary Brush Screener")
                if "Drum Screener" in sel_system:
                    bio_ele.append("DRUM SCREENER")
                    bio_sys.append("Drum Screener")
                if "Lifting sump" in sel_system:
                    bio_ele.append("LIFTING SUMP PUMP")
                    bio_sys.append("Lifting sump")
                else:
                    if "DAF (Dissolved Air Flotation)" in sel_system:
                        bio_ele.append("DAF FEED PUMP")
                        bio_sys.append("DAF (Dissolved Air Flotation)")
                if "DAF (Dissolved Air Flotation)" in sel_system:
                    bio_ele.extend(["DAF SCRAPPER", "DAF SLUDGE PUMP", "DAF BUBBLE GENERATION PUMP"])
                    bio_sys.extend(["DAF (Dissolved Air Flotation)","DAF (Dissolved Air Flotation)","DAF (Dissolved Air Flotation)"])
                    if((frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"daf_with_dosing")==1)):
                        bio_ele.extend(["DAF DOSING PUMP-1", "DAF DOSING PUMP-2"])
                        bio_sys.extend(["DAF (Dissolved Air Flotation)","DAF (Dissolved Air Flotation)"])
                if "Equalization System" in sel_system:
                    for m in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(self.project_startup_sheet)+"'",as_dict=1):
                        if(m.seperate_blower_for_equalization_tank == 1):
                            bio_ele.extend(["EQT BLOWER"])
                            bio_sys.append("Equalization System")
                if "Neutralization System" in sel_system:
                    bio_ele.extend(["NT PUMP", "NT DOSING PUMP"])
                    bio_sys.extend(["Neutralization System","Neutralization System"])
                if "Cooling Tower" in sel_system:
                    bio_ele.append("COOLING TOWER")
                    bio_sys.append("Cooling Tower")
                if "De-Nitrification System" in sel_system:
                    bio_ele.extend(["DNT PUMP", "DNT FLOW MIXER"])
                    bio_sys.extend(["De-Nitrification System","De-Nitrification System"])
                if "Biological Oxidation System" in sel_system:
                    bio_ele.extend(["BIO BLOWER"])
                    bio_sys.extend(["Biological Oxidation System"])
                if "Circular Clarifier System" in sel_system:
                    bio_ele.append("CIRCULAR CLARIFIER SYSTEM")
                    bio_sys.append("Circular Clarifier System")
                if "SRS System" in sel_system:
                    bio_ele.append("SRS PUMP")
                    bio_sys.append("SRS System")
                if "Sludge Thickener with mech" in sel_system:
                    bio_ele.append("SLUDGE THICKENER WITH MECH")
                    bio_sys.append("Sludge Thickener with mech")
                if "Belt Press" in sel_system:
                    bio_ele.extend(["BELT PRESS", "BELT POLY UNIT MODEL", "BELT FEED PUMP", "BELT WASHING PUMP", "BELT PRESS AGITATOR"])
                    bio_sys.extend(["Belt Press","Belt Press","Belt Press","Belt Press","Belt Press"])
                if "Screw Press" in sel_system:
                    bio_ele.extend(["SCREW PRESS", "SCREW POLY UNIT MODEL", "SCREW FEED PUMP", "SCREW PRESS AGITATOR"])
                    bio_sys.extend(["Screw Press","Screw Press","Screw Press","Screw Press"])
                if("Ammonia Striper" in sel_system):
                    bio_ele.extend(["BLOWER","DOSING PUMP"])
                    bio_sys.extend(["Ammonia Striper","Ammonia Striper"])
                # bio_ele.extend(["PLC","PANEL"])
                for m in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    if(m.eqt_tank_type == "Carousel"):
                        bio_ele.append("EQT FLOW MAKER")
                        bio_sys.append("Equalization System")
                    if(m.bio_tank_type == "Carousel"):
                        bio_ele.append("BIO FLOW MAKER")
                        bio_sys.append("Biological Oxidation System")
                plc=["PANEL","PLC"]
                kw=0.18
                self.bio_electrical_items=[]
                for i in range(len(bio_ele)):
                    if(bio_ele[i] in plc):kw=1
                    tt="DOL FEEDER"
                    if(kw>5.5):tt="S/D FEEDER"
                    if(bio_ele[i]=="BIO BLOWER"):
                        self.append("bio_electrical_items",{
                            "item_description":bio_ele[i],
                            "system":bio_sys[i],
                            "kw":kw,
                            "type":tt,
                            "vfd_type":"VFD FEEDER"
                        })
                    else:
                        self.append("bio_electrical_items",{
                            "item_description":bio_ele[i],
                            "system":bio_sys[i],
                            "kw":kw,
                            "type":tt
                        })
                cts_ele=["FEED PUMP", "SLUDGE PUMP", "DOSING PUMP-1", "DOSING PUMP-2", "DOSING PUMP-3", "DOSING PUMP-4", "DOSING PUMP-5", "AGITATOR"]
                plc=["PANEL","PLC"]
                dos = ["DOSING PUMP-1", "DOSING PUMP-2", "DOSING PUMP-3", "DOSING PUMP-4", "DOSING PUMP-5"]
                kw=0.18
                self.cts_electrical_items=[]
                for i in range(len(cts_ele)):
                    if(cts_ele[i] in plc):
                        kw=1
                    tt="DOL FEEDER"
                    if(kw>5.5):
                        tt="S/D FEEDER"
                    self.append("cts_electrical_items",{
                        "item_description":cts_ele[i],
                        "kw":kw,
                        "type":tt
                    })
                dgt_ele=["BLOWER","DOSING PUMP"]
                plc=["PANEL","PLC"]
                self.dgt_electrical_items=[]
                for i in range(len(dgt_ele)):
                    tt="DOL FEEDER"
                    if(kw>5.5):
                        tt="S/D FEEDER"
                    self.append("dgt_electrical_items",{
                        "item_description":dgt_ele[i],
                        "type":tt
                    })
                #FAB
                if(self.edit_qty!=1):
                    self.fabrication_table = []
                    for i in frappe.db.sql("SELECT * FROM `tabFabrication Table` INNER JOIN `tabFabrication` ON `tabFabrication`.name=`tabFabrication Table`.parent WHERE `tabFabrication`.docstatus=0 and `tabFabrication Table`.system!='REVERSE OSMOSIS' and `tabFabrication Table`.system!='REJECT REVERSE OSMOSIS' ",as_dict=1):
                        if(float(self.flow)>float(i.min_flow) and float(self.flow)<=float(i.max_flow)):
                            self.append('fabrication_table', {
                                'system':i.system,
                                'days': i.days,
                                'persons':i.persons,
                                'charges':i.charges,
                                'qty':i.qty,
                                'consumables':i.consumables,
                                'total_charges':i.total_charges
                            })
                        self.total_fabrication_cost=i.total_cost
                        
                #mf
                mf = ["PRE-FILTER", "MODULES", "FEED PUMP", "BACKWASH PUMP", "FEED/BACKWASH PUMP", "CIP PUMP", "SULPHUR BLACK SLUDGE PUMP","SULPHUR BLACK DOSING PUMP", "SULPHUR BLACK LAMELLA SETTLER", "LEVEL TRANSMITTER", "LEVEL FLOAT", "ELECTROMAGNETIC FLOWMETER", "PRESSURE TRANSMITTER", "PRESSURE GAUGE", "PH SENSOR", "CIP PRE-FILTER","MF SKID FRAME", "PIPES,FITTINGS & VALVES", "FAB. & ERECTION" ,"CIP TANK","CIP FRAME","CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3", "CIP DOSING PUMP FRAME", "CIP SKID FRAME","CIP SKID FRAME","CIP DOSING TANK FRAME","CIP DOSING TANK-1", "CIP DOSING TANK-2","CIP DOSING TANK-3","CIP TANK FRAME"]
                self.mf_table = []
                prefilter=[]
                dtnk1=0
                dtnk2=0
                for i in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    for k in mf:
                        if(k == "PRE-FILTER"):
                            flow = (self.flow/21)*1.15
                            up=0
                            preflow=0
                            preqty=0
                            if(flow>0 and flow<=30):
                                preflow=30
                                preqty=1
                            elif(flow>30 and flow<=45):
                                preflow=45
                                preqty=1
                            elif(flow>45 and flow<=90):
                                preflow=82
                                preqty=1
                            elif(flow>90):
                                preflow=round(flow/2)
                                preqty=flow/82
                            
                            # if(preflow>0 and preflow<=30):up = 562325
                            # elif(preflow>30 and preflow<=45):up = 664415
                            # elif(preflow>45 and preflow<=82):up = 740775
                            if(preflow>0 and preflow<=30):up = (5650+1125)*1.1*(self.usd+2)
                            elif(preflow>30 and preflow<=45):up = (6880+1125)*1.1*(self.usd+2)
                            elif(preflow>45 and preflow<=82):up = (7800+1125)*1.1*(self.usd+2)
                            
                            self.append('mf_table', {
                                    "item_description":"PRE-FILTER",
                                    "flow":preflow,
                                    "w_qty":int(-1 * preqty // 1 * -1),
                                    "unit_price":up,
                                    "total_price":up*int(-1 * preqty // 1 * -1)
                                })
                        elif(k == "FEED PUMP"):
                            if(i.loop_operation == "Double"):
                                flowfeed=[]
                                addflow=float(i.feed_pump) +10
                                for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and flow>='"+str(i.feed_pump)+"' and flow<='"+str(addflow)+"' and range1>=4 ",as_dict=1):
                                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        flowfeed.append(g.base_rate)
                                if(flowfeed and i.feed_pump>0):
                                    self.append('mf_table', {
                                        "item_description":"FEED PUMP",
                                        "flow":i.feed_pump,
                                        "range":4,
                                        "w_qty":i.feed_qty,
                                        "sb_qty":1,
                                        "unit_price":g.base_rate,
                                        "total_price" : (g.base_rate * (i.feed_qty +1))
                                    })
                                else:
                                    self.append('mf_table', {
                                        "item_description":"FEED PUMP",
                                        "flow":i.feed_pump,
                                        "range":4,
                                        "w_qty":i.feed_qty,
                                        "sb_qty":1,
                                        "unit_price":0
                                    })
                        elif(k == "BACKWASH PUMP"):
                            if(i.loop_operation == "Single"):
                                backfeed=[]
                                addflow=float(i.bw_pump) +10
                                for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and flow>='"+str(i.bw_pump)+"' and flow<='"+str(addflow)+"' and range1>=4 ",as_dict=1):
                                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        backfeed.append(g.base_rate)
                                
                                if(backfeed and i.bw_pump>0):
                                    self.append('mf_table', {
                                        "item_description":"FEED/BW PUMP",
                                        "flow":i.bw_pump,
                                        "range":4,
                                        "w_qty":i.bw_qty,
                                        "sb_qty":1,
                                        "unit_price":g.base_rate,
                                        "total_price" : (g.base_rate * (i.bw_qty + 1))
                                    })
                                else:
                                    self.append('mf_table', {
                                        "item_description":"FEED/BW PUMP",
                                        "flow":i.bw_pump,
                                        "range":4,
                                        "w_qty":i.bw_qty,
                                        "sb_qty":1,
                                        "unit_price":0
                                    })
                            else:
                                backfeed=[]
                                addflow=float(i.bw_pump) +10
                                for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and flow>='"+str(i.bw_pump)+"' and flow<='"+str(addflow)+"' and range1>=4 ",as_dict=1):
                                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        backfeed.append(g.base_rate)
                                
                                if(backfeed and i.bw_pump>0):
                                    self.append('mf_table', {
                                        "item_description":"BACKWASH PUMP",
                                        "flow":i.bw_pump,
                                        "range":4,
                                        "w_qty":i.bw_qty,
                                        "sb_qty":1,
                                        "unit_price":g.base_rate,
                                        "total_price" : (g.base_rate * (i.bw_qty + 1))
                                    })
                                else:
                                    self.append('mf_table', {
                                        "item_description":"BACKWASH PUMP",
                                        "flow":i.bw_pump,
                                        "range":4,
                                        "w_qty":i.bw_qty,
                                        "sb_qty":1,
                                        "unit_price":0
                                    })
                        elif(k == "MODULES"):
                            mod=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='MICRO FILTER' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mod.append(g.base_rate)
                                    
                            if(mod):
                                self.append('mf_table', {
                                    "item_description":"MODULES",
                                    "flow":1,
                                    "w_qty":round(i.total_modules),
                                    "unit_price":float(mod[0])*1.1,
                                    "total_price" : (float(mod[0])*1.1 * round(i.total_modules))
                                })
                            else:
                                self.append('mf_table', {
                                    "item_description":"MODULES",
                                    "flow":1,
                                    "range":round(i.total_modules),
                                    "w_qty":i.bw_qty,
                                    "unit_price":0
                                })
                        elif(k == "CIP PUMP"):
                            cipfeed=[]
                            cipflow=float(i.cip_pump) +10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and flow>='"+str(i.cip_pump)+"' and flow<='"+str(cipflow)+"' and range1>=4 ",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    cipfeed.append(g.base_rate)
                            
                            if(cipfeed and i.cip_pump>0):
                                self.append('mf_table', {
                                    "item_description":"CIP PUMP",
                                    "flow":i.cip_pump,
                                    "range":4,
                                    "w_qty":i.cip_qty,
                                    "sb_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * (i.cip_qty +1))
                                })
                            else:
                                self.append('mf_table', {
                                    "item_description":"CIP PUMP",
                                    "flow":i.cip_pump,
                                    "range":4,
                                    "w_qty":i.cip_qty,
                                    "sb_qty":1,
                                    "unit_price":0
                                })
                        elif(k == "CIP DOSING PUMP-1"):
                            cipdose=[]
                            addflow=60
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='DOSING PUMP' and flow>='50' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    cipdose.append(g.base_rate)
                            
                            if(cipdose):
                                self.append('mf_table', {
                                    "item_description":"CIP DOSING PUMP-1",
                                    "flow":50,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 2)
                                })
                            else:
                                self.append('mf_table', {
                                    "item_description":"CIP DOSING PUMP-1",
                                    "flow":50,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":0,
                                })
                        elif(k == "CIP DOSING PUMP-2"):
                            cipdose=[]
                            addflow=60
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='DOSING PUMP' and flow>='50' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    cipdose.append(g.base_rate)
                            
                            if(cipdose):
                                self.append('mf_table', {
                                    "item_description":"CIP DOSING PUMP-2",
                                    "flow":50,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 2)
                                })
                            else:
                                self.append('mf_table', {
                                    "item_description":"CIP DOSING PUMP-2",
                                    "flow":50,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":0,
                                })
                        elif(k == "CIP DOSING PUMP-3"):
                            cipdose=[]
                            addflow=60
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='DOSING PUMP' and flow>='50' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    cipdose.append(g.base_rate)
                            
                            if(cipdose):
                                self.append('mf_table', {
                                    "item_description":"CIP DOSING PUMP-3",
                                    "flow":50,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 2)
                                })
                            else:
                                self.append('mf_table', {
                                    "item_description":"CIP DOSING PUMP-3",
                                    "flow":50,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":0,
                                })
                        elif(k == "LEVEL TRANSMITTER"):
                            lvltran=[]
                            flow=1
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='LEVEL TRANSMITTER' ",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    lvltran.append(g.base_rate)
                            
                            if(lvltran):
                                self.append('mf_table', {
                                    "item_description":"LEVEL TRANSMITTER",
                                    "flow":1,
                                    "range":i.tank_height,
                                    "w_qty":1,
                                    "unit_price":lvltran[0],
                                    "total_price" : (lvltran[0] * 1)
                                })
                            else:
                                self.append('mf_table', {
                                    "item_description":"LEVEL TRANSMITTER",
                                    "flow":1,
                                    "range":i.tank_height,
                                    "w_qty":1,
                                    "unit_price":0
                                })
                        elif(k == "LEVEL FLOAT"):
                            lvlfloat=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='LEVEL FLOAT' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    lvlfloat.append(g.base_rate)
                                    
                            if(lvlfloat):
                                self.append('mf_table', {
                                    "item_description":"LEVEL FLOAT",
                                    "flow":1,
                                    "w_qty":1,
                                    "unit_price":lvlfloat[0],
                                    "total_price" : (lvlfloat[0] * 1)
                                })
                            else:
                                self.append('mf_table', {
                                    "item_description":"LEVEL FLOAT",
                                    "flow":1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="ELECTROMAGNETIC FLOWMETER"):
                            elm=[]
                            addflow=float(i.bw_pump) +20
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='ELECTROMAGNETIC FLOWMETER' and flow>='"+str(i.bw_pump)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    elm.append(g.base_rate)
                            
                            if(elm and i.bw_pump>0):
                                self.append('mf_table', {
                                    "item_description":"ELECTROMAGNETIC FLOWMETER",
                                    "flow":i.bw_pump,
                                    "w_qty":i.no_of_loops + i.cip_qty + i.bw_qty,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * (i.no_of_loops + i.cip_qty + i.bw_qty))
                                })
                            else:
                                self.append('mf_table', {
                                    "item_description":"ELECTROMAGNETIC FLOWMETER",
                                    "flow":i.bw_pump,
                                    "w_qty":i.no_of_loops + i.cip_qty + i.bw_qty,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k == "PRESSURE TRANSMITTER"):
                            pressure=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='PRESSURE TRANSMITTER' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    pressure.append(g.base_rate)
                                    
                            if(pressure):
                                self.append('mf_table', {
                                    "item_description":"PRESSURE TRANSMITTER",
                                    "flow":1,
                                    "w_qty":((i.no_of_loops * 2)+1+1),
                                    "unit_price":pressure[0],
                                    "total_price" : (pressure[0] * ((i.no_of_loops * 2)+1+1))
                                })
                            else:
                                self.append('mf_table', {
                                    "item_description":"PRESSURE TRANSMITTER",
                                    "flow":1,
                                    "w_qty":((i.no_of_loops * 2)+1+1),
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k == "PRESSURE GAUGE"):
                            pressure=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='PRESSURE GAUGE' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    pressure.append(g.base_rate)
                                    
                            if(pressure):
                                self.append('mf_table', {
                                    "item_description":"PRESSURE GAUGE",
                                    "flow":1,
                                    "w_qty":((i.no_of_loops * 2)+1+2),
                                    "unit_price":pressure[0],
                                    "total_price" : (pressure[0] * ((i.no_of_loops * 2)+1+2))
                                })
                            else:
                                self.append('mf_table', {
                                    "item_description":"PRESSURE GAUGE",
                                    "flow":1,
                                    "w_qty":((i.no_of_loops * 2)+1+2),
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k == "PH SENSOR"):
                            ph=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='PH SENSOR' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    ph.append(g.base_rate)
                                    
                            if(ph):
                                self.append('mf_table', {
                                    "item_description":"PH SENSOR",
                                    "flow":1,
                                    "w_qty":1,
                                    "unit_price":ph[0],
                                    "total_price" : (ph[0] * 1)
                                })
                            else:
                                self.append('mf_table', {
                                     "item_description":"PRESSURE GAUGE",
                                    "flow":1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k == "CIP PRE-FILTER"):
                            cippre=[]
                            addflow=(i.cip_pump * 1.5) +50
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='BAG FILTER' and flow>='"+str(i.cip_pump * 1.5)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' and `tabPurchase Order Item`.`base_rate`>0 ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    cippre.append(g.base_rate)
                            if(cippre and i.cip_pump>0):
                                ccip1 = (i.cip_pump * 1.5)
                                ccip2 = ccip1/150
                                ccip3 = int(-1 * ccip2 // 1 * -1)
                                ccip4 = (i.cip_pump * 1.5)/ccip3
                                # ccqty = 
                                self.append('mf_table', {
                                    "item_description":"CIP PRE-FILTER",
                                    "flow":ccip4,
                                    "w_qty":ccip3,
                                    "unit_price":cippre[0],
                                    "total_price" : (cippre[0] * ccip3)
                                })
                            else:
                                ccip1 = (i.cip_pump * 1.5)
                                ccip2 = ccip1/150
                                ccip3 = int(-1 * ccip2 // 1 * -1)
                                if(ccip3!=0):
                                	ccip4 = (i.cip_pump * 1.5)/ccip3
                                else:
                                	ccip4=0
                                self.append('mf_table', {
                                    "item_description":"CIP PRE-FILTER",
                                    "flow":ccip4,
                                    "w_qty":ccip3,
                                    "unit_price":0,
                                    "total_price" : 0
                                })   
                        elif(k=="CIP TANK"):
                            ciptank=[]
                            ciptankflow=0
                            if(i.loop_operation == 'Single'):
                                ciptankflow = i.modules_per_loop * 80
                            else:
                                ciptankflow = (i.modules_per_loop * 80) /2
                                
                            finalaffc=0
                            finalqty=0
                            if(ciptankflow<=1200):
                                finalaffc=ciptankflow
                                finalqty = 1
                            else:
                                finalaffc=ciptankflow/1200
                                finalaffc = int(-1 * finalaffc // 1 * -1)
                                finalqty = finalaffc
                                finalaffc = ciptankflow/finalaffc
                            addflow=float(finalaffc +1000)
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='"+str(finalaffc)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    ciptank.append(g.base_rate)
                            
                            if(ciptank and i.modules_per_loop>0):
                                self.append('mf_table', {
                                    "item_description":"CIP TANK",
                                    "flow":finalaffc,
                                    "w_qty":finalqty,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * finalqty)
                                })
                            else:
                                self.append('mf_table', {
                                    "item_description":"CIP TANK",
                                    "flow":finalaffc,
                                    "w_qty":finalqty,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP FRAME"):
                            for i in self.mf_table:
                                pp=''
                                if(i.item_description== "CIP TANK"):
                                    if(i.flow>0 and i.flow<=180):
                                        pp="180 LITRES TANK FRAME"
                                    elif(i.flow>180 and i.flow<=250):
                                        pp="250 LITRES TANK FRAME"
                                    elif(i.flow>250 and i.flow<=450):
                                        pp="450 LITRES TANK FRAME"
                                    elif(i.flow>450 and i.flow<=1200):
                                        pp="1200 LITRES TANK FRAME"
                                    elif(i.flow>1200):
                                        pp="1200 LITRES TANK FRAME"
                                    price_ar=[]
                                    for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='"+str(pp)+"'",as_dict=1):
                                        for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                            price_ar.append(rate.base_rate)
                                    self.append('mf_table', {
                                        "item_description":"CIP FRAME",
                                        "flow":i.flow,
                                        "w_qty":i.w_qty,
                                        "unit_price":sum(price_ar),
                                        "total_price" : sum(price_ar) * i.w_qty
                                    })
                        elif(k=="CIP DOSING TANK-1"):
                            cipdosetank=[]
                            addflow=1050
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='50' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                                    if(g.base_rate>0):
                                        cipdosetank.append(g.base_rate)
                            dtnk1=50
                            if(cipdosetank):
                                self.append('mf_table', {
                                    "item_description":"CIP DOSING TANK-1",
                                    "flow":dtnk1,
                                    "w_qty":1,
                                    "unit_price":cipdosetank[0],
                                    "total_price" : (cipdosetank[0] * 1)
                                })
                            else:
                                self.append('mf_table', {
                                    "item_description":"CIP DOSING TANK-1",
                                    "flow":dtnk1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING TANK-2"):
                            cipdosetank=[]
                            addflow=1050
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='50' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                                    if(g.base_rate>0):
                                        cipdosetank.append(g.base_rate)
                            dtnk1=50
                            if(cipdosetank):
                                self.append('mf_table', {
                                    "item_description":"CIP DOSING TANK-2",
                                    "flow":dtnk1,
                                    "w_qty":1,
                                    "unit_price":cipdosetank[0],
                                    "total_price" : (cipdosetank[0] * 1)
                                })
                            else:
                                self.append('mf_table', {
                                    "item_description":"CIP DOSING TANK-2",
                                    "flow":dtnk1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING TANK-3"):
                            cipdosetank=[]
                            addflow=1050
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='50' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                                    if(g.base_rate>0):
                                        cipdosetank.append(g.base_rate)
                            dtnk1=50
                            if(cipdosetank):
                                self.append('mf_table', {
                                    "item_description":"CIP DOSING TANK-3",
                                    "flow":dtnk1,
                                    "w_qty":1,
                                    "unit_price":cipdosetank[0],
                                    "total_price" : (cipdosetank[0] * 1)
                                })
                            else:
                                self.append('mf_table', {
                                    "item_description":"CIP DOSING TANK-3",
                                    "flow":dtnk1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP TANK FRAME"):
                            price_ar=[]
                            for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='180 LITRES TANK FRAME'",as_dict=1):
                                for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    price_ar.append(rate.base_rate)
                            self.append('mf_table', {
                                "item_description":"CIP DOSING TANK-1 FRAME",
                                "flow":50,
                                "w_qty":1,
                                "unit_price":sum(price_ar),
                                "total_price" : sum(price_ar)
                            })
                            self.append('mf_table', {
                                "item_description":"CIP DOSING TANK-2 FRAME",
                                "flow":50,
                                "w_qty":1,
                                "unit_price":sum(price_ar),
                                "total_price" : sum(price_ar)
                            })
                            self.append('mf_table', {
                                "item_description":"CIP DOSING TANK-3 FRAME",
                                "flow":50,
                                "w_qty":1,
                                "unit_price":sum(price_ar),
                                "total_price" : sum(price_ar)
                            })
                        elif(k=="MF SKID FRAME"):
                            price_ar=[]
                            for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='"+str(k)+"' ",as_dict=1):
                                for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty*self.flow/1000)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    price_ar.append(rate.base_rate)
                            self.append('mf_table', {
                                    "item_description":"MF SKID FRAME",
                                    "flow":self.flow/1000,
                                    "w_qty":1,
                                    "unit_price":sum(price_ar),
                                    "total_price" : sum(price_ar)
                                })
                        elif(k=="CIP DOSING TANK FRAME"):
                            cipf=[]
                            for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='LANISOSS30440X403MM' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                                if(g.base_rate>0):
                                    cipf.append(g.base_rate)
                            w_qty1=0
                            w_qty2=0
                            w_qty3=0
                            w_qty4=0
                            for vs in self.mf_table:
                                if(vs.item_description == "CIP DOSING PUMP-1"):
                                    w_qty1 = vs.w_qty * 2.5
                                elif(vs.item_description == "CIP DOSING PUMP-2"):
                                    w_qty2 = vs.w_qty * 2.5
                                elif(vs.item_description == "CIP DOSING PUMP-3"):
                                    w_qty3 = vs.w_qty * 2.5
                            self.append('mf_table', {
                                "item_description":"CIP DOSING PUMP-1 FRAME",
                                "flow":50,
                                "w_qty":w_qty1,
                                "unit_price":cipf[0],
                                "total_price" : cipf[0] * w_qty1
                            })
                            self.append('mf_table', {
                                "item_description":"CIP DOSING PUMP-2 FRAME",
                                "flow":50,
                                "w_qty":w_qty2,
                                "unit_price":cipf[0],
                                "total_price" : cipf[0] * w_qty2
                            })
                            self.append('mf_table', {
                                "item_description":"CIP DOSING PUMP-3 FRAME",
                                "flow":50,
                                "w_qty":w_qty3,
                                "unit_price":cipf[0],
                                "total_price" : cipf[0] * w_qty3
                            })
                        if('Sulphur Black Removal System' in selected_s):
                            if(k == "SULPHUR BLACK DOSING PUMP"):
                                sbdp_rate=[0]
                                mffl=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mf_dosing_pump")
                                mf_qt=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mf_dosing_pump_quanity_working")
                                mf_qt2=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mf_dosing_pump_quanity_standby")
                                for kkk in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='DOSING PUMP' and flow>='"+str(mffl)+"' ORDER BY flow ASC LIMIT 1 ",as_dict=1):
                                    get_rate_from_po = frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(kkk.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                    if(get_rate_from_po):
                                        for g in get_rate_from_po:
                                            sbdp_rate.append(g.base_rate)
                                if(sbdp_rate):
                                    self.append('mf_table', {
                                        "item_description":"SULPHUR BLACK DOSING PUMP",
                                        "flow":round(mffl,2),
                                        "w_qty":mf_qt,
                                        "ssb_qty":mf_qt2,
                                        "unit_price":sbdp_rate[0],
                                        "total_price" : sbdp_rate[0]*(mf_qt+mf_qt2)
                                    })
                                else:
                                    self.append('mf_table', {
                                        "item_description":"SULPHUR BLACK DOSING PUMP",
                                        "flow":round(mffl,2),
                                        "w_qty":mf_qt,
                                        "ssb_qty":mf_qt2,
                                        "unit_price":0,
                                        "total_price" : 0
                                    })
                                    
                                sulcip=[]
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='LANISOSS30440X403MM' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                                    if(g.base_rate>0):
                                        sulcip.append(g.base_rate)
                                for vs in self.mf_table:
                                    if(vs.item_description == "SULPHUR BLACK DOSING PUMP"):
                                        w_qty1 = vs.w_qty * 2.5
                                self.append('mf_table', {
                                    "item_description":"SULPHUR BLACK DOSING PUMP FRAME",
                                    "flow":round(mffl,2),
                                    "w_qty":w_qty1,
                                    "unit_price":sulcip[0],
                                    "total_price" : sulcip[0] * w_qty1
                                })
                                cipdosetank=[]
                                addflow=((round(mffl,2) * 22) + 1000)
                                for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='"+str(round(mffl,2) * 22)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                                        if(g.base_rate>0):
                                            cipdosetank.append(g.base_rate)
                                dtnk1=round(mffl,2) * 22
                                if(cipdosetank):
                                    self.append('mf_table', {
                                        "item_description":"SULPHUR BLACK DOSING TANK",
                                        "flow":dtnk1,
                                        "w_qty":1,
                                        "unit_price":cipdosetank[0],
                                        "total_price" : (cipdosetank[0] * 1)
                                    })
                                else:
                                    self.append('mf_table', {
                                        "item_description":"SULPHUR BLACK DOSING TANK",
                                        "flow":dtnk1,
                                        "w_qty":1,
                                        "unit_price":0,
                                        "total_price" : 0
                                    })
                                price_ar=[]
                                if(dtnk1>0 and dtnk1<=180):
                                    pp="180 LITRES TANK FRAME"
                                elif(dtnk1>180 and dtnk1<=250):
                                    pp="250 LITRES TANK FRAME"
                                elif(dtnk1>250 and dtnk1<=450):
                                    pp="450 LITRES TANK FRAME"
                                elif(dtnk1>450 and dtnk1<=1200):
                                    pp="1200 LITRES TANK FRAME"
                                elif(dtnk1>1200):
                                    pp="1200 LITRES TANK FRAME"
                                else:
                                    pp='1200'
                                for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='"+str(pp)+"'",as_dict=1):
                                    for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        price_ar.append(rate.base_rate)
                                if(price_ar):
                                    self.append('mf_table', {
                                        "item_description":"SULPHUR BLACK DOSING TANK FRAME",
                                        "flow":round(mffl,2) * 22,
                                        "w_qty":1,
                                        "unit_price":sum(price_ar),
                                        "total_price" : sum(price_ar)
                                    })
                                else:
                                    self.append('mf_table', {
                                        "item_description":"SULPHUR BLACK DOSING TANK FRAME",
                                        "flow":round(mffl,2) * 22,
                                        "w_qty":1,
                                        "unit_price":0,
                                        "total_price" : 0
                                    })
                                    
                                
                            elif(k=="SULPHUR BLACK SLUDGE PUMP"):
                                sbsp_rate=[]
                                mbrfl=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mf_sludge_pump_capacity")
                                mbr_qt=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mf_sludge_pump_quanity_working")
                                mbr_qt2=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mf_sludge_pump_quanity_standby")
                                for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and range1>=1  and flow>='"+str(mbrfl)+"' and flow<='"+str(float(mbrfl) + 10)+"'",as_dict=1):
                                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate`,`tabPurchase Order Item`.`parent`,`tabPurchase Order Item`.`item_code` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        sbsp_rate.append(g.base_rate)
                                if(sbsp_rate):
                                    self.append('mf_table', {
                                        "item_description":"SULPHUR BLACK SLUDGE PUMP",
                                        "flow":round(mbrfl,2),
                                        "range":1,
                                        "w_qty":mbr_qt,
                                        "sb_qty":mbr_qt2,
                                        "unit_price":sbsp_rate[0],
                                        "total_price" : sbsp_rate[0]*(mbr_qt+mbr_qt2)
                                    })
                            elif(k=="SULPHUR BLACK LAMELLA SETTLER"):
                                mffl=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mf_lamella_settler")
                                tank_he = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"tank_height")
                                lamella= (mffl*4)/2.5
                                self.append('mf_table', {
                                    "item_description":"SULPHUR BLACK LAMELLA SETTLER",
                                    "flow":mffl,
                                    "range":1,
                                    "w_qty":lamella,
                                    "unit_price":7600,
                                    "total_price" : 7600 * lamella
                                })
                #mbr
                mbr = ["MBR MODULES","BACKWASH PUMP", "CIP PUMP", "PERMEATE/BACKWASH/CIP PUMP"]
                # if(self.is_rewolutte==1):
                #     mbr.append("CONDUCTIVITY SENSOR")
                self.mbr_koch_table = []
                dtnk1=0
                dtnk2=0
                for i in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    if(i.mbr_type == 'SUB-UF'):
                        mbr.append("SLUDGE EXTRACT PUMP")
                    else:
                        mbr.append("SLUDGE RECIRCULATION PUMP")
                    mbr.extend(["MBR BLOWER","SULPHUR BLACK SLUDGE PUMP", "SULPHUR BLACK DOSING PUMP", "SULPHUR BLACK LAMELLA SETTLER", "LEVEL TRANSMITTER", "LEVEL FLOAT", "ELECTROMAGNETIC FLOWMETER", "PRESSURE TRANSMITTER", "PRESSURE GAUGE","CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3","CIP DOSING PUMP FRAME","CIP DOSING TANK-1", "CIP DOSING TANK-2", "MBR SKID FRAME","CIP DOSING TANK FRAME"])
                    for k in mbr:
                        if(k == "MBR MODULES"):
                            if(i.mbr_model =='PSH 330-8'):
                                # rr=1327306.4
                                rr=(15000+1000)*1.1*(self.usd+2)
                            elif(i.mbr_model =='PSH 660-16'):
                                # rr=2696091.13
                                rr=(31000+1000)*1.1*(self.usd+2)
                            elif(i.mbr_model =='PSH 1800-36'):
                                # rr=4894442.35
                                rr=(58000+1000)*1.1*(self.usd+2)
                            elif(i.mbr_model =='PSH 1800-40'):
                                # rr=5226268.95
                                rr=(62000+1000)*1.1*(self.usd+2)
                            elif(i.mbr_model =='PSH 1800-44'):
                                # rr=5475138.9
                                rr=(65000+1000)*1.1*(self.usd+2)
                            else:
                                rr=0
                                
                            self.append('mbr_koch_table', {
                                "item_description":"MBR MODULES",
                                "flow":0,
                                "range":i.mbr_model,
                                "w_qty":i.design_total_no_of_modules,
                                "unit_price":rr,
                                "total_price" : (rr * i.design_total_no_of_modules)
                            })
                        elif(k=="FEED PUMP"):
                            if(i.is_mbr_feed_pump_required == 1):
                                mbrfeed=[]
                                addflow=float(i.mbr_feed_pump) + 10
                                for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and flow>='"+str(i.mbr_feed_pump)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        mbrfeed.append(g.base_rate)
                                
                                if(mbrfeed and i.mbr_feed_pump>0):
                                    self.append('mbr_koch_table', {
                                        "item_description":"FEED PUMP",
                                        "flow":i.mbr_feed_pump,
                                        "w_qty":i.feed_pump_qty,
                                        "unit_price":g.base_rate,
                                        "total_price" : (g.base_rate * i.feed_pump_qty)
                                    })
                                else:
                                    self.append('mbr_koch_table', {
                                        "item_description":"FEED PUMP",
                                        "flow":i.mbr_feed_pump,
                                        "w_qty":i.feed_pump_qty,
                                        "unit_price":0,
                                        "total_price" : 0
                                    })
                            else:
                                self.append('mbr_koch_table', {
                                        "item_description":"FEED PUMP",
                                        "flow":0,
                                        "w_qty":0,
                                        "unit_price":0,
                                        "total_price" : 0
                                    })
                        elif(k=="PERMEATE/BACKWASH/CIP PUMP"):
                            mbrper=[]
                            addflow=float(i.mbr_backwash_pump)+10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and flow>='"+str(i.mbr_backwash_pump)+"' and range1>=1.2 order by flow ASC",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                                    mbrper.append(g.base_rate)
                            
                            if(mbrper and i.mbr_backwash_pump>0):
                                self.append('mbr_koch_table', {
                                    "item_description":"PERMEATE/BACKWASH/CIP PUMP",
                                    "flow":i.mbr_backwash_pump,
                                    "range":1.2,
                                    "w_qty":i.pump_qty,
                                    "ssb_qty":i.permeate_backwash_store_standby_qty,
                                    "unit_price":mbrper[0],
                                    "total_price" : (mbrper[0] * (i.pump_qty + i.permeate_backwash_store_standby_qty))
                                })
                            else:
                                self.append('mbr_koch_table', {
                                    "item_description":"PERMEATE/BACKWASH/CIP PUMP",
                                    "flow":i.mbr_backwash_pump,
                                    "range":1.2,
                                    "w_qty":i.pump_qty,
                                    "ssb_qty":i.permeate_backwash_store_standby_qty,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="MBR BLOWER"):
                            motor_cost=0
                            mbr_blower_flow=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbr_blower__train1")
                            flow3min = mbr_blower_flow * 0.588578
                            mbr_range = 0.45
                            inchh2 = mbr_range * 401.865
                            power = ((flow3min * inchh2)/(6356 * 0.67))/1.34
                            if(power<=0.045): kw=0.045; 
                            elif(power<=0.18): kw=0.18; 
                            elif(power<=0.37): kw=0.37; motor_cost=9622; 
                            elif(power<=0.55): kw=0.55; motor_cost=10476; 
                            elif(power<=0.75): kw=0.75; motor_cost=11117; 
                            elif(power<=1.1): kw=1.1; motor_cost=12078; 
                            elif(power<=1.5): kw=1.5; motor_cost=13547; 
                            elif(power<=2.2): kw=2.2; motor_cost=15789; 
                            elif(power<=3.7): kw=3.7; motor_cost=21503; 
                            elif(power<=4): kw=4; motor_cost=24888; 
                            elif(power<=5.5): kw=5.5; motor_cost=30800; 
                            elif(power<=7.5): kw=7.5; motor_cost=52931; 
                            elif(power<=11): kw=11; motor_cost=53813; 
                            elif(power<=15): kw=15; motor_cost=74261; 
                            elif(power<=18.5): kw=18.5; motor_cost=83169; 
                            elif(power<=22): kw=22; motor_cost=104988; 
                            elif(power<=30): kw=30; motor_cost=119441; 
                            elif(power<=37): kw=37; motor_cost=170992; 
                            elif(power<=45): kw=45; motor_cost=249535; 
                            elif(power<=55): kw=55; motor_cost=286980; 
                            elif(power<=75): kw=75; motor_cost=330045; 
                            elif(power<=90): kw=90; motor_cost=387308; 
                            elif(power<=110): kw=110; motor_cost=471705; 
                            elif(power<=160): kw=160; motor_cost=516345;
                            self.append('mbr_koch_table', {
                                    "item_description":"MBR BLOWER",
                                    "flow":i.mbr_blower__train1,
                                    "range":0.45,
                                    "w_qty":1,
                                    "sb_qty":1,
                                    "unit_price":0,
                                    "motor_cost":motor_cost*2,
                                    "total_price" : 0+(motor_cost*2)
                                })
                        elif(k=="SLUDGE EXTRACT PUMP"):
                            mbrsld=[]
                            if(i.mbr_sludge_pump>0):
                                addflow=float(i.mbr_sludge_pump) + 10
                            else:
                                addflow=float(i.mbr_sludge_pump)
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and range1>=1 and flow>='"+str(i.mbr_sludge_pump)+"' and flow<='"+str(addflow)+"' ORDER BY flow ASC",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrsld.append(g.base_rate)
                            mbrsb=0
                            if(i.mbr_sludge_pump>=1):
                                mbrsb=i.sludge_pump_sb_qty
                            if(mbrsld and i.mbr_sludge_pump>0):
                                self.append('mbr_koch_table', {
                                    "item_description":"SLUDGE EXTRACT PUMP",
                                    "flow":i.mbr_sludge_pump,
                                    "range":1,
                                    "w_qty":i.mbr_sludge_pump_qty,
                                    "sb_qty":mbrsb,
                                    "unit_price":g.base_rate,
                                    "total_price" : g.base_rate * (i.blower_pump_qty + mbrsb)
                                })
                            else:
                                self.append('mbr_koch_table', {
                                    "item_description":"SLUDGE EXTRACT PUMP",
                                    "flow":i.mbr_sludge_pump,
                                    "range":1,
                                    "w_qty":i.mbr_sludge_pump_qty,
                                    "sb_qty":mbrsb,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="SLUDGE RECIRCULATION PUMP"):
                            mbrrec=[]
                            addflow=float(i.mbr_circulation_pump)
                            if(addflow>0):
                                for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and range1>=0.5 and flow>='"+str(i.mbr_circulation_pump)+"' and flow<='"+str(addflow)+"' ORDER BY flow ASC",as_dict=1):
                                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        mbrrec.append(g.base_rate)
                            mbrrecsb=0
                            if(i.mbr_circulation_pump>=1 or i.circulation_pump_qty>=1):
                                mbrrecsb=i.mbr_circ_sb_qty
                            mbrwqty=i.circulation_pump_qty
                            mbrssbqty=0
                            if(i.mbr_type == "SUB-UF"):
                                mbrwqty=i.mbr_sludge_pump_qty
                                mbrssbqty=i.circulation_pump_store_standby_qty
                            if(mbrrec and i.mbr_circulation_pump>0):
                                self.append('mbr_koch_table', {
                                    "item_description":"SLUDGE RECIRCULATION PUMP",
                                    "flow":i.mbr_circulation_pump,
                                    "range":0.5,
                                    "w_qty":mbrwqty,
                                    "sb_qty":mbrrecsb,
                                    "ssb_qty":mbrssbqty,
                                    "unit_price":mbrrec[0],
                                    "total_price" : mbrrec[0] * (mbrwqty + mbrrecsb + mbrssbqty)
                                })
                            else:
                                self.append('mbr_koch_table', {
                                    "item_description":"SLUDGE RECIRCULATION PUMP",
                                    "flow":i.mbr_circulation_pump,
                                    "range":0.5,
                                    "w_qty":mbrwqty,
                                    "sb_qty":mbrrecsb,
                                    "ssb_qty":mbrssbqty,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING PUMP-1"):
                            mbrcip=[]
                            cipflow = i.dosing_pump_mc
                            addflow=float(cipflow) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='DOSING PUMP' and flow>='"+str(cipflow)+"' and flow<='"+str(addflow)+"'  ORDER BY flow ASC",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrcip.append(g.base_rate)
                            
                            if(mbrcip and cipflow>0):
                                self.append('mbr_koch_table', {
                                    "item_description":"CIP DOSING PUMP-1",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":mbrcip[0],
                                    "total_price" : (mbrcip[0] * 2)
                                })
                            else:
                                self.append('mbr_koch_table', {
                                    "item_description":"CIP DOSING PUMP-1",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING PUMP-2"):
                            mbrcip2=[]
                            cipflow2 = i.dosing_pump_rc
                            addflow=float(cipflow2) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='DOSING PUMP' and flow>='"+str(cipflow2)+"' and flow<='"+str(addflow)+"'  ORDER BY flow ASC",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrcip2.append(g.base_rate)
                            
                            if(mbrcip2 and cipflow2>0):
                                self.append('mbr_koch_table', {
                                    "item_description":"CIP DOSING PUMP-2",
                                    "flow":cipflow2,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 2)
                                })
                            else:
                                self.append('mbr_koch_table', {
                                    "item_description":"CIP DOSING PUMP-2",
                                    "flow":cipflow2,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING PUMP-3"):
                            mbrcip3=[]
                            cipflow3 = i.citric_dosing_pump_mc_and_rc
                            addflow=float(cipflow3) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='DOSING PUMP' and flow>='"+str(cipflow3)+"' and flow<='"+str(addflow)+"'  ORDER BY flow ASC",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrcip3.append(g.base_rate)
                            
                            if(mbrcip3 and cipflow3>0):
                                self.append('mbr_koch_table', {
                                    "item_description":"CIP DOSING PUMP-3",
                                    "flow":cipflow3,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 2)
                                })
                            else:
                                self.append('mbr_koch_table', {
                                    "item_description":"CIP DOSING PUMP-3",
                                    "flow":cipflow3,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k == "LEVEL TRANSMITTER"):
                            lvltran=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='LEVEL TRANSMITTER' ",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    lvltran.append(g.base_rate)
                            
                            if(lvltran):
                                self.append('mbr_koch_table', {
                                    "item_description":"LEVEL TRANSMITTER",
                                    "flow":1,
                                    "range":i.tank_height,
                                    "w_qty":i.design_no_of_trains,
                                    "unit_price":lvltran[0],
                                    "total_price" : (lvltran[0] * i.design_no_of_trains)
                                })
                            else:
                                self.append('mbr_koch_table', {
                                    "item_description":"LEVEL TRANSMITTER",
                                    "flow":1,
                                    "range":i.tank_height,
                                    "w_qty":i.design_no_of_trains,
                                    "unit_price":0,
                                    "total_price":0
                                })   
                        elif(k == "LEVEL FLOAT"):
                            lvlfloat=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='LEVEL FLOAT' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    lvlfloat.append(g.base_rate)
                                    
                            if(lvlfloat):
                                self.append('mbr_koch_table', {
                                    "item_description":"LEVEL FLOAT",
                                    "flow":1,
                                    "w_qty":1,
                                    "unit_price":lvlfloat[0],
                                    "total_price" : (lvlfloat[0] * 1)
                                })
                            else:
                                self.append('mbr_koch_table', {
                                    "item_description":"LEVEL FLOAT",
                                    "flow":1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="ELECTROMAGNETIC FLOWMETER"):
                            elm=[]
                            addflow=float(i.mbr_backwash_pump) +20
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='ELECTROMAGNETIC FLOWMETER' and flow>='"+str(i.mbr_backwash_pump)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    elm.append(g.base_rate)
                            
                            if(elm and i.mbr_backwash_pump>0):
                                self.append('mbr_koch_table', {
                                    "item_description":"ELECTROMAGNETIC FLOWMETER",
                                    "flow":i.mbr_backwash_pump,
                                    "w_qty":i.design_no_of_trains,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * i.design_no_of_trains)
                                })
                            else:
                                self.append('mbr_koch_table', {
                                    "item_description":"ELECTROMAGNETIC FLOWMETER",
                                    "flow":i.mbr_backwash_pump,
                                    "w_qty":i.design_no_of_trains,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k == "PRESSURE TRANSMITTER"):
                            pressure=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='PRESSURE TRANSMITTER' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    pressure.append(g.base_rate)
                                    
                            if(pressure):
                                self.append('mbr_koch_table', {
                                    "item_description":"PRESSURE TRANSMITTER",
                                    "flow":1,
                                    "w_qty":(i.design_no_of_trains + 1),
                                    "unit_price":pressure[0],
                                    "total_price" : (pressure[0] * (i.design_no_of_trains + 1))
                                })
                            else:
                                self.append('mbr_koch_table', {
                                    "item_description":"PRESSURE TRANSMITTER",
                                    "flow":1,
                                    "w_qty":(i.design_no_of_trains + 1),
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k == "PRESSURE GAUGE"):
                            pressure=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='PRESSURE GAUGE' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    pressure.append(g.base_rate)
                                    
                            if(pressure):
                                self.append('mbr_koch_table', {
                                    "item_description":"PRESSURE GAUGE",
                                    "flow":1,
                                    "w_qty":(i.design_no_of_trains + 1),
                                    "unit_price":pressure[0],
                                    "total_price" : (pressure[0] * (i.design_no_of_trains + 1))
                                })
                            else:
                                self.append('mbr_koch_table', {
                                    "item_description":"PRESSURE GAUGE",
                                    "flow":1,
                                    "w_qty":(i.design_no_of_trains + 1),
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING TANK-1"):
                            cipdosetank=[]
                            tnk1 = i.dosing_pump_rc *2
                            addflow=tnk1+1000
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='"+str(tnk1)+"' and flow<='"+str(addflow)+"' ORDER BY flow ASC",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    cipdosetank.append(g.base_rate)
                            dtnk1=tnk1
                            if(cipdosetank and tnk1>0):
                                self.append('mbr_koch_table', {
                                    "item_description":"CIP DOSING TANK-1",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":cipdosetank[0],
                                    "total_price" : (cipdosetank[0] * 1)
                                })
                            else:
                                self.append('mbr_koch_table', {
                                    "item_description":"CIP DOSING TANK-1",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })  
                        elif(k=="CIP DOSING TANK-2"):
                            cipdosetank=[]
                            tnk1 = i.citric_dosing_pump_mc_and_rc *3
                            addflow=tnk1+1000
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='"+str(tnk1)+"' and flow<='"+str(addflow)+"' ORDER BY flow ASC",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    cipdosetank.append(g.base_rate)
                            dtnk2=tnk1
                            if(cipdosetank and tnk1>0):
                                self.append('mbr_koch_table', {
                                    "item_description":"CIP DOSING TANK-2",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":cipdosetank[0],
                                    "total_price" : (cipdosetank[0] * 1)
                                })
                            else:
                                self.append('mbr_koch_table', {
                                    "item_description":"CIP DOSING TANK-2",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP SKID FRAME"):
                            cip_flow_query=frappe.db.sql("select flow from `tabRO Items` where parent='"+str(self.choose_ro_template)+"' and item_description='CIP-1 TANK' ",as_dict=1)
                            cip_flow=0
                            
                            if(cip_flow_query):
                                cip_flow=cip_flow_query[0].flow
                            bom_for_cip='none'
                            if(float(cip_flow)>0 and float(cip_flow)<=180):
                                bom_for_cip='180 LITRES TANK FRAME'
                            elif(float(cip_flow)>180 and float(cip_flow)<=250):
                                bom_for_cip='250 LITRES TANK FRAME'
                            elif(float(cip_flow)>250 and float(cip_flow)<=450):
                                bom_for_cip='450 LITRES TANK FRAME'
                            elif(float(cip_flow)>450 and float(cip_flow)):
                                bom_for_cip='1200 LITRES TANK FRAME'
                            if(bom_for_cip!='none'):
                                price_ar=[]
                                for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='"+str(bom_for_cip)+"' ",as_dict=1):
                                    for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        price_ar.append(rate.base_rate)
                                self.append('mbr_koch_table', {
                                    "item_description":"CIP SKID FRAME",
                                    "flow":cip_flow,
                                    "w_qty":1,
                                    "unit_price":sum(price_ar),
                                    "total_price" : sum(price_ar)
                                })
                            else:
                                self.append('mbr_koch_table', {
                                    "item_description":"CIP SKID FRAME",
                                    "flow":1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING PUMP FRAME"):
                            cipf=[]
                            for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='LANISOSS30440X403MM' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                                if(g.base_rate>0):
                                    cipf.append(g.base_rate)
                            w_qty1=0
                            w_qty2=0
                            w_qty3=0
                            w_qty4=0
                            for vs in self.mbr_koch_table:
                                if(vs.item_description == "CIP DOSING PUMP-1"):
                                    w_qty1 = vs.w_qty * 2.5
                                elif(vs.item_description == "CIP DOSING PUMP-2"):
                                    w_qty2 = vs.w_qty * 2.5
                                elif(vs.item_description == "CIP DOSING PUMP-3"):
                                    w_qty3 = vs.w_qty * 2.5
                            self.append('mbr_koch_table', {
                                "item_description":"CIP DOSING PUMP-1 FRAME",
                                "flow":50,
                                "w_qty":w_qty1,
                                "unit_price":cipf[0],
                                "total_price" : cipf[0] * w_qty1
                            })
                            self.append('mbr_koch_table', {
                                "item_description":"CIP DOSING PUMP-2 FRAME",
                                "flow":50,
                                "w_qty":w_qty2,
                                "unit_price":cipf[0],
                                "total_price" : cipf[0] * w_qty2
                            })
                            self.append('mbr_koch_table', {
                                "item_description":"CIP DOSING PUMP-3 FRAME",
                                "flow":50,
                                "w_qty":w_qty3,
                                "unit_price":cipf[0],
                                "total_price" : cipf[0] * w_qty3
                            })
                        elif(k=="CIP DOSING TANK FRAME"):
                            price_ar=[]
                            for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='250 LITRES TANK FRAME'",as_dict=1):
                                for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    price_ar.append(rate.base_rate)
                            if(dtnk1>250):
                                self.append('mbr_koch_table', {
                                    "item_description":"CIP DOSING TANK-1 FRAME",
                                    "flow":250,
                                    "w_qty":1,
                                    "unit_price":sum(price_ar),
                                    "total_price" : sum(price_ar)
                                })
                            if(dtnk2>250):
                                self.append('mbr_koch_table', {
                                    "item_description":"CIP DOSING TANK-2 FRAME",
                                    "flow":250,
                                    "w_qty":1,
                                    "unit_price":sum(price_ar),
                                    "total_price" : sum(price_ar)
                                })
                        if('Sulphur Black Removal System' in selected_s):
                            if(k=="SULPHUR BLACK SLUDGE PUMP"):
                                sbsp_rate=[]
                                mbrfl=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbr_sludge_pump_capacity")
                                mbr_qt=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbr_sludge_pump_quanity_working")
                                mbr_qt2=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbr_sludge_pump_quanity_standby")
                                for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and range1>=1  and flow>='"+str(mbrfl)+"' and flow<='"+str(float(mbrfl) + 10)+"'",as_dict=1):
                                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate`,`tabPurchase Order Item`.`parent`,`tabPurchase Order Item`.`item_code` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        sbsp_rate.append(g.base_rate)
                                if(sbsp_rate):
                                    self.append('mbr_koch_table', {
                                        "item_description":"SULPHUR BLACK SLUDGE PUMP",
                                        "flow":round(mbrfl,2),
                                        "range":1,
                                        "w_qty":mbr_qt,
                                        "sb_qty":mbr_qt2,
                                        "unit_price":sbsp_rate[0],
                                        "total_price" : sbsp_rate[0]*(mbr_qt+mbr_qt2)
                                    })
                            
                            elif(k=="SULPHUR BLACK DOSING PUMP"):
                                sbdp_rate=[0]
                                mbrfl=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbr_dosing_pump")
                                mbr_qt=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbr_dosing_pump_quanity_working")
                                mbr_qt2=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbr_dosing_pump_quanity_standby")
                                
                                for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and range1>=1  and flow>='"+str(mbrfl)+"' and flow<='"+str(float(mbrfl) + 10)+"'",as_dict=1):
                                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate`,`tabPurchase Order Item`.`parent`,`tabPurchase Order Item`.`item_code` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        sbsp_rate.append(g.base_rate)
                                if(sbsp_rate):
                                    self.append('mbr_koch_table', {
                                        "item_description":"SULPHUR BLACK DOSING PUMP",
                                        "flow":round(mbrfl,2),
                                        "range":1,
                                        "w_qty":mbr_qt,
                                        "sb_qty":mbr_qt2,
                                        "unit_price":sbsp_rate[0],
                                        "total_price" : sbsp_rate[0]*(mbr_qt+mbr_qt2)
                                    })
                                sulcip=[]
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='LANISOSS30440X403MM' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                                    if(g.base_rate>0):
                                        sulcip.append(g.base_rate)
                                for vs in self.mbr_koch_table:
                                    if(vs.item_description == "SULPHUR BLACK DOSING PUMP"):
                                        w_qty1 = vs.w_qty * 2.5
                                self.append('mbr_koch_table', {
                                    "item_description":"SULPHUR BLACK DOSING PUMP FRAME",
                                    "flow":round(mbrfl,2),
                                    "w_qty":w_qty1,
                                    "unit_price":sulcip[0],
                                    "total_price" : sulcip[0] * w_qty1
                                })
                                cipdosetank=[]
                                addflow=(round(mbrfl,2) * 22) + 1000
                                for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='"+str((round(mbrfl,2) * 22))+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                                        if(g.base_rate>0):
                                            cipdosetank.append(g.base_rate)
                                dtnk1=(round(mbrfl,2) * 22)
                                if(cipdosetank):
                                    self.append('mbr_koch_table', {
                                        "item_description":"SULPHUR BLACK DOSING TANK",
                                        "flow":dtnk1,
                                        "w_qty":1,
                                        "unit_price":cipdosetank[0],
                                        "total_price" : (cipdosetank[0] * 1)
                                    })
                                else:
                                    self.append('mbr_koch_table', {
                                        "item_description":"SULPHUR BLACK DOSING TANK",
                                        "flow":dtnk1,
                                        "w_qty":1,
                                        "unit_price":0,
                                        "total_price" : 0
                                    })
                                price_ar=[]
                                if(dtnk1>0 and dtnk1<=180):
                                    pp="180 LITRES TANK FRAME"
                                elif(dtnk1>180 and dtnk1<=250):
                                    pp="250 LITRES TANK FRAME"
                                elif(dtnk1>250 and dtnk1<=450):
                                    pp="450 LITRES TANK FRAME"
                                elif(dtnk1>450 and dtnk1<=1200):
                                    pp="1200 LITRES TANK FRAME"
                                elif(dtnk1>1200):
                                    pp="1200 LITRES TANK FRAME"
                                else:
                                    pp='1200'
                                for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='"+str(pp)+"'",as_dict=1):
                                    for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        price_ar.append(rate.base_rate)
                                self.append('mbr_koch_table', {
                                    "item_description":"SULPHUR BLACK DOSING TANK FRAME",
                                    "flow":dtnk1,
                                    "w_qty":1,
                                    "unit_price":sum(price_ar),
                                    "total_price" : sum(price_ar)
                                })
                                
                            elif(k=="SULPHUR BLACK LAMELLA SETTLER"):
                                mbrfl=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbr_lamella_settler")
                                tank_he = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"tank_height")
                                lamella= (mbrfl*4)/2.5
                                self.append('mbr_koch_table', {
                                    "item_description":"SULPHUR BLACK LAMELLA SETTLER",
                                    "flow":mbrfl,
                                    "range":1,
                                    "w_qty":lamella,
                                    "unit_price":7600,
                                    "total_price" : 7600 * lamella
                                })
                # #mbr_ovivo_cost
                mbr_ovivo = ["MBR MODULES", "TOP PERMEATE MODULE", "BASE MODULE"]
                self.mbr_ovivo_table = []
                dtnk1=0
                dtnk2=0
                dtnk3=0
                for i in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    # if(i.feed_pump_required_for_ovivo == 1):
                    mbr_ovivo.append("FEED PUMP")
                    mbr_ovivo.extend(["PERMEATE PUMP", "BACKWASH/CIP PUMP"])
                    if(i.ovivo_type == 'S-UF'):
                        mbr_ovivo.append("SLUDGE EXTRACT PUMP")
                    else:
                        mbr_ovivo.append("SLUDGE RECIRCULATION PUMP")
                    mbr_ovivo.append("CIP PUMP")
                    mbr_ovivo.extend(["SPRINKLER PUMP","MBR BLOWER","SULPHUR BLACK SLUDGE PUMP","SULPHUR BLACK DOSING PUMP", "SULPHUR BLACK LAMELLA SETTLER", "LEVEL TRANSMITTER", "LEVEL FLOAT", "ELECTROMAGNETIC FLOWMETER","TURBIDITY SENSOR", "PRESSURE TRANSMITTER", "PRESSURE GAUGE","CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3", "CIP DOSING PUMP-4","CIP DOSING PUMP FRAME","CIP DOSING TANK-1", "CIP DOSING TANK-2", "CIP DOSING TANK-3","CIP DOSING TANK FRAME", "PIPES,FITTINGS & VALVES", "FAB. & ERECTION"])
                    for k in mbr_ovivo:
                        if(k=="MBR MODULES"):
                            if(i.ovivo_no_module_required>100):
                                mbr_md_rate = 198000
                            else:
                                mbr_md_rate = 210000
                            self.append('mbr_ovivo_table', {
                                "item_description":"MBR MODULES",
                                "flow":1,
                                "range":0,
                                "w_qty":i.ovivo_no_module_required,
                                "unit_price":mbr_md_rate,
                                "total_price" : (mbr_md_rate * i.ovivo_no_module_required)
                            })
                        elif(k=="TOP PERMEATE MODULE"):
                            mbrovivomodel=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TOP PERMEATE MODULE' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrovivomodel.append(g.base_rate)
                                    
                            if(mbrovivomodel):
                                self.append('mbr_ovivo_table', {
                                        "item_description":"TOP PERMEATE MODULE",
                                        "flow":1,
                                        "range":0,
                                        "w_qty":i.ovivo_no_of_stacks_required,
                                        "unit_price":mbrovivomodel[0],
                                        "total_price" : (mbrovivomodel[0] * i.ovivo_no_of_stacks_required)
                                    })
                            else:
                                self.append('mbr_ovivo_table', {
                                        "item_description":"TOP PERMEATE MODULE",
                                        "flow":1,
                                        "range":0,
                                        "w_qty":i.ovivo_no_of_stacks_required,
                                        "unit_price":0,
                                        "total_price" : 0
                                    })
                        elif(k=="BASE MODULE"):
                            mbrovivomodel=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='BASE MODULE' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrovivomodel.append(g.base_rate)
                                    
                            if(mbrovivomodel):
                                self.append('mbr_ovivo_table', {
                                        "item_description":"BASE MODULE",
                                        "flow":1,
                                        "range":0,
                                        "w_qty":i.ovivo_no_of_stacks_required,
                                        "unit_price":mbrovivomodel[0],
                                        "total_price" : (mbrovivomodel[0] * i.ovivo_no_of_stacks_required)
                                    })
                            else:
                                self.append('mbr_ovivo_table', {
                                        "item_description":"BASE MODULE",
                                        "flow":1,
                                        "range":0,
                                        "w_qty":i.ovivo_no_of_stacks_required,
                                        "unit_price":0,
                                        "total_price" : 0
                                    })
                        elif(k=="FEED PUMP"):
                            if(i.feed_pump_required_for_ovivo == 1):
                                mbrovivofeed=[]
                                addflow=float(i.ovivo_feed_pump) + 10
                                for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and flow>='"+str(i.ovivo_feed_pump)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        mbrovivofeed.append(g.base_rate)
                                
                                if(mbrovivofeed and i.ovivo_feed_pump>0):
                                    self.append('mbr_ovivo_table', {
                                        "item_description":"FEED PUMP",
                                        "flow":i.ovivo_feed_pump,
                                        "w_qty":i.ovivo_feed_qty,
                                        "sb_qty":i.ovivo_feed_sqty,
                                        "unit_price":mbrovivofeed[0],
                                        "total_price" : (mbrovivofeed[0] * (i.ovivo_feed_pump + i.ovivo_feed_qty + i.ovivo_feed_sqty))
                                    })
                                else:
                                    self.append('mbr_ovivo_table', {
                                        "item_description":"FEED PUMP",
                                        "flow":i.ovivo_feed_pump,
                                        "w_qty":i.ovivo_feed_qty,
                                        "sb_qty":i.ovivo_feed_sqty,
                                        "unit_price":0,
                                        "total_price" : 0
                                    })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"FEED PUMP",
                                    "flow":0,
                                    "w_qty":0,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP PUMP"):
                            mbrovivocip=[]
                            addflow=float(i.ovivo_cip) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and flow>='"+str(i.ovivo_cip)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrovivocip.append(g.base_rate)
                            
                            if(mbrovivocip and i.ovivo_cip>0):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP PUMP",
                                    "flow":i.ovivo_cip,
                                    "w_qty":i.ovivo_cip_qty,
                                    "sb_qty":i.ovivo_cip_sqty,
                                    "unit_price":mbrovivocip[0],
                                    "total_price" : (mbrovivocip[0] * (i.ovivo_cip + i.ovivo_cip_qty + i.ovivo_cip_sqty))
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP PUMP",
                                    "flow":i.ovivo_cip,
                                    "w_qty":i.ovivo_cip_qty,
                                    "sb_qty":i.ovivo_cip_sqty,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="PERMEATE PUMP"):
                            mbrper=[]
                            addflow=float(i.ovivo_permeate_pump) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and range1>=1.5 and flow>='"+str(i.ovivo_permeate_pump)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                                    if(g.base_rate>0):
                                        mbrper.append(g.base_rate)
                                        
                            if(mbrper and i.ovivo_permeate_pump>0):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"PERMEATE PUMP",
                                    "flow":i.ovivo_permeate_pump,
                                    "range":1.5,
                                    "w_qty":i.ovivo_permeate_qty,
                                    "sb_qty":i.ovivo_permeate_sqty,
                                    "unit_price":mbrper[0],
                                    "total_price" : (mbrper[0] * (i.ovivo_permeate_qty + i.ovivo_permeate_sqty))
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"PERMEATE PUMP",
                                    "flow":i.ovivo_permeate_pump,
                                    "range":1.5,
                                    "w_qty":i.ovivo_permeate_qty,
                                    "sb_qty":i.ovivo_permeate_sqty,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="BACKWASH/CIP PUMP"):
                            mbrper=[]
                            addflow=float(i.ovivo_bc) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and range1>=1.5 and flow>='"+str(i.ovivo_bc)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrper.append(g.base_rate)
                            
                            if(mbrper and i.ovivo_bc>0):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"BACKWASH/CIP PUMP",
                                    "flow":i.ovivo_bc,
                                    "range":1.5,
                                    "w_qty":i.ovivo_backwash_qty,
                                    "sb_qty":i.ovivo_backwash_sqty,
                                    "unit_price":mbrper[0],
                                    "total_price" : (mbrper[0] * (i.ovivo_backwash_qty + i.ovivo_backwash_sqty))
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"BACKWASH/CIP PUMP",
                                    "flow":i.ovivo_bc,
                                    "range":1.5,
                                    "w_qty":i.ovivo_backwash_qty,
                                    "sb_qty":i.ovivo_backwash_sqty,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="SLUDGE EXTRACT PUMP"):
                            mbrper=[]
                            addflow=float(i.ovivo_sludge_pump) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and range1>=1 and flow>='"+str(i.ovivo_sludge_pump)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrper.append(g.base_rate)
                            
                            if(mbrper and i.ovivo_sludge_pump>0):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"SLUDGE EXTRACT PUMP",
                                    "flow":i.ovivo_sludge_pump,
                                    "range":1,
                                    "w_qty":i.ovivo_sludge_qty,
                                    "sb_qty":i.ovivo_sludge_qty,
                                    "unit_price":mbrper[0],
                                    "total_price" : (mbrper[0] * (i.ovivo_sludge_qty + i.ovivo_sludge_qty))
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"SLUDGE EXTRACT PUMP",
                                    "flow":i.ovivo_sludge_pump,
                                    "range":1,
                                    "w_qty":i.ovivo_sludge_qty,
                                    "sb_qty":i.ovivo_sludge_qty,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="SLUDGE RECIRCULATION PUMP"):
                            mbrper=[]
                            addflow=float(i.ovivo_circulation_pump) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SUBMERSIBLE PUMP' and range1>=1 and flow>='"+str(i.ovivo_circulation_pump)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrper.append(g.base_rate)
                            
                            if(mbrper and i.ovivo_circulation_pump>0):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"SLUDGE RECIRCULATION PUMP",
                                    "flow":i.ovivo_circulation_pump,
                                    "range":1,
                                    "w_qty":i.ovivo_circulation_qty,
                                    "sb_qty":i.ovivo_circulation_sqty,
                                    "unit_price":mbrper[0],
                                    "total_price" : (mbrper[0] * (i.ovivo_circulation_qty + i.ovivo_circulation_sqty))
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"SLUDGE RECIRCULATION PUMP",
                                    "flow":i.ovivo_circulation_pump,
                                    "range":1,
                                    "w_qty":i.ovivo_circulation_qty,
                                    "sb_qty":i.ovivo_circulation_sqty,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="SPRINKLER PUMP"):
                            mbrper=[]
                            addflow=float(i.ovivo_sprinkler_pump) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and range1>=1 and flow>='"+str(i.ovivo_sprinkler_pump)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrper.append(g.base_rate)
                            
                            if(mbrper and i.ovivo_sprinkler_pump>0):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"SPRINKLER PUMP",
                                    "flow":i.ovivo_sprinkler_pump,
                                    "range":1.5,
                                    "w_qty":i.ovivo_sprinkler_qty,
                                    "sb_qty":i.ovivo_sprinkler_qty,
                                    "unit_price":mbrper[0],
                                    "total_price" : (mbrper[0] * (i.ovivo_sprinkler_qty + i.ovivo_sprinkler_qty))
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"SPRINKLER PUMP",
                                    "flow":i.ovivo_sprinkler_pump,
                                    "range":1.5,
                                    "w_qty":i.ovivo_sprinkler_qty,
                                    "sb_qty":i.ovivo_sprinkler_qty,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="MBR BLOWER"):
                            motor_cost=0
                            mbr_blower_flow=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"ovivo_blower")
                            flow3min = mbr_blower_flow * 0.588578
                            mbr_range = 0.45
                            inchh2 = mbr_range * 401.865
                            power = ((flow3min * inchh2)/(6356 * 0.67))/1.34
                            if(power<=0.045): kw=0.045; 
                            elif(power<=0.18): kw=0.18; 
                            elif(power<=0.37): kw=0.37; motor_cost=9622; 
                            elif(power<=0.55): kw=0.55; motor_cost=10476; 
                            elif(power<=0.75): kw=0.75; motor_cost=11117; 
                            elif(power<=1.1): kw=1.1; motor_cost=12078; 
                            elif(power<=1.5): kw=1.5; motor_cost=13547; 
                            elif(power<=2.2): kw=2.2; motor_cost=15789; 
                            elif(power<=3.7): kw=3.7; motor_cost=21503; 
                            elif(power<=4): kw=4; motor_cost=24888; 
                            elif(power<=5.5): kw=5.5; motor_cost=30800; 
                            elif(power<=7.5): kw=7.5; motor_cost=52931; 
                            elif(power<=11): kw=11; motor_cost=53813; 
                            elif(power<=15): kw=15; motor_cost=74261; 
                            elif(power<=18.5): kw=18.5; motor_cost=83169; 
                            elif(power<=22): kw=22; motor_cost=104988; 
                            elif(power<=30): kw=30; motor_cost=119441; 
                            elif(power<=37): kw=37; motor_cost=170992; 
                            elif(power<=45): kw=45; motor_cost=249535; 
                            elif(power<=55): kw=55; motor_cost=286980; 
                            elif(power<=75): kw=75; motor_cost=330045; 
                            elif(power<=90): kw=90; motor_cost=387308; 
                            elif(power<=110): kw=110; motor_cost=471705; 
                            elif(power<=160): kw=160; motor_cost=516345;
                            self.append('mbr_ovivo_table', {
                                    "item_description":"MBR BLOWER",
                                    "flow":i.ovivo_blower,
                                    "range":0.45,
                                    "w_qty":1,
                                    "sb_qty":1,
                                    "unit_price":0,
                                    "motor_cost":motor_cost*2,
                                    "total_price" : 0+(motor_cost*2)
                                })
                        elif(k=="CIP DOSING PUMP-1"):
                            mbrcip=[]
                            cipflow = i.naocl_dosing_pump_rc
                            addflow=float(cipflow) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='DOSING PUMP' and flow>='"+str(cipflow)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrcip.append(g.base_rate)
                            
                            if(mbrcip and cipflow>0):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING PUMP-1",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 2)
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING PUMP-1",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING PUMP-2"):
                            mbrcip=[]
                            cipflow = i.citric_dosing_pump_mc_rc
                            addflow=float(cipflow) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='DOSING PUMP' and flow>='"+str(cipflow)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrcip.append(g.base_rate)
                            
                            if(mbrcip and cipflow>0):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING PUMP-2",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 2)
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING PUMP-2",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING PUMP-3"):
                            mbrcip=[]
                            cipflow = i.hcl_dosing_pump_mc_rc
                            addflow=float(cipflow) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='DOSING PUMP' and flow>='"+str(cipflow)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrcip.append(g.base_rate)
                            if(mbrcip and cipflow>0):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING PUMP-3",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 2)
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING PUMP-3",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING PUMP-4"):
                            mbrcip=[]
                            cipflow = i.alum_dosing_pump_mc_rc
                            addflow=float(cipflow) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='DOSING PUMP' and flow>='"+str(cipflow)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrcip.append(g.base_rate)
                            if(mbrcip and cipflow>0):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING PUMP-4",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 2)
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING PUMP-4",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="TURBIDITY SENSOR"):
                            self.append('mbr_ovivo_table',{
                                "item_description":k,
                                "flow":0,
                                "w_qty":i.ovivo_no_of_trains,
                                "unit_price":250000,
                                "total_price" : 250000*float(i.ovivo_no_of_trains)
                            })
                        elif(k=="LEVEL TRANSMITTER"):
                            lvltran=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='LEVEL TRANSMITTER' ",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    lvltran.append(g.base_rate)
                            
                            
                            if(lvltran):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"LEVEL TRANSMITTER",
                                    "flow":1,
                                    "range":i.tank_height,
                                    "w_qty":i.ovivo_no_of_trains,
                                    "unit_price":lvltran[0],
                                    "total_price" : (lvltran[0] * i.design_no_of_trains)
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"LEVEL TRANSMITTER",
                                    "flow":1,
                                    "range":i.tank_height,
                                    "w_qty":i.ovivo_no_of_trains,
                                    "unit_price":0,
                                    "total_price":0
                                })   
                        elif(k=="LEVEL FLOAT"):
                            lvlfloat=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='LEVEL FLOAT' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    lvlfloat.append(g.base_rate)
                                    
                            if(lvlfloat):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"LEVEL FLOAT",
                                    "flow":1,
                                    "w_qty":3,
                                    "unit_price":lvlfloat[0],
                                    "total_price" : (lvlfloat[0] * 3)
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"LEVEL FLOAT",
                                    "flow":1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="ELECTROMAGNETIC FLOWMETER"):
                            elm=[]
                            addflow=float(i.ovivo_bc) +20
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='ELECTROMAGNETIC FLOWMETER' and flow>='"+str(i.ovivo_bc)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    elm.append(g.base_rate)
                            
                            if(elm and i.ovivo_bc>0):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"ELECTROMAGNETIC FLOWMETER",
                                    "flow":i.ovivo_bc,
                                    "w_qty":(i.ovivo_no_of_trains + i.ovivo_sprinkler_qty + i.ovivo_backwash_qty),
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * (i.ovivo_no_of_trains + i.ovivo_sprinkler_qty + i.ovivo_backwash_qty))
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"ELECTROMAGNETIC FLOWMETER",
                                    "flow":i.ovivo_bc,
                                    "w_qty":(i.ovivo_no_of_trains + i.ovivo_sprinkler_qty + i.ovivo_backwash_qty),
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="PRESSURE TRANSMITTER"):
                            pressure=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='PRESSURE TRANSMITTER' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    pressure.append(g.base_rate)
                                    
                            if(pressure):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"PRESSURE TRANSMITTER",
                                    "flow":1,
                                    "w_qty":(i.ovivo_no_of_trains + i.ovivo_sprinkler_qty + i.ovivo_backwash_qty + i.ovivo_sludge_qty),
                                    "unit_price":pressure[0],
                                    "total_price" : (pressure[0] * (i.ovivo_no_of_trains + i.ovivo_sprinkler_qty + i.ovivo_backwash_qty + i.ovivo_sludge_qty))
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"PRESSURE TRANSMITTER",
                                    "flow":1,
                                    "w_qty":(i.ovivo_no_of_trains + i.ovivo_sprinkler_qty + i.ovivo_backwash_qty + i.ovivo_sludge_qty),
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="PRESSURE GAUGE"):
                            pressure=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='PRESSURE GAUGE' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    pressure.append(g.base_rate)
                                    
                            if(pressure):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"PRESSURE GAUGE",
                                    "flow":1,
                                    "w_qty":(i.ovivo_no_of_trains + i.ovivo_sprinkler_qty + i.ovivo_backwash_qty + i.ovivo_sludge_qty),
                                    "unit_price":pressure[0],
                                    "total_price" : (pressure[0] * (i.ovivo_no_of_trains + i.ovivo_sprinkler_qty + i.ovivo_backwash_qty + i.ovivo_sludge_qty))
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"PRESSURE GAUGE",
                                    "flow":1,
                                    "w_qty":(i.ovivo_no_of_trains + i.ovivo_sprinkler_qty + i.ovivo_backwash_qty + i.ovivo_sludge_qty),
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING TANK-1"):
                            cipdosetank=[]
                            tnk1 = i.naocl_dosing_pump_rc * 1.5
                            addflow=tnk1+1000
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='"+str(tnk1)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    cipdosetank.append(g.base_rate)
                            dtnk1=tnk1
                            if(cipdosetank and tnk1>0):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING TANK-1",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 1)
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING TANK-1",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING TANK-2"):
                            cipdosetank=[]
                            tnk1 = i.citric_dosing_pump_mc_rc *2
                            addflow=tnk1+1000
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='"+str(tnk1)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    cipdosetank.append(g.base_rate)
                            dtnk2=tnk1
                            if(cipdosetank and tnk1>0):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING TANK-2",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 1)
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING TANK-2",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING TANK-3"):
                            cipdosetank=[]
                            tnk1 = i.hcl_dosing_pump_mc_rc *2
                            addflow=tnk1+1000
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='"+str(tnk1)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    cipdosetank.append(g.base_rate)
                            dtnk3=tnk1
                            if(cipdosetank and tnk1):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING TANK-3",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 1)
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING TANK-3",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP SKID FRAME"):
                            cip_flow_query=frappe.db.sql("select flow from `tabRO Items` where parent='"+str(self.choose_ro_template)+"' and item_description='CIP-1 TANK' ",as_dict=1)
                            cip_flow=0
                            
                            if(cip_flow_query):
                                cip_flow=cip_flow_query[0].flow
                            bom_for_cip='none'
                            if(float(cip_flow)>0 and float(cip_flow)<=180):
                                bom_for_cip='180 LITRES TANK FRAME'
                            elif(float(cip_flow)>180 and float(cip_flow)<=250):
                                bom_for_cip='250 LITRES TANK FRAME'
                            elif(float(cip_flow)>250 and float(cip_flow)<=450):
                                bom_for_cip='450 LITRES TANK FRAME'
                            elif(float(cip_flow)>450 and float(cip_flow)):
                                bom_for_cip='1200 LITRES TANK FRAME'
                            if(bom_for_cip!='none'):
                                price_ar=[]
                                for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='"+str(bom_for_cip)+"' ",as_dict=1):
                                    for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        price_ar.append(rate.base_rate)
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP SKID FRAME",
                                    "flow":cip_flow,
                                    "w_qty":1,
                                    "unit_price":sum(price_ar),
                                    "total_price" : sum(price_ar)
                                })
                            else:
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP SKID FRAME",
                                    "flow":1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING PUMP FRAME"):
                            cipf=[]
                            for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='LANISOSS30440X403MM' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                                if(g.base_rate>0):
                                    cipf.append(g.base_rate)
                            w_qty1=0
                            w_qty2=0
                            w_qty3=0
                            w_qty4=0
                            for vs in self.mbr_ovivo_table:
                                if(vs.item_description == "CIP DOSING PUMP-1"):
                                    w_qty1 = vs.w_qty * 2.5
                                elif(vs.item_description == "CIP DOSING PUMP-2"):
                                    w_qty2 = vs.w_qty * 2.5
                                elif(vs.item_description == "CIP DOSING PUMP-3"):
                                    w_qty3 = vs.w_qty * 2.5
                                elif(vs.item_description == "CIP DOSING PUMP-4"):
                                    w_qty4 = vs.w_qty * 2.5
                            self.append('mbr_ovivo_table', {
                                "item_description":"CIP DOSING PUMP-1 FRAME",
                                "flow":50,
                                "w_qty":w_qty1,
                                "unit_price":cipf[0],
                                "total_price" : cipf[0] * w_qty1
                            })
                            self.append('mbr_ovivo_table', {
                                "item_description":"CIP DOSING PUMP-2 FRAME",
                                "flow":50,
                                "w_qty":w_qty2,
                                "unit_price":cipf[0],
                                "total_price" : cipf[0] * w_qty2
                            })
                            self.append('mbr_ovivo_table', {
                                "item_description":"CIP DOSING PUMP-3 FRAME",
                                "flow":50,
                                "w_qty":w_qty3,
                                "unit_price":cipf[0],
                                "total_price" : cipf[0] * w_qty3
                            })
                            self.append('mbr_ovivo_table', {
                                "item_description":"CIP DOSING PUMP-4 FRAME",
                                "flow":50,
                                "w_qty":w_qty4,
                                "unit_price":cipf[0],
                                "total_price" : cipf[0] * w_qty4
                            })
                            # price_ar=[]
                            # for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='180 LITRES TANK FRAME'",as_dict=1):
                            #     for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                            #         price_ar.append(rate.base_rate)
                            # self.append('mbr_ovivo_table', {
                            #     "item_description":"CIP DOSING PUMP-1 FRAME",
                            #     "flow":180,
                            #     "w_qty":1,
                            #     "unit_price":sum(price_ar),
                            #     "total_price" : sum(price_ar)
                            # })
                            # self.append('mbr_ovivo_table', {
                            #     "item_description":"CIP DOSING PUMP-2 FRAME",
                            #     "flow":180,
                            #     "w_qty":1,
                            #     "unit_price":sum(price_ar),
                            #     "total_price" : sum(price_ar)
                            # })
                            # self.append('mbr_ovivo_table', {
                            #     "item_description":"CIP DOSING PUMP-3 FRAME",
                            #     "flow":180,
                            #     "w_qty":1,
                            #     "unit_price":sum(price_ar),
                            #     "total_price" : sum(price_ar)
                            # })
                        elif(k=="CIP DOSING TANK FRAME"):
                            price_ar=[]
                            for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='250 LITRES TANK FRAME'",as_dict=1):
                                for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    price_ar.append(rate.base_rate)
                            if(dtnk1>250):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING TANK-1 FRAME",
                                    "flow":250,
                                    "w_qty":1,
                                    "unit_price":sum(price_ar),
                                    "total_price" : sum(price_ar)
                                })
                            if(dtnk2>250):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING TANK-2 FRAME",
                                    "flow":250,
                                    "w_qty":1,
                                    "unit_price":sum(price_ar),
                                    "total_price" : sum(price_ar)
                                })
                            if(dtnk3>250):
                                self.append('mbr_ovivo_table', {
                                    "item_description":"CIP DOSING TANK-3 FRAME",
                                    "flow":250,
                                    "w_qty":1,
                                    "unit_price":sum(price_ar),
                                    "total_price" : sum(price_ar)
                                })
                        if('Sulphur Black Removal System' in selected_s):
                            if(k=="SULPHUR BLACK SLUDGE PUMP"):
                                sbsp_rate=[]
                                mbrfl=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbro_sludge_pump_capacity")
                                mbr_qt=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbro_sludge_pump_quanity_working")
                                mbr_qt2=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbro_sludge_pump_quanity_standby")
                                for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and range1>=1  and flow>='"+str(mbrfl)+"' and flow<='"+str(float(mbrfl) + 10)+"'",as_dict=1):
                                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate`,`tabPurchase Order Item`.`parent`,`tabPurchase Order Item`.`item_code` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        sbsp_rate.append(g.base_rate)
                                if(sbsp_rate):
                                    self.append('mbr_ovivo_table', {
                                        "item_description":"SULPHUR BLACK SLUDGE PUMP",
                                        "flow":round(mbrfl,2),
                                        "range":1,
                                        "w_qty":mbr_qt,
                                        "sb_qty":mbr_qt2,
                                        "unit_price":sbsp_rate[0],
                                        "total_price" : sbsp_rate[0]*(mbr_qt+mbr_qt2)
                                    })
                            elif(k=="SULPHUR BLACK DOSING PUMP"):
                                sbdp_rate=[0]
                                mbrfl=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbro_dosing_pump")
                                mbr_qt=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbro_dosing_pump_quanity_working")
                                mbr_qt2=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbro_dosing_pump_quanity_standby")
                                for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and range1>=1  and flow>='"+str(mbrfl)+"' and flow<='"+str(float(mbrfl) + 10)+"'",as_dict=1):
                                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate`,`tabPurchase Order Item`.`parent`,`tabPurchase Order Item`.`item_code` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        sbsp_rate.append(g.base_rate)
                                if(sbsp_rate):
                                    self.append('mbr_ovivo_table', {
                                        "item_description":"SULPHUR BLACK DOSING PUMP",
                                        "flow":round(mbrfl,2),
                                        "range":1,
                                        "w_qty":mbr_qt,
                                        "sb_qty":mbr_qt2,
                                        "unit_price":sbsp_rate[0],
                                        "total_price" : sbsp_rate[0]*(mbr_qt+mbr_qt2)
                                    })
                                sulcip=[]
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='LANISOSS30440X403MM' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                                    if(g.base_rate>0):
                                        sulcip.append(g.base_rate)
                                for vs in self.mbr_ovivo_table:
                                    if(vs.item_description == "SULPHUR BLACK DOSING PUMP"):
                                        w_qty1 = vs.w_qty * 2.5
                                self.append('mbr_ovivo_table', {
                                    "item_description":"SULPHUR BLACK DOSING PUMP FRAME",
                                    "flow":round(mbrfl,2),
                                    "w_qty":w_qty1,
                                    "unit_price":sulcip[0],
                                    "total_price" : sulcip[0] * w_qty1
                                })
                                cipdosetank=[]
                                addflow=(round(mbrfl,2) * 22) + 1000
                                for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='"+str((round(mbrfl,2) * 22))+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                                        if(g.base_rate>0):
                                            cipdosetank.append(g.base_rate)
                                dtnk1=(round(mbrfl,2) * 22)
                                if(cipdosetank):
                                    self.append('mbr_ovivo_table', {
                                        "item_description":"SULPHUR BLACK DOSING TANK",
                                        "flow":dtnk1,
                                        "w_qty":1,
                                        "unit_price":cipdosetank[0],
                                        "total_price" : (cipdosetank[0] * 1)
                                    })
                                else:
                                    self.append('mbr_ovivo_table', {
                                        "item_description":"SULPHUR BLACK DOSING TANK",
                                        "flow":dtnk1,
                                        "w_qty":1,
                                        "unit_price":0,
                                        "total_price" : 0
                                    })
                                price_ar=[]
                                if(dtnk1>0 and dtnk1<=180):
                                    pp="180 LITRES TANK FRAME"
                                elif(dtnk1>180 and dtnk1<=250):
                                    pp="250 LITRES TANK FRAME"
                                elif(dtnk1>250 and dtnk1<=450):
                                    pp="450 LITRES TANK FRAME"
                                elif(dtnk1>450 and dtnk1<=1200):
                                    pp="1200 LITRES TANK FRAME"
                                elif(dtnk1>1200):
                                    pp="1200 LITRES TANK FRAME"
                                else:
                                    pp='1200'
                                for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='"+str(pp)+"'",as_dict=1):
                                    for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        price_ar.append(rate.base_rate)
                                self.append('mbr_ovivo_table', {
                                    "item_description":"SULPHUR BLACK DOSING TANK FRAME",
                                    "flow":dtnk1,
                                    "w_qty":1,
                                    "unit_price":sum(price_ar),
                                    "total_price" : sum(price_ar)
                                })
                            elif(k=="SULPHUR BLACK LAMELLA SETTLER"):
                                mbrfl=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbro_lamella_settler")
                                tank_he = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"tank_height")
                                lamella= (mbrfl*4)/2.5
                                self.append('mbr_ovivo_table', {
                                    "item_description":"SULPHUR BLACK LAMELLA SETTLER",
                                    "flow":mbrfl,
                                    "range":1,
                                    "w_qty":lamella,
                                    "unit_price":7600,
                                    "total_price" : 7600 * lamella
                                })
                # #mbr_cts_cost
                # mbr_cts = ["MBR MODULES", "TOP PERMEATE MODULE", "BASE MODULE", "FEED PUMP", "PERMEATE PUMP", "BACKWASH/CIP PUMP", "SLUDGE EXTRACT PUMP", "SLUDGE RECIRCULATION PUMP", "SPRINKLER PUMP", "SULPHUR BLACK SLUDGE PUMP","SULPHUR BLACK DOSING PUMP", "SULPHUR BLACK LAMELLA SETTLER", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3","CIP DOSING PUMP FRAME", "SULPHUR BLACK DOSING PUMP", "SULPHUR BLACK LAMELLA SETTLER", "LEVEL TRANSMITTER", "LEVEL FLOAT", "ELECTROMAGNETIC FLOWMETER","TURBIDITY SENSOR", "PRESSURE TRANSMITTER", "PRESSURE GAUGE", "CIP DOSING TANK-1", "CIP DOSING TANK-2", "CIP DOSING TANK-3", "CIP DOSING TANK FRAME", "PIPES,FITTINGS & VALVES", "FAB. & ERECTION"]
                
                mbr_cts = ["MBR MODULES", "TOP PERMEATE MODULE", "BASE MODULE"]
                dtnk1=0
                dtnk2=0
                dtnk3=0
                for i in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    if(i.feed_pump_required_for_ovivo == 1):
                        mbr_cts.append("FEED PUMP")
                    mbr_cts.extend(["PERMEATE PUMP", "BACKWASH/CIP PUMP"])
                    if(i.ovivo_type == 'S-UF'):
                        mbr_cts.append("SLUDGE EXTRACT PUMP")
                    else:
                        mbr_cts.append("SLUDGE RECIRCULATION PUMP")
                    mbr_cts.extend(["SPRINKLER PUMP","MBR BLOWER","SULPHUR BLACK SLUDGE PUMP","SULPHUR BLACK DOSING PUMP", "SULPHUR BLACK LAMELLA SETTLER", "LEVEL TRANSMITTER", "LEVEL FLOAT", "ELECTROMAGNETIC FLOWMETER","TURBIDITY SENSOR", "PRESSURE TRANSMITTER", "PRESSURE GAUGE","CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3","CIP DOSING PUMP-4","CIP DOSING PUMP FRAME","CIP DOSING TANK-1", "CIP DOSING TANK-2", "CIP DOSING TANK-3","CIP DOSING TANK FRAME", "PIPES,FITTINGS & VALVES", "FAB. & ERECTION"])
                self.mbr_cts_table = []
                for i in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    for k in mbr_cts:
                        if(k == "MBR MODULES"):
                            mbrovivomodel=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='CERAMIC MBR' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrovivomodel.append(g.base_rate)
                                    
                            if(mbrovivomodel):
                                self.append('mbr_cts_table', {
                                        "item_description":"MBR MODULES",
                                        "flow":1,
                                        "range":0,
                                        "w_qty":i.cts_ovivo_no_module_required,
                                        "unit_price":mbrovivomodel[0],
                                        "total_price" : (mbrovivomodel[0] * i.cts_ovivo_no_module_required)
                                    })
                            else:
                                self.append('mbr_cts_table', {
                                        "item_description":"MBR MODULES",
                                        "flow":1,
                                        "range":0,
                                        "w_qty":i.cts_ovivo_no_module_required,
                                        "unit_price":0,
                                        "total_price" : 0
                                    })
                        elif(k == "TOP PERMEATE MODULE"):
                            mbrovivomodel=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TOP PERMEATE MODULE' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrovivomodel.append(g.base_rate)
                                    
                            if(mbrovivomodel):
                                self.append('mbr_cts_table', {
                                        "item_description":"TOP PERMEATE MODULE",
                                        "flow":1,
                                        "range":0,
                                        "w_qty":i.cts_ovivo_no_of_stacks_required,
                                        "unit_price":mbrovivomodel[0],
                                        "total_price" : (mbrovivomodel[0] * i.cts_ovivo_no_of_stacks_required)
                                    })
                            else:
                                self.append('mbr_cts_table', {
                                        "item_description":"TOP PERMEATE MODULE",
                                        "flow":1,
                                        "range":0,
                                        "w_qty":i.cts_ovivo_no_of_stacks_required,
                                        "unit_price":0,
                                        "total_price" : 0
                                    })
                        elif(k == "BASE MODULE"):
                            mbrovivomodel=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='BASE MODULE' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrovivomodel.append(g.base_rate)
                                    
                            if(mbrovivomodel):
                                self.append('mbr_cts_table', {
                                        "item_description":"BASE MODULE",
                                        "flow":1,
                                        "range":0,
                                        "w_qty":i.cts_ovivo_no_of_stacks_required,
                                        "unit_price":mbrovivomodel[0],
                                        "total_price" : (mbrovivomodel[0] * i.cts_ovivo_no_of_stacks_required)
                                    })
                            else:
                                self.append('mbr_cts_table', {
                                        "item_description":"BASE MODULE",
                                        "flow":1,
                                        "range":0,
                                        "w_qty":i.cts_ovivo_no_of_stacks_required,
                                        "unit_price":0,
                                        "total_price" : 0
                                    })
                        elif(k=="FEED PUMP"):
                            if(i.feed_pump_required_for_ovivo == 1):
                                mbrovivofeed=[]
                                addflow=float(i.cts_ovivo_permeate_pump) + 10
                                for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and flow>='"+str(i.cts_ovivo_permeate_pump)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        mbrovivofeed.append(g.base_rate)
                                
                                if(mbrovivofeed and i.cts_ovivo_permeate_pump>0):
                                    self.append('mbr_cts_table', {
                                        "item_description":"FEED PUMP",
                                        "flow":i.cts_ovivo_permeate_pump,
                                        "w_qty":i.cts_ovivo_permeate_qty,
                                        "sb_qty":i.cts_ovivo_permeate_sqty,
                                        "unit_price":mbrovivofeed[0],
                                        "total_price" : (mbrovivofeed[0] * (i.cts_ovivo_permeate_pump + i.cts_ovivo_permeate_qty + i.cts_ovivo_permeate_sqty))
                                    })
                                else:
                                    self.append('mbr_cts_table', {
                                        "item_description":"FEED PUMP",
                                        "flow":i.cts_ovivo_permeate_pump,
                                        "w_qty":i.cts_ovivo_permeate_qty,
                                        "sb_qty":i.cts_ovivo_permeate_sqty,
                                        "unit_price":0,
                                        "total_price" : 0
                                    })
                            else:
                                self.append('mbr_cts_table', {
                                        "item_description":"FEED PUMP",
                                        "flow":0,
                                        "w_qty":0,
                                        "unit_price":0,
                                        "total_price" : 0
                                    })
                        elif(k=="PERMEATE PUMP"):
                            mbrper=[]
                            addflow=float(i.cts_ovivo_permeate_pump) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and range1>=1.5 and flow>='"+str(i.cts_ovivo_permeate_pump)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrper.append(g.base_rate)
                            
                            if(mbrper and i.cts_ovivo_permeate_pump>0):
                                self.append('mbr_cts_table', {
                                    "item_description":"PERMEATE PUMP",
                                    "flow":i.cts_ovivo_permeate_pump,
                                    "range":1.5,
                                    "w_qty":i.cts_ovivo_permeate_qty,
                                    "sb_qty":i.cts_ovivo_permeate_sqty,
                                    "unit_price":mbrper[0],
                                    "total_price" : (mbrper[0] * (i.cts_ovivo_permeate_qty + i.cts_ovivo_permeate_sqty))
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"PERMEATE PUMP",
                                    "flow":i.cts_ovivo_permeate_pump,
                                    "range":1.5,
                                    "w_qty":i.cts_ovivo_permeate_qty,
                                    "sb_qty":i.cts_ovivo_permeate_sqty,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="BACKWASH/CIP PUMP"):
                            mbrper=[]
                            addflow=float(i.cts_ovivo_bc) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and range1>=1 and flow>='"+str(i.cts_ovivo_bc)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrper.append(g.base_rate)
                            
                            if(mbrper and i.cts_ovivo_bc>0):
                                self.append('mbr_cts_table', {
                                    "item_description":"BACKWASH/CIP PUMP",
                                    "flow":i.cts_ovivo_bc,
                                    "range":1.5,
                                    "w_qty":i.cts_ovivo_backwash_qty,
                                    "sb_qty":i.cts_ovivo_backwash_sqty,
                                    "unit_price":mbrper[0],
                                    "total_price" : (mbrper[0] * (i.cts_ovivo_backwash_qty + i.cts_ovivo_backwash_sqty))
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"BACKWASH/CIP PUMP",
                                    "flow":i.cts_ovivo_bc,
                                    "range":1.5,
                                    "w_qty":i.cts_ovivo_backwash_qty,
                                    "sb_qty":i.cts_ovivo_backwash_sqty,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="SLUDGE EXTRACT PUMP"):
                            mbrper=[]
                            addflow=float(i.cts_ovivo_sludge_pump_2) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and range1>=1 and flow>='"+str(i.cts_ovivo_sludge_pump_2)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrper.append(g.base_rate)
                            
                            if(mbrper and i.cts_ovivo_sludge_pump_2>0):
                                self.append('mbr_cts_table', {
                                    "item_description":"SLUDGE EXTRACT PUMP",
                                    "flow":i.cts_ovivo_sludge_pump_2,
                                    "range":1,
                                    "w_qty":i.cts_ovivo_sludge_qty,
                                    "sb_qty":i.cts_ovivo_sludge_qty,
                                    "unit_price":mbrper[0],
                                    "total_price" : (mbrper[0] * (i.cts_ovivo_sludge_qty + i.cts_ovivo_sludge_qty))
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"SLUDGE EXTRACT PUMP",
                                    "flow":i.cts_ovivo_sludge_pump_2,
                                    "range":1,
                                    "w_qty":i.cts_ovivo_sludge_qty,
                                    "sb_qty":i.cts_ovivo_sludge_qty,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="SPRINKLER PUMP"):
                            mbrper=[]
                            addflow=float(i.cts_ovivo_sprinkler_pump_2) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and range1>=1.5 and flow>='"+str(i.cts_ovivo_sprinkler_pump_2)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrper.append(g.base_rate)
                            
                            if(mbrper and i.cts_ovivo_sprinkler_pump_2>0):
                                self.append('mbr_cts_table', {
                                    "item_description":"SPRINKLER PUMP",
                                    "flow":i.cts_ovivo_sprinkler_pump_2,
                                    "range":1.5,
                                    "w_qty":i.cts_ovivo_sprinkler_qty,
                                    "sb_qty":i.cts_ovivo_sprinkler_qty,
                                    "unit_price":mbrper[0],
                                    "total_price" : (mbrper[0] * (i.cts_ovivo_sprinkler_qty + i.cts_ovivo_sprinkler_qty))
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"SPRINKLER PUMP",
                                    "flow":i.cts_ovivo_sprinkler_pump_2,
                                    "range":1.5,
                                    "w_qty":i.cts_ovivo_sprinkler_qty,
                                    "sb_qty":i.cts_ovivo_sprinkler_qty,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="MBR BLOWER"):
                            motor_cost=0
                            mbr_blower_flow=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"cts_ovivo_blower")
                            flow3min = mbr_blower_flow * 0.588578
                            mbr_range = 0.45
                            inchh2 = mbr_range * 401.865
                            power = ((flow3min * inchh2)/(6356 * 0.67))/1.34
                            if(power<=0.045): kw=0.045; 
                            elif(power<=0.18): kw=0.18; 
                            elif(power<=0.37): kw=0.37; motor_cost=9622; 
                            elif(power<=0.55): kw=0.55; motor_cost=10476; 
                            elif(power<=0.75): kw=0.75; motor_cost=11117; 
                            elif(power<=1.1): kw=1.1; motor_cost=12078; 
                            elif(power<=1.5): kw=1.5; motor_cost=13547; 
                            elif(power<=2.2): kw=2.2; motor_cost=15789; 
                            elif(power<=3.7): kw=3.7; motor_cost=21503; 
                            elif(power<=4): kw=4; motor_cost=24888; 
                            elif(power<=5.5): kw=5.5; motor_cost=30800; 
                            elif(power<=7.5): kw=7.5; motor_cost=52931; 
                            elif(power<=11): kw=11; motor_cost=53813; 
                            elif(power<=15): kw=15; motor_cost=74261; 
                            elif(power<=18.5): kw=18.5; motor_cost=83169; 
                            elif(power<=22): kw=22; motor_cost=104988; 
                            elif(power<=30): kw=30; motor_cost=119441; 
                            elif(power<=37): kw=37; motor_cost=170992; 
                            elif(power<=45): kw=45; motor_cost=249535; 
                            elif(power<=55): kw=55; motor_cost=286980; 
                            elif(power<=75): kw=75; motor_cost=330045; 
                            elif(power<=90): kw=90; motor_cost=387308; 
                            elif(power<=110): kw=110; motor_cost=471705; 
                            elif(power<=160): kw=160; motor_cost=516345;
                            self.append('mbr_cts_table', {
                                    "item_description":"MBR BLOWER",
                                    "flow":i.cts_ovivo_blower,
                                    "range":0.45,
                                    "w_qty":1,
                                    "sb_qty":1,
                                    "unit_price":0,
                                    "motor_cost":motor_cost*2,
                                    "total_price" : 0+(motor_cost*2)
                                })
                        elif(k=="CIP DOSING PUMP-1"):
                            mbrcip=[]
                            cipflow = i.cts_naocl_dosing_pump_rc
                            addflow=float(cipflow) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='DOSING PUMP' and flow>='"+str(cipflow)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrcip.append(g.base_rate)
                            
                            if(mbrcip and cipflow>0):
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING PUMP-1",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 2)
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING PUMP-1",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING PUMP-2"):
                            mbrcip=[]
                            cipflow = i.cts_citric_dosing_pump_mc_rc
                            addflow=float(cipflow) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='DOSING PUMP' and flow>='"+str(cipflow)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrcip.append(g.base_rate)
                            
                            if(mbrcip and cipflow>0):
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING PUMP-2",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 2)
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING PUMP-2",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING PUMP-3"):
                            mbrcip=[]
                            cipflow = i.cts_hcl_dosing_pump_mc_rc
                            addflow=float(cipflow) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='DOSING PUMP' and flow>='"+str(cipflow)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrcip.append(g.base_rate)
                            if(mbrcip and cipflow>0):
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING PUMP-3",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 2)
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING PUMP-3",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING PUMP-4"):
                            mbrcip=[]
                            cipflow = i.cts_alum_dosing_pump_mc_rc
                            addflow=float(cipflow) + 10
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='DOSING PUMP' and flow>='"+str(cipflow)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    mbrcip.append(g.base_rate)
                            if(mbrcip and cipflow>0):
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING PUMP-4",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 2)
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING PUMP-4",
                                    "flow":cipflow,
                                    "w_qty":1,
                                    "ssb_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k == "TURBIDITY SENSOR" and self.is_rewolutte==1):
                            self.append('mbr_cts_table',{
                                "item_description":k,
                                "flow":0,
                                "w_qty":i.cts_ovivo_no_of_trains,
                                "unit_price":250000,
                                "total_price" : 250000*float(i.cts_ovivo_no_of_trains)
                            })
                            cs_cost=frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`description`='Conductivity sensor' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            cs=cs_cost[0].base_rate if cs_cost else 0
                            self.append('mbr_cts_table',{
                                "item_description":"CONDUCTIVITY SENSOR",
                                "flow":0,
                                "w_qty":1,
                                "unit_price":cs,
                                "total_price" : cs
                            })
                        elif(k == "LEVEL TRANSMITTER"):
                            lvltran=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='LEVEL TRANSMITTER' ",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    lvltran.append(g.base_rate)
                            
                            
                            if(lvltran):
                                self.append('mbr_cts_table', {
                                    "item_description":"LEVEL TRANSMITTER",
                                    "flow":1,
                                    "range":i.tank_height,
                                    "w_qty":i.cts_ovivo_no_of_trains,
                                    "unit_price":lvltran[0],
                                    "total_price" : (lvltran[0] * i.design_no_of_trains)
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"LEVEL TRANSMITTER",
                                    "flow":1,
                                    "range":i.tank_height,
                                    "w_qty":i.cts_ovivo_no_of_trains,
                                    "unit_price":0,
                                    "total_price":0
                                })   
                        elif(k == "LEVEL FLOAT"):
                            lvlfloat=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='LEVEL FLOAT' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    lvlfloat.append(g.base_rate)
                                    
                            if(lvlfloat):
                                self.append('mbr_cts_table', {
                                    "item_description":"LEVEL FLOAT",
                                    "flow":1,
                                    "w_qty":3,
                                    "unit_price":lvlfloat[0],
                                    "total_price" : (lvlfloat[0] * 3)
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"LEVEL FLOAT",
                                    "flow":1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="ELECTROMAGNETIC FLOWMETER"):
                            elm=[]
                            addflow=float(i.cts_ovivo_bc) +20
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='ELECTROMAGNETIC FLOWMETER' and flow>='"+str(i.cts_ovivo_bc)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    elm.append(g.base_rate)
                            
                            if(elm and i.cts_ovivo_bc>0):
                                self.append('mbr_cts_table', {
                                    "item_description":"ELECTROMAGNETIC FLOWMETER",
                                    "flow":i.cts_ovivo_bc,
                                    "w_qty":(i.cts_ovivo_no_of_trains + i.cts_ovivo_sprinkler_qty + i.cts_ovivo_backwash_qty + i.cts_ovivo_sludge_qty),
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * i.design_no_of_trains)
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"ELECTROMAGNETIC FLOWMETER",
                                    "flow":i.cts_ovivo_bc,
                                    "w_qty":(i.cts_ovivo_no_of_trains + i.cts_ovivo_sprinkler_qty + i.cts_ovivo_backwash_qty + i.cts_ovivo_sludge_qty),
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k == "PRESSURE TRANSMITTER"):
                            pressure=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='PRESSURE TRANSMITTER' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    pressure.append(g.base_rate)
                                    
                            if(pressure):
                                self.append('mbr_cts_table', {
                                    "item_description":"PRESSURE TRANSMITTER",
                                    "flow":1,
                                    "w_qty":(i.cts_ovivo_no_of_trains + i.cts_ovivo_sprinkler_qty + i.cts_ovivo_backwash_qty + i.cts_ovivo_sludge_qty),
                                    "unit_price":pressure[0],
                                    "total_price" : (pressure[0] * 1)
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"PRESSURE TRANSMITTER",
                                    "flow":1,
                                    "w_qty":(i.cts_ovivo_no_of_trains + i.cts_ovivo_sprinkler_qty + i.cts_ovivo_backwash_qty + i.cts_ovivo_sludge_qty),
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k == "PRESSURE GAUGE"):
                            pressure=[]
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='PRESSURE GAUGE' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    pressure.append(g.base_rate)
                                    
                            if(pressure):
                                self.append('mbr_cts_table', {
                                    "item_description":"PRESSURE GAUGE",
                                    "flow":1,
                                    "w_qty":(i.cts_ovivo_no_of_trains + i.cts_ovivo_sprinkler_qty + i.cts_ovivo_backwash_qty + i.cts_ovivo_sludge_qty),
                                    "unit_price":pressure[0],
                                    "total_price" : (pressure[0] * 1)
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"PRESSURE GAUGE",
                                    "flow":1,
                                    "w_qty":(i.cts_ovivo_no_of_trains + i.cts_ovivo_sprinkler_qty + i.cts_ovivo_backwash_qty + i.cts_ovivo_sludge_qty),
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING TANK-1"):
                            cipdosetank=[]
                            tnk1 = i.cts_naocl_dosing_pump_rc *2
                            addflow=tnk1+1000
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='"+str(tnk1)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    cipdosetank.append(g.base_rate)
                            dtnk1=tnk1
                            if(cipdosetank and tnk1>0):
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING TANK-1",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 1)
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING TANK-1",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING TANK-2"):
                            cipdosetank=[]
                            tnk1 = i.cts_citric_dosing_pump_mc_rc *2
                            addflow=tnk1+1000
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='"+str(tnk1)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    cipdosetank.append(g.base_rate)
                            dtnk2=tnk1
                            if(cipdosetank and tnk1>0):
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING TANK-2",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 1)
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING TANK-2",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING TANK-3"):
                            cipdosetank=[]
                            tnk1 = i.cts_hcl_dosing_pump_mc_rc *2
                            addflow=tnk1+1000
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='"+str(tnk1)+"' and flow<='"+str(addflow)+"'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    cipdosetank.append(g.base_rate)
                            dtnk3=tnk1
                            if(cipdosetank and tnk1):
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING TANK-3",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":g.base_rate,
                                    "total_price" : (g.base_rate * 1)
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING TANK-3",
                                    "flow":tnk1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP SKID FRAME"):
                            cip_flow_query=frappe.db.sql("select flow from `tabRO Items` where parent='"+str(self.choose_ro_template)+"' and item_description='CIP-1 TANK' ",as_dict=1)
                            cip_flow=0
                            
                            if(cip_flow_query):
                                cip_flow=cip_flow_query[0].flow
                            bom_for_cip='none'
                            if(float(cip_flow)>0 and float(cip_flow)<=180):
                                bom_for_cip='180 LITRES TANK FRAME'
                            elif(float(cip_flow)>180 and float(cip_flow)<=250):
                                bom_for_cip='250 LITRES TANK FRAME'
                            elif(float(cip_flow)>250 and float(cip_flow)<=450):
                                bom_for_cip='450 LITRES TANK FRAME'
                            elif(float(cip_flow)>450 and float(cip_flow)):
                                bom_for_cip='1200 LITRES TANK FRAME'
                            if(bom_for_cip!='none'):
                                price_ar=[]
                                for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='"+str(bom_for_cip)+"' ",as_dict=1):
                                    for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        price_ar.append(rate.base_rate)
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP SKID FRAME",
                                    "flow":cip_flow,
                                    "w_qty":1,
                                    "unit_price":sum(price_ar),
                                    "total_price" : sum(price_ar)
                                })
                            else:
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP SKID FRAME",
                                    "flow":1,
                                    "w_qty":1,
                                    "unit_price":0,
                                    "total_price" : 0
                                })
                        elif(k=="CIP DOSING PUMP FRAME"):
                            cipf=[]
                            w_qty1=0
                            w_qty2=0
                            w_qty3=0
                            w_qty4=0
                            for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='LANISOSS30440X403MM' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                                if(g.base_rate>0):
                                    cipf.append(g.base_rate)
                            for vs in self.mbr_cts_table:
                                if(vs.item_description == "CIP DOSING PUMP-1"):
                                    w_qty1 = vs.w_qty * 2.5
                                elif(vs.item_description == "CIP DOSING PUMP-2"):
                                    w_qty2 = vs.w_qty * 2.5
                                elif(vs.item_description == "CIP DOSING PUMP-3"):
                                    w_qty3 = vs.w_qty * 2.5
                                elif(vs.item_description == "CIP DOSING PUMP-4"):
                                    w_qty4 = vs.w_qty * 2.5
                            self.append('mbr_cts_table', {
                                "item_description":"CIP DOSING PUMP-1 FRAME",
                                "flow":50,
                                "w_qty":w_qty1,
                                "unit_price":cipf[0],
                                "total_price" : cipf[0] * w_qty1
                            })
                            self.append('mbr_cts_table', {
                                "item_description":"CIP DOSING PUMP-2 FRAME",
                                "flow":50,
                                "w_qty":w_qty2,
                                "unit_price":cipf[0],
                                "total_price" : cipf[0] * w_qty2
                            })
                            self.append('mbr_cts_table', {
                                "item_description":"CIP DOSING PUMP-3 FRAME",
                                "flow":50,
                                "w_qty":w_qty3,
                                "unit_price":cipf[0],
                                "total_price" : cipf[0] * w_qty3
                            })
                            self.append('mbr_cts_table', {
                                "item_description":"CIP DOSING PUMP-4 FRAME",
                                "flow":50,
                                "w_qty":w_qty4,
                                "unit_price":cipf[0],
                                "total_price" : cipf[0] * w_qty4
                            })
                        elif(k=="CIP DOSING TANK FRAME"):
                            price_ar=[]
                            for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='250 LITRES TANK FRAME'",as_dict=1):
                                for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    price_ar.append(rate.base_rate)
                            if(dtnk1>250):
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING TANK-1 FRAME",
                                    "flow":250,
                                    "w_qty":1,
                                    "unit_price":sum(price_ar),
                                    "total_price" : sum(price_ar)
                                })
                            if(dtnk2>250):
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING TANK-2 FRAME",
                                    "flow":250,
                                    "w_qty":1,
                                    "unit_price":sum(price_ar),
                                    "total_price" : sum(price_ar)
                                })
                            if(dtnk3>250):
                                self.append('mbr_cts_table', {
                                    "item_description":"CIP DOSING TANK-3 FRAME",
                                    "flow":250,
                                    "w_qty":1,
                                    "unit_price":sum(price_ar),
                                    "total_price" : sum(price_ar)
                                })
                        
                                
                # bio_calculation
                
                a0=["LIFTING SUMP PUMP", "LPS LEVEL FLOAT", "LPS LEVEL TRANSMITTER", "LPS PIPES", "LPS LIFTING", "NT PUMP", "NT EMFM", "NT DOSING PUMP", "NT PH SENSOR", "NT DIFFUSER", "NT PIPES", "NT DIFFUSER PIPES", "NT LEVEL FLOAT", "NT LEVEL TRANSMITTER", "NT LIFTING", "DT DIFFUSER", "DT DIFFUSER PIPES", "CFT DIFFUSER", "CFT DIFFUSER PIPES", "SRS PUMP", "SRS EMFM", "SRS DIFFUSER", "SRS PIPES", "SRS DIFFUSER PIPES", "SRS LEVEL FLOAT", "SRS LIFTING", "LIFTING HOIST", "LIFTING HOIST BASE"]
                re_a0=["SUBMERSIBLE PUMP", "LEVEL FLOAT", "LEVEL TRANSMITTER", "PIPES", "FITTINGS", "SUBMERSIBLE PUMP", "ELECTROMAGNETIC FLOWMETER", "DOSING PUMP", "PH SENSOR", "DIFFUSER", "PIPES", "PIPES", "LEVEL FLOAT", "LEVEL TRANSMITTER", "FITTINGS", "DIFFUSER", "PIPES", "DIFFUSER", "PIPES", "SUBMERSIBLE PUMP", "ELECTROMAGNETIC FLOWMETER", "DIFFUSER", "PIPES", "PIPES", "LEVEL FLOAT","FITTINGS", "LIFTING HOIST", "LIFTING HOIST BASE"]
                sys = ["Lifting sump", "Lifting sump", "Lifting sump", "Lifting sump", "Lifting sump", "Neutralization System", "Neutralization System", "Neutralization System", "Neutralization System", "Neutralization System", "Neutralization System", "Neutralization System", "Neutralization System", "Neutralization System", "Neutralization System", "Distribution system", "Distribution system", "Clarifier Feed Tank", "Clarifier Feed Tank", "SRS System", "SRS System", "SRS System", "SRS System", "SRS System", "SRS System", "SRS System", "LIFTING HOIST", "LIFTING HOIST BASE"]
                for m in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    a0.extend(["DAF BUBBLE GENERATION PUMP", "DAF SLUDGE PUMP", "DAF LEVEL FLOAT","DAF PRESSURE GAUGE","DAF COMPOUND GAUGE","DAF AIR FLOWMETER"])
                    re_a0.extend(["BUBBLE GENERATION PUMP", "SURFACE MOUNTED PUMP", "LEVEL FLOAT","DAF PRESSURE GAUGE","DAF COMPOUND GAUGE","DAF AIR FLOWMETER"])
                    sys.extend(["DAF (Dissolved Air Flotation)", "DAF (Dissolved Air Flotation)", "DAF (Dissolved Air Flotation)", "DAF (Dissolved Air Flotation)","DAF (Dissolved Air Flotation)","DAF (Dissolved Air Flotation)"])
                    
                    sel_system=[]
                    for v in frappe.db.sql("SELECT selected_system_name FROM `tabSelected Process System` where parent='"+str(self.project_startup_sheet)+"'",as_dict=1):
                        sel_system.append(v.selected_system_name)
                    
                    if "Lifting sump" in sel_system:
                        pass
                    else:
                        if "DAF (Dissolved Air Flotation)" in sel_system:
                            a0.append("DAF FEED PUMP")
                            re_a0.append("SURFACE MOUNTED PUMP")
                            sys.append("DAF (Dissolved Air Flotation)")

                    if "DAF (Dissolved Air Flotation)" in sel_system:
                        if(m.daf_with_dosing):
                            a0.extend(["DAF TURBIDITY SENSOR", "DAF EMFM","DAF DOSING PUMP-1", "DAF DOSING PUMP-2", "DAF DOSING PUMP-1 FRAME", "DAF DOSING PUMP-2 FRAME", "DAF DOSING TANK-1","DAF DOSING TANK-2","DAF DOSING TANK-1 FRAME", "DAF DOSING TANK-2 FRAME"])
                            re_a0.extend(["TURBIDITY SENSOR", "ELECTROMAGNETIC FLOWMETER","DOSING PUMP", "DOSING PUMP","DAF DOSING PUMP-1 FRAME", "DAF DOSING PUMP-2 FRAME", "DAF DOSING TANK-1","DAF DOSING TANK-2","DAF DOSING TANK-1 FRAME", "DAF DOSING TANK-2 FRAME"])
                            sys.extend(["DAF (Dissolved Air Flotation)", "DAF (Dissolved Air Flotation)","DAF (Dissolved Air Flotation)", "DAF (Dissolved Air Flotation)","DAF (Dissolved Air Flotation)","DAF (Dissolved Air Flotation)","DAF (Dissolved Air Flotation)","DAF (Dissolved Air Flotation)","DAF (Dissolved Air Flotation)","DAF (Dissolved Air Flotation)"])
                        
                    a0.extend(["EQT DIFFUSER","EQT BRANCH PIPES","EQT GRID PIPES"])
                    re_a0.extend(["DIFFUSER","PIPES","PIPES"])
                    sys.extend(["Equalization System", "Equalization System","Equalization System"])
                    
                    if(m.seperate_blower_for_equalization_tank ==1):
                        a0.extend(["EQT BLOWER","EQT BLOWER PIPES"])
                        re_a0.extend(["BLOWER","PIPES"])
                        sys.extend(["Equalization System", "Equalization System"])
                    if(m.eqt_tank_type == "Carousel"):
                        a0.append("EQT FLOW MAKER")
                        re_a0.append("FLOW MAKER")
                        sys.append("Equalization System")
                    
                    a0.extend(["BIO DIFFUSER", "BIO BLOWER", "BIO LATERAL", "BIO HEADER PIPES", "BIO BRANCH PIPES", "BIO BLOWER PIPES", "DO SENSOR"])
                    re_a0.extend(["DIFFUSER", "BLOWER", "OTT LATERAL", "PIPES", "PIPES", "PIPES", "DO SENSOR"])
                    sys.extend(["Biological Oxidation System", "Biological Oxidation System", "Biological Oxidation System", "Biological Oxidation System", "Biological Oxidation System", "Biological Oxidation System", "Biological Oxidation System"])
                    
                    if(m.bio_tank_type == "Carousel"):
                        a0.append("BIO FLOW MAKER")
                        re_a0.append("FLOW MAKER")
                        sys.append("Biological Oxidation System")
                    if "De-Nitrification System" in sel_system:
                        a0.extend(["DNT PUMP", "DNT FLOW MIXER", "DNT EMFM", "DNT PIPES", "DNT LIFTING"])
                        re_a0.extend(["SUBMERSIBLE PUMP", "FLOW MIXER", "ELECTROMAGNETIC FLOWMETER", "PIPES", "FITTINGS"])
                        sys.extend(["De-Nitrification System", "De-Nitrification System", "De-Nitrification System", "De-Nitrification System", "De-Nitrification System"])
                    
                self.pre_treatment_table=[]
                for i in range(len(a0)):
                    if(sys[i] in selected_s):
                        self.append('pre_treatment_table', {
                            "item_description":a0[i],
                            "renamed":re_a0[i],
                            "system":sys[i]
                        })
                ar=["LIFTING HOIST","LIFTING HOIST BASE"]
                for j in ar:
                    self.append('pre_treatment_table',{
                        "item_description":str(j),
                        "renamed":str(j),
                        "system":str(j)
                    })
                for m in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    for i in self.pre_treatment_table:
                        if(i.item_description == "LIFTING SUMP PUMP"):
                            if("DAF (Dissolved Air Flotation)" in selected_s):
                                flow=round((m.flow/24)*1.2)
                            else:
                                flow=round((m.flow/24)*1.5)
                            w_qty=1
                            if(flow>125):
                                if("DAF (Dissolved Air Flotation)" in selected_s):
                                    vv = (((m.flow/24)*1.2)/125)
                                    w_qty = int(-1 * vv // 1 * -1)
                                    flow=flow/w_qty
                                else:
                                    w_qty=round(round(m.flow/24)*1.5/125)
                                    flow=flow/w_qty
                            else:
                                flow=flow;
                                w_qty=1
                            i.flow=flow
                            # i.range = (((m.tank_height/10)+0.5)*100)/100
                            i.range = (m.tank_height + 0.5)/10
                            i.w_qty = w_qty;
                            i.sb_qty = 1
                        elif(i.item_description=="DRUM SCREENER"):
                            i.flow=round((m.flow/24),2)
                            i.w_qty=1
                        elif(i.item_description == "EQT DIFFUSER"):
                            i.flow = 1
                            i.w_qty = m.eqtk
                        elif(i.item_description == "EQT TANK PIPE"):
                            i.range = m.e_bio_size
                            i.w_qty = m.e_bio_float
                        elif(i.item_description == "EQT BLOWER"):
                            i.flow = m.eq_blower
                            i.range = (m.tank_height +  0.5)/10
                            i.w_qty = 1
                        elif(i.item_description == "EQT DIFFUSER PIPES"):
                            i.flow=0
                            i.range=m.eqt_diffuser_pipe_line_size
                            i.w_qty=m.eqt_diffuser_pipe_line_length
                        elif(i.item_description in ["DT DIFFUSER","SRS DIFFUSER","CFT DIFFUSER","NT DIFFUSER"]):
                            i.flow = 1
                            i.range = 0
                            value_w_qty = (m.diffuser_dt+m.diffuser_srs+m.diffuser_cft+m.diffuser_nt)
                            if(i.item_description=="DT DIFFUSER"):value_w_qty=m.diffuser_dt
                            elif(i.item_description=="SRS DIFFUSER"):value_w_qty=m.diffuser_srs
                            elif(i.item_description=="CFT DIFFUSER"):value_w_qty=m.diffuser_cft
                            elif(i.item_description=="NT DIFFUSER"):value_w_qty=m.diffuser_nt
                            v=int(-1 * value_w_qty // 5 * -5)
                            i.w_qty = v
                        elif(i.item_description=="BIO DIFFUSER"):
                            i.flow=1;i.range=0;i.w_qty=round(m.no_of_diff)
                        elif(i.item_description in ["LPS PIPES","NT PIPES","DNT PIPES","SRS PIPES"]):
                            qqty=0
                            a_f = self.flow/24
                            m_v = 2.5
                            f0 = 3600
                            f2=(((4*a_f)/(m_v*f0*3.14))**(1/2))*1000
                            if(i.item_description=="LPS PIPES"):
                                if("DAF (Dissolved Air Flotation)" in selected_s):f2=f2*1.2
                                else:f2=f2*1.5
                                qqty=(m.tank_height+0.5+0.5)*2
                            elif(i.item_description=="NT PIPES"):
                                f2=f2
                                qqty=(m.tank_height+0.5+5)*2
                            elif(i.item_description=="SRS PIPES"):
                                f2=f2*1.5
                                qqty=(m.tank_height+0.5+0.5)*2
                            elif(i.item_description=="DNT PIPES"):
                                f2=f2*2
                                qqty=(m.tank_height+0.5)*2
                            if(f2>0 and f2<6.99):ff="DN6"
                            elif(f2>6.99 and f2<10.42):ff="DN8"
                            elif(f2>10.42 and f2<13.85):ff="DN10"
                            elif(f2>13.85 and f2<18.04):ff="DN15"   
                            elif(f2>18.04 and f2<23.37):ff="DN20"
                            elif(f2>23.37 and f2<30.1):ff="DN25"
                            elif(f2>30.1 and f2<38.86):ff="DN32"
                            elif(f2>38.86 and f2<44.96):ff="DN40"
                            elif(f2>44.96 and f2<57.08):ff="DN50"
                            elif(f2>57.08 and f2<68.81):ff="DN65"
                            elif(f2>68.81 and f2<84.68):ff="DN80"
                            elif(f2>84.68 and f2<110.08):ff="DN100"
                            elif(f2>110.08 and f2<135.76):ff="DN125"
                            elif(f2>135.76 and f2<162.72):ff="DN150"
                            elif(f2>162.72 and f2<213.54):ff="DN200"
                            elif(f2>213.54 and f2<266.25):ff="DN250"
                            elif(f2>266.25 and f2<315.93):ff="DN300"
                            elif(f2>315.93 and f2<347.68):ff="DN350"
                            elif(f2>347.68 and f2<398.02):ff="DN400"
                            elif(f2>398.02 and f2<448.62):ff="DN450"
                            elif(f2>448.62 and f2<498.44):ff="DN500"
                            elif(f2>498.44 and f2<549.44):ff="DN550"
                            elif(f2>549.44 and f2<598.92):ff="DN600"
                            elif(f2>598.92 and f2<749.3):ff="DN750"
                            i.range=ff
                            i.w_qty=qqty
                        elif(i.renamed == "PIPES"):
                            if(i.item_description == "NT DIFFUSER PIPES"):
                                i.flow=0
                                i.range=m.nt_pipe_size
                                i.w_qty=m.nt_pipe_length
                            elif(i.item_description == "DT DIFFUSER PIPES"):
                                i.flow=0
                                i.range=m.dt_pipe_size
                                i.w_qty=m.dt_pipe_length
                            elif(i.item_description == "CFT DIFFUSER PIPES"):
                                i.flow=0
                                i.range=m.cft_pipe_size
                                i.w_qty=m.cft_pipe_length
                            elif(i.item_description == "SRS DIFFUSER PIPES"):
                                i.flow=0
                                i.range=m.srs_pipe_size
                                i.w_qty=m.srs_pipe_length
                            elif(i.item_description=="BIO HEADER PIPES"):
                                if(m.seperate_blower_for_equalization_tank == 1):
                                    i.range = m.s_blower_size
                                    i.w_qty = m.s_blower_length
                                else:
                                    i.range = m.n_s_blower_size
                                    i.w_qty = m.ns_blower_length
                            elif(i.item_description=="BIO BRANCH PIPES"):
                                i.range=m.b_bio_size
                                i.w_qty=m.b_bio_length
                            elif(i.item_description=="BIO BLOWER PIPES"):
                                i.range=m.d_blower_size
                                i.w_qty=m.d_blower_length
                            elif(i.item_description=="EQT BLOWER PIPES"):
                                if(m.seperate_blower_for_equalization_tank == 1):
                                    i.range=m.s_blower_size
                                    i.w_qty=m.s_blower_length
                                else:
                                    i.range=0
                                    i.w_qty=0
                            elif(i.item_description=="EQT BRANCH PIPES"):
                                i.range=m.e_bio_size
                                i.w_qty=m.e_bio_float
                            elif(i.item_description=="EQT GRID PIPES"):
                                i.range=m.eqt_diffuser_pipe_line_size
                                i.w_qty=m.eqt_diffuser_pipe_line_length
                        elif(i.item_description == "EQT FLOW MAKER"):
                            if(m.eqt_tank_type == "Carousel"):
                                i.w_qty=1
                                i.unit_price=2100000
                                i.total_price=2100000
                        elif(i.item_description == "BIO FLOW MAKER"):
                            if(m.bio_tank_type == "Carousel"):
                                i.w_qty = m.no_of_bio_tanks * 2
                                i.unit_price=2100000
                                i.total_price=2100000*float(i.w_qty)
                        elif(i.item_description == "NT PUMP"):
                            flow=round(m.flow/24)
                            w_qty=1
                            if(flow>125):
                                vv = ((m.flow/24)/125)
                                w_qty = int(-1 * vv // 1 * -1)
                                flow=flow/w_qty
                            else:
                                flow=flow;
                                w_qty=1
                            i.flow=flow
                            i.range = (m.tank_height + 0.5 + 5)/10
                            i.w_qty=w_qty
                            i.sb_qty=1
                        elif(i.item_description == "SRS PUMP"):
                            flow=round(m.flow/24)
                            w_qty=1
                            if(flow>125):
                                vv = ((m.flow/24)/125)
                                w_qty = int(-1 * vv // 1 * -1)
                                flow=flow/w_qty
                            else:
                                flow=flow;
                                w_qty=1
                            i.flow=flow
                            i.range = (m.tank_height)/10
                            i.w_qty=w_qty
                            i.sb_qty=1
                        elif(i.item_description == "DNT PUMP"):
                            flow=round(m.flow*2/24)
                            w_qty=1
                            if(flow>250):
                                while(flow>125):w_qty=round(round(m.flow*2/24)/125);flow=flow/w_qty
                            elif(flow>125):
                                flow=flow/2;w_qty=2
                            i.flow=flow
                            i.range = (m.tank_height + 0.5 + 0.5)/10
                            i.w_qty=w_qty
                            i.sb_qty=1
                        elif(i.item_description == "NT PH SENSOR"):
                            i.w_qty = 1
                            i.flow = 1
                        elif(i.item_description == "NT DOSING PUMP"):
                            i.flow=round(m.flow/15)
                            i.w_qty =1
                            i.ssb_qty=1
                        elif(i.item_description == "NT PRESSURE GAUGE"):
                            i.range = 5
                            i.w_qty = 2
                        elif(i.item_description == "DAF TURBIDITY SENSOR"):
                            i.flow = 1
                            i.w_qty = 2
                        elif(i.item_description == "DAF SLUDGE PUMP"):
                            dafsludge=int(-1 * round((m.flow/24)*0.15) // 5 * -5)
                            i.flow=dafsludge
                            i.range=1.5
                            i.w_qty=1
                            i.sb_qty=1
                        elif(i.item_description=="DAF FEED PUMP"):
                            i.flow=round(m.flow/24)
                            i.range=m.tank_height/10
                            i.w_qty=1
                            i.sb_qty=1
                        elif(i.item_description == "DAF BUBBLE GENERATION PUMP"):
                            i.flow=round((m.flow/24)*0.3)
                            if(round((m.flow/24)*0.3)>42):
                                i.flow=round((m.flow/24)*0.3)/2
                            i.range=0.5
                            i.w_qty=1
                            i.sb_qty=1
                        elif(i.item_description == "DAF DOSING PUMP-1"):
                            i.flow=50
                            i.w_qty=1
                            i.ssb_qty=1
                        elif(i.item_description == "DAF DOSING PUMP-2"):
                            i.flow=50
                            i.w_qty=1
                            i.ssb_qty=1
                        elif(i.item_description == "DAF DOSING PUMP-1 FRAME"):
                            i.flow=50
                        elif(i.item_description == "DAF DOSING PUMP-2 FRAME"):
                            i.flow=50
                        elif(i.item_description == "DAF DOSING TANK-1"):
                            i.flow=1200
                            i.w_qty=1
                        elif(i.item_description == "DAF DOSING TANK-2"):
                            i.flow=1200
                            i.w_qty=1
                        elif(i.item_description == "DAF DOSING TANK-1 FRAME"):
                            i.flow=1200
                            i.w_qty=1
                        elif(i.item_description == "DAF DOSING TANK-2 FRAME"):
                            i.flow=1200
                            i.w_qty=1
                        elif(i.item_description == "BIO BLOWER"):
                            if(m.seperate_blower_for_equalization_tank == 1):
                                i.flow=round(m.bio_blower)
                                i.range = (m.tank_height +  0.5)/10
                                i.w_qty = m.total_blower
                                i.sb_qty = 1
                            else:
                                i.flow=round(m.each_blower)
                                i.range = (m.tank_height +  0.5)/10
                                i.w_qty = m.total_blower
                                i.sb_qty = 1
                        elif(i.renamed == "ELECTROMAGNETIC FLOWMETER"):
                            i.flow = round(m.flow/24,2)
                            i.w_qty =1
                        elif(i.item_description == "DNT FLOW MIXER"):
                            i.flow = 1
                            if(self.flow>2500):
                                vav = (self.flow/2500)
                                va=int(-1 * float(vav) // 1 * -1)
                            else:
                                va = 1
                            i.w_qty = va
                        elif(i.item_description == "DO SENSOR"):
                            i.flow = 1
                            # i.w_qty = m.no_of_bio_tanks
                            i.w_qty=1
                        elif(i.item_description == "DOI DO SENSOR"):
                            i.flow = 1
                            i.w_qty = m.no_of_bio_tanks
                        elif(i.renamed == "LEVEL TRANSMITTER"):
                            i.flow =1
                            i.range = m.tank_height
                            if(i.item_description=="LPS LEVEL TRANSMITTER"):
                                i.w_qty=0
                            elif(i.item_description=="NT LEVEL TRANSMITTER"):
                                i.w_qty=1
                        elif(i.renamed == "LEVEL FLOAT"):
                            i.flow =1
                            if(i.item_description=="LPS LEVEL FLOAT"):
                                i.w_qty=2
                            elif(i.item_description=="DAF LEVEL FLOAT" or i.item_description=="SRS LEVEL FLOAT"):
                                i.w_qty=1
                            elif(i.item_description=="NT LEVEL FLOAT"):
                                i.w_qty=1
                        elif(i.item_description == "LIFTING HOIST"):
                            i.w_qty = 3
                        elif(i.item_description == "BIO LATERAL"):
                            i.w_qty = float(m.ott_laterals) * float(m.ott_lateral_size)
                            i.range = "AR"+str(m.ott_lateral_size)
                            i.unit_price = float(m.currency_value)*1.1*(self.eur+2)
                            i.total_price = (i.w_qty * i.unit_price)
                if("Ammonia Striper" in selected_s):
                    bb = ['AMMONIA TOWER','BLOWER FAN','PALL RINGS','PH SENSOR','DOSING PUMP']
                    vs = ["AMMONIA TOWER","AIR BLOWER","PALL RINGS", "PH SENSOR","DOSING PUMP"]
                    for i in range(len(bb)):
                        self.append('pre_treatment_table', {
                            "item_description":bb[i],
                            "renamed":vs[i],
                            "system":"Ammonia Striper"
                        })
                        
                    dia=0
                    qq=0
                    dt_cost=0
                    bf_cost=0
                    bf_flow=0
                    pall_ring_qty=0
                    if(self.flow>=150 and self.flow<=600):dia=1;qq=1
                    elif(self.flow>600 and self.flow<=1000):dia=1.4;qq=1
                    elif(self.flow>1000 and self.flow<=1600):dia=1.8;qq=1
                    elif(self.flow>1600 and self.flow<=2500):dia=2.2;qq=1
                    elif(self.flow>2500 and self.flow<=3200):dia=1.8;qq=2
                    elif(self.flow>3200 and self.flow<=5000):dia=2.2;qq=2
                    elif(self.flow>5000 and self.flow<=7500):dia=2.2;qq=3
                    elif(self.flow>7500 and self.flow<=10000):dia=2.2;qq=4
                    
                    if(dia==1):dt_cost=230000;bf_cost=79000;bf_flow=1000;pall_ring_qty=1.96
                    elif(dia==1.4):dt_cost=290000;bf_cost=89000;bf_flow=1550;pall_ring_qty=3.85
                    elif(dia==1.8):dt_cost=375000;bf_cost=90000;bf_flow=2800;pall_ring_qty=6.35
                    elif(dia==2.2):dt_cost=475000;bf_cost=150000;bf_flow=4200;pall_ring_qty=9.5
                    for i in self.pre_treatment_table:
                        if(i.item_description == "AMMONIA TOWER"):
                            i.flow=self.flow
                            i.range = dia
                            i.w_qty = qq
                            i.unit_price = dt_cost
                            i.total_price = dt_cost*qq
                            
                        elif(i.item_description == "BLOWER FAN"):
                            i.flow=self.flow
                            i.range = bf_flow
                            i.w_qty = qq
                            i.unit_price = bf_cost
                            i.total_price = bf_cost*qq
                        
                        elif(i.item_description == "PALL RINGS"):
                            pall_ring=frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='PRPP25X25' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            i.flow=self.flow
                            i.w_qty = qq*pall_ring_qty
                            i.unit_price = pall_ring[0].base_rate if pall_ring else 0
                            i.total_price = pall_ring[0].base_rate*(qq*pall_ring_qty) if pall_ring else 0
                            
                        elif(i.item_description == "DOSING PUMP"):
                            fl=self.flow*0.04
                            i.flow = int(-1 * fl // 50 * -50)
                            i.w_qty = qq
                            i.sb_qty=1
                            
                        elif(i.item_description == "PH SENSOR"):
                            i.w_qty = qq
                            i.flow = 1
                            
                    sulcip=[]
                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='LANISOSS30440X403MM' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                        if(g.base_rate>0):
                            sulcip.append(g.base_rate)
                    for vs in self.pre_treatment_table:
                        if(vs.item_description == "DOSING PUMP"):
                            w_qty1 = (vs.w_qty + vs.sb_qty) * 2.5
                    self.append('pre_treatment_table', {
                        "item_description":"DOSING PUMP FRAME",
                        "flow":50,
                        "w_qty":w_qty1,
                        "unit_price":sulcip[0],
                        "total_price" : sulcip[0] * w_qty1,
                        "system":"Ammonia Striper"
                    })
                    
                for i in self.pre_treatment_table:
                
                    if(i.item_description=="DOSING PUMP"):
                        dgt_rate_query=frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='"+str(i.renamed)+"' and flow>='"+str(i.flow)+"' and flow<='"+str(i.flow+10)+"'",as_dict=1)
                        for k in dgt_rate_query:
                            for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                i.unit_price=g.base_rate
                                if(i.sb_qty is None):
                                    i.sb_qty = 0
                                if(i.w_qty is None):
                                    i.w_qty = 0
                                if(i.ssb_qty is None):
                                    i.ssb_qty = 0
                                i.total_price=(i.w_qty+i.sb_qty+i.ssb_qty)*i.unit_price
                        
                ardiff=[]
                for i in self.pre_treatment_table:
                    if(i.renamed == 'PH SENSOR'):
                        if(i.flow==0):
                            pass
                        else:
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='"+str(i.renamed)+"' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    ardiff.append({
                                        'item_d':i.item_description,
                                        'item_description':k.item_description,
                                        'rate':g.base_rate
                                    })
                
                for i in self.pre_treatment_table:
                    if(i.sb_qty is None):
                        i.sb_qty = 0
                    if(i.w_qty is None):
                        i.w_qty = 0
                    if(i.ssb_qty is None):
                        i.ssb_qty = 0
                    for j in ardiff:
                        if(str(i.item_description) == str(j['item_d'])):
                            i.unit_price=j['rate']
                            i.total_price=(i.w_qty+i.sb_qty+i.ssb_qty)*i.unit_price
                #bio calculation
                #belt press code starting
                if("Belt Press" in selected_s):
                    belt=["BELT POLY UNIT MODEL", "BELT FEED PUMP", "BELT WASHING PUMP","BELT FLOCCULATION SKID"]
                    belt_renamed=["BELT POLY UNIT MODEL", "SURFACE MOUNTED PUMP", "SURFACE MOUNTED PUMP","FLOCCULATION"]
                    for i in range(len(belt)):
                        sb=0
                        ssb=0
                        qq2=1
                        qq=self.without
                        if(self.withcheck==1):
                            qq=self.with_b
                        if(qq>11):
                            qq1=qq/11
                            qq2=int(-1 * float(qq1) // 1 * -1)
                        if(belt[i]=="BELT FEED PUMP"):sb=1
                        elif(belt[i]=="BELT DOSING PUMP"):ssb=1
                        self.append('pre_treatment_table', {
                            "item_description":belt[i],
                            "renamed":belt_renamed[i],
                            "w_qty":qq2,
                            "sb_qty":sb,
                            "ssb_qty":ssb,
                            "system":"Belt Press"
                            })
                    for k in self.pre_treatment_table:
                        if(self.withcheck==1):
                            if(self.with_b>0 and self.with_b<=2.5):
                                # btvalue=500
                                if(k.item_description == "BELT POLY UNIT MODEL"):k.flow=1;k.range = "BSB 600"
                                elif(k.item_description == "BELT FLOCCULATION SKID"):k.flow = 2.5;k.range = 4
                                elif(k.item_description == "BELT FEED PUMP"):k.flow = 2.5;k.range = 4
                                elif(k.item_description == "BELT WASHING PUMP"):k.flow = 4;k.range = 4
                                elif(k.item_description == "BELT DOSING PUMP"):k.flow = 600
                            elif(self.with_b>2.5 and self.with_b<=4.5):
                                # btvalue=800
                                if(k.item_description == "BELT POLY UNIT MODEL"):k.flow=1;k.range = "BSB 600"
                                elif(k.item_description == "BELT FEED PUMP"):k.flow = 4.5;k.range = 4
                                elif(k.item_description == "BELT FLOCCULATION SKID"):k.flow = 4.5;k.range = 4
                                elif(k.item_description == "BELT WASHING PUMP"):k.flow = 5.9;k.range = 4
                                elif(k.item_description == "BELT DOSING PUMP"):k.flow = 1100
                            elif(self.with_b>4.5):
                                # btvalue=1300
                                if(k.item_description == "BELT POLY UNIT MODEL"):k.flow=1;k.range = "BSB 1200"
                                elif(k.item_description == "BELT FEED PUMP"):k.flow = 16;k.range = 4
                                elif(k.item_description == "BELT FLOCCULATION SKID"):k.flow = 16;k.range = 4
                                elif(k.item_description == "BELT WASHING PUMP"):k.flow = 8.8;k.range = 4
                                elif(k.item_description == "BELT DOSING PUMP"):k.flow = 2500
                        else:
                            if(self.without>0 and self.without<=2.5):
                                # btvalue=500
                                if(k.item_description == "BELT POLY UNIT MODEL"):k.flow=1;k.range = "BSB 600"
                                elif(k.item_description == "BELT FEED PUMP"):k.flow = 2.5;k.range = 4
                                elif(k.item_description == "BELT FLOCCULATION SKID"):k.flow = 2.5;k.range = 4
                                elif(k.item_description == "BELT WASHING PUMP"):k.flow = 4;k.range = 4
                                elif(k.item_description == "BELT DOSING PUMP"):k.flow = 600
                            elif(self.without>2.5 and self.without<=4.5):
                                # btvalue=800
                                if(k.item_description == "BELT POLY UNIT MODEL"):k.flow=1;k.range = "BSB 600"
                                elif(k.item_description == "BELT FEED PUMP"):k.flow = 4.5;k.range = 4
                                elif(k.item_description == "BELT FLOCCULATION"):k.flow = 4.5;k.range = 4
                                elif(k.item_description == "BELT WASHING PUMP"):k.flow = 5.9;k.range = 4
                                elif(k.item_description == "BELT DOSING PUMP"):k.flow = 1100
                            elif(self.without>4.5):
                                # btvalue=1300
                                if(k.item_description == "BELT POLY UNIT MODEL"):k.flow=1;k.range = "BSB 1200"
                                elif(k.item_description == "BELT FEED PUMP"):k.flow = 16;k.range = 4
                                elif(k.item_description == "BELT FLOCCULATION SKID"):k.flow = 16;k.range = 4
                                elif(k.item_description == "BELT WASHING PUMP"):k.flow = 8.8;k.range = 4
                                elif(k.item_description == "BELT DOSING PUMP"):k.flow = 2500
                ##belt press coding ending
                ##screw press coding starts
                if("Screw Press" in selected_s):
                    screw=["SCREW POLY UNIT MODEL", "SCREW FEED PUMP","SCREW FLOCCULATION SKID"]
                    ssv=["SCREW POLY UNIT MODEL","SURFACE MOUNTED PUMP","FLOCCULATION"]
                    for vs in range(len(screw)):
                        sb=0
                        ssb=0
                        if(screw[vs]=="SCREW FEED PUMP"):sb=1
                        elif(screw[vs]=="SCREW DOSING PUMP"):ssb=1
                        self.append("pre_treatment_table",{
                            "item_description":screw[vs],
                            "renamed":ssv[vs],
                            "w_qty":1,
                            "sb_qty":sb,
                            "ssb_qty":ssb,
                            "flow":1,
                            "system":"Screw Press"
                        })
                    for k in self.pre_treatment_table:
                        if(self.withcheck==1):
                            if(self.with_b>0 and self.with_b<=3):
                                # btvalue=3
                                if(k.item_description == "SCREW FEED PUMP"):k.flow = 3;k.range = 4
                                elif(k.item_description == "SCREW FLOCCULATION SKID"):k.flow = 3;k.range = 4
                                elif(k.item_description == "SCREW DOSING PUMP"):k.flow=1100
                            elif(self.with_b>3 and self.with_b<=5):
                                # btvalue=5
                                if(k.item_description == "SCREW FEED PUMP"):k.flow = 5;k.range = 4
                                elif(k.item_description == "SCREW FLOCCULATION SKID"):k.flow = 5;k.range = 4
                                elif(k.item_description == "SCREW DOSING PUMP"):k.flow=1300
                            elif(self.with_b>5 and self.with_b<=10):
                                # btvalue=10
                                if(k.item_description == "SCREW FEED PUMP"):k.flow = 10;k.range = 4
                                elif(k.item_description == "SCREW FLOCCULATION SKID"):k.flow = 10;k.range = 4
                                elif(k.item_description == "SCREW DOSING PUMP"):k.flow=1550
                        else:
                            if(self.without>0 and self.without<=3):
                                # btvalue=3
                                if(k.item_description == "SCREW FEED PUMP"):k.flow = 3;k.range = 4
                                elif(k.item_description == "SCREW FLOCCULATION SKID"):k.flow = 3;k.range = 4
                                elif(k.item_description == "SCREW DOSING PUMP"):k.flow=1100
                            elif(self.without>3 and self.without<=5):
                                # btvalue=5
                                if(k.item_description == "SCREW FEED PUMP"):k.flow = 5;k.range = 4
                                elif(k.item_description == "SCREW FLOCCULATION SKID"):k.flow = 5;k.range = 4
                                elif(k.item_description == "SCREW DOSING PUMP"):k.flow=1300
                            elif(self.without>5 and self.without<=10):
                                # btvalue=10
                                if(k.item_description == "SCREW FEED PUMP"):k.flow = 10;k.range = 4
                                elif(k.item_description == "SCREW FLOCCULATION SKID"):k.flow = 10;k.range = 4
                                elif(k.item_description == "SCREW DOSING PUMP"):k.flow=1550
                ##screww press coding ends
                
                #do_increase_system
                if("DO increase system" in selected_s):
                    do_increase=["DOI BLOWER PIPE","DOI DIFFUSER PIPE","DOI EMFM","DOI DIFFUSER","DOI DO SENSOR"]
                    do_renamed = ["PIPES","PIPES","ELECTROMAGNETIC FLOWMETER","DIFFUSER","DO SENSOR"]
                    for vs in range(len(do_increase)):
                        if("DO increase system" in selected_s):
                            self.append("pre_treatment_table",{
                                "item_description":do_increase[vs],
                                "renamed":do_renamed[vs],
                                "w_qty":1,
                                "system":"DO increase system"
                            })
                
                    for v in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(self.project_startup_sheet)+"'",as_dict=1):
                        for i in self.pre_treatment_table:
                            if(i.item_description == "DOI BLOWER"):
                                i.range = v.do_increase_blower_model
                                i.w_qty = 1
                            elif(i.item_description == "DOI BLOWER PIPE"):
                                i.range = v.do_increase_blower_size
                                i.w_qty = v.do_increase_blower_pipe_length
                            elif(i.item_description == "DOI DIFFUSER PIPE"):
                                i.range = v.do_increase_diffuser_pipe_size
                                i.w_qty = v.do_increase_diffuser_pipe_length
                            elif(i.item_description == "DOI EMFM"):
                                i.flow = round(v.flow/24,2)
                                i.w_qty =1
                            elif(i.item_description == "DOI DIFFUSER"):
                                i.flow = 1
                                i.range = 0
                                value_w_qty = (float(v.diffuser_dt)+float(v.diffuser_srs)+float(v.diffuser_cft)+float(v.diffuser_nt))
                                vas=int(-1 * float(value_w_qty) // 5 * -5)
                                i.w_qty = vas
                
                ##fittings table
                for v in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    fitarr=[]
                    fittings = ["SCREW ROD", "NUT", "WASHER","ROPE", "D-CLAMP", "D-SHACKLE","GUIDE PIPE","BOLT","NUT","WASHER", "SCREW ROD", "NUT", "WASHER", "L-ANGLE","THIMBLE"]
                    item = ["TRISOSS304M16BSP","NTISOSS304M16HN","WSISOSS304M162MMPW","RISOSS304M6WW", "CLMISOSS304M6", "SHAISOSS304M6","PASMESS316S10DN50-2INERW","BTISOSS304M1265MMFTHT","NTISOSS304M12HN","WSISOSS304M122MMPW", "TRISOSS304M10BSP", "NTISOSS304M10HN", "WSISOSS304M102MMPW", "LANISOSS30450X505MM","TMBISOSS304M6"]
                    self.fittings_table=[]
                    for i in range(len(fittings)):
                        self.append("fittings_table",{
                            "item_description":fittings[i],
                            "item_code":item[i]
                        })
                work_qty=1
                tkt_hei=v.tank_height + 0.5
                for z in self.pre_treatment_table:
                    if(z.renamed == "SUBMERSIBLE PUMP"):
                        if(z.w_qty is None):
                            z.w_qty=0
                        if(z.sb_qty is None):
                            z.sb_qty=0
                
                for y in self.fittings_table:
                    if(y.item_description == "ROPE"):y.w_qty=(tkt_hei+7)*(work_qty)
                    elif(y.item_description == "D-CLAMP"):y.w_qty=3*(work_qty)
                    elif(y.item_description == "D-SHACKLE"):y.w_qty=(work_qty)
                    elif(y.item_description == "SCREW ROD"):y.w_qty=(0.15*4)*(work_qty)
                    elif(y.item_description == "NUT"):
                        y.w_qty=4*(work_qty)
                        if(y.item_code=="NTISOSS304M12HN"):y.w_qty=2*(work_qty)
                    elif(y.item_description == "WASHER"):y.w_qty=4*(work_qty)
                    elif(y.item_description == "L-ANGLE"):y.w_qty=1.5*(work_qty)
                    elif(y.item_description=="BOLT"):y.w_qty=2*(work_qty)
                    elif(y.item_description=="GUIDE PIPE"):y.w_qty=(tkt_hei*2)*(work_qty)
                    elif(y.item_description=="THIMBLE"):y.w_qty=work_qty
                
                for j in self.fittings_table:
                    if(j.w_qty is None):
                        j.w_qty=0
                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(j.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                        j.amount = round(j.w_qty*g.base_rate,2)
                
                subfit=0
                for j in self.fittings_table:
                    subfit=subfit+j.amount
                
                self.fittings_total = subfit
                for k in self.pre_treatment_table:
                    if(k.renamed == "FITTINGS"):
                        k.w_qty=2
                        k.unit_price = self.fittings_total
                        k.total_price = k.unit_price*k.w_qty
                        
                arblow=[]
                # for i in self.pre_treatment_table:
                #     if(i.renamed == 'OTT LATERAL'):
                #         if(i.range==0):
                #             pass
                #         else:
                #             for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='"+str(i.renamed)+"' and model='"+str(i.range)+"'",as_dict=1):
                #                 for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                #                     arblow.append({
                #                         'model':i.range,
                #                         'item_description':k.item_description,
                #                         'rate':g.base_rate
                #                     })
                ardiff = []
                arbub = []
                arrper = []
                arrpipe = []
                diff = []
                for i in self.pre_treatment_table:
                    if(i.renamed in ['TURBIDITY SENSOR','PH SENSOR','FLOW MIXER','DO SENSOR','LEVEL FLOAT','LEVEL TRANSMITTER']):
                        if(i.flow==0):
                            pass
                        else:
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='"+str(i.renamed)+"' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    ardiff.append({
                                        'item_d':i.item_description,
                                        'item_description':k.item_description,
                                        'rate':g.base_rate
                                    })
                    elif(i.renamed in ['PRESSURE TRANSMITTER','PRESSURE GAUGE']):
                        addrange=float(i.range)+10
                        for k in frappe.db.sql("SELECT item_code,item_description,name,range1 from `tabChild Fetch Items` where item_description='"+str(i.renamed)+"'",as_dict=1):
                            if(float(k.range1)>=float(i.range) and float(k.range1)<=float(addrange)):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    arrper.append({
                                        'item_d':i.item_description,
                                        'item_description':k.item_description,
                                        'rate':g.base_rate
                                    })
                    elif(i.renamed == 'PIPES'):
                        for k in frappe.db.sql("SELECT item_code,weight FROM `tabWeight Template` WHERE process_size='"+str(i.range)+"' and sch='SCH-05'",as_dict=1):
                            for g in frappe.db.sql("SELECT `tabPurchase Order`.`creation`,`tabPurchase Order Item`.`base_rate`,`tabPurchase Order Item`.`parent` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' and `tabPurchase Order Item`.`base_rate`>0 ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                to_total=float(g.base_rate)
                                arrpipe.append({
                                    'item_d':i.item_description,
                                    'item_description':k.item_description,
                                    'rate':to_total
                                })
                    elif(i.renamed in ['DIFFUSER','BELT POLY UNIT MODEL','SCREW POLY UNIT MODEL']):
                        for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='"+str(i.renamed)+"' and flow='1'",as_dict=1):
                            for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                diff.append({
                                    'item_d':i.item_description,
                                    'item_description':k.item_description,
                                    'rate':g.base_rate,
                                })
                    elif(i.renamed == "FLOCCULATION"):
                    #     if(i.flow<=5):
                    #         fl=0.1
                    #     else:
                    #         fl=0.25
                        fl=0.1
                        price_ar=[]
                        for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='FLOCCULATION"+str(fl)+"' ",as_dict=1):
                            for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                price_ar.append(rate.base_rate)
                        qq2=1
                        if(i.item_description=="BELT FLOCCULATION SKID"):
                            qq=self.without
                            if(self.withcheck==1):
                                qq=self.with_b
                            if(qq>11):
                                qq1=qq/11
                                qq2=int(-1 * float(qq1) // 1 * -1)
                        
                        i.w_qty=qq2
                        i.unit_price=sum(price_ar)
                        i.total_price=sum(price_ar)*qq2
                    elif(i.renamed == "DAF DOSING PUMP-1 FRAME" or i.renamed == "DAF DOSING PUMP-2 FRAME"):
                        dafdos=[]
                        for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='LANISOSS30440X403MM' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                            if(g.base_rate>0):
                                dafdos.append(g.base_rate)
                        i.w_qty = 2 * 2.5
                        i.unit_price = dafdos[0]
                        i.total_price = dafdos[0] * 2 * 2.5
                    elif(i.renamed == 'DAF DOSING TANK-1' or i.renamed == 'DAF DOSING TANK-2'):
                        cipdosetank=[]
                        addflow=tnk1+1000
                        for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='TANK' and flow>='1200' and flow<='"+str(addflow)+"'",as_dict=1):
                            for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                cipdosetank.append(g.base_rate)
                        i.w_qty = 1
                        i.unit_price = cipdosetank[0]
                        i.total_price = cipdosetank[0] * 1
                    elif(i.renamed == 'DAF DOSING TANK-1 FRAME' or i.renamed == 'DAF DOSING TANK-2 FRAME'):
                        price_ar=[]
                        for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='1200 LITRES TANK FRAME'",as_dict=1):
                            for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                price_ar.append(rate.base_rate)
                        i.w_qty = 1
                        i.unit_price = sum(price_ar)
                        i.total_price = sum(price_ar) * 1
                    elif(i.renamed in ["LIFTING HOIST","LIFTING HOIST BASE"]):
                        bom='BOM-LIFTING HOIST BASE-002'
                        if(i.renamed=="LIFTING HOIST"):
                            bom='BOM-LIFTING HOIST-002'
                        rate_from_bom=[]
                        for bb in frappe.db.sql("SELECT distinct(name),item_code,parent,stock_qty from `tabBOM Explosion Item` where parent='"+str(bom)+"' ",as_dict=1):
                            for rate in frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,`tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(bb.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                rate_from_bom.append(rate.base_rate*bb.stock_qty)
                        i.w_qty=1
                        i.unit_price=sum(rate_from_bom)
                        i.total_price=sum(rate_from_bom)*i.w_qty
                    elif(i.renamed in ['BUBBLE GENERATION PUMP','SUBMERSIBLE PUMP','SURFACE MOUNTED PUMP','DOSING PUMP','TANK','ELECTROMAGNETIC FLOWMETER']):
                        if(i.flow!=None):
                            addflow=float(i.flow)+25
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='"+str(i.renamed)+"' and flow>='"+str(i.flow)+"' and flow<='"+str(addflow)+"' ",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    arbub.append({
                                        'item_d':i.item_description,
                                        'item_description':k.item_description,
                                        'rate':g.base_rate
                                    })
                    
                for i in self.pre_treatment_table:
                    if(i.sb_qty is None):
                        i.sb_qty = 0
                    if(i.w_qty is None):
                        i.w_qty = 0
                    if(i.ssb_qty is None):
                        i.ssb_qty = 0
                    for j in ardiff:
                        if(str(i.item_description) == str(j['item_d'])):
                            i.unit_price=j['rate']
                            i.total_price=(i.w_qty+i.sb_qty+i.ssb_qty)*i.unit_price
                    for j in arblow:
                        if(str(i.range) == str(j['model'])):
                            i.unit_price=j['rate']
                            i.total_price=(i.w_qty+i.sb_qty+i.ssb_qty)*i.unit_price
                    for j in arbub:
                        if(str(i.item_description) == str(j['item_d'])):
                            i.unit_price=j['rate']
                            i.total_price=(i.w_qty+i.sb_qty+i.ssb_qty)*i.unit_price
                    for j in arrper:
                        if(str(i.item_description) == str(j['item_d'])):
                            i.unit_price=j['rate']
                            i.total_price=(i.w_qty+i.sb_qty+i.ssb_qty)*i.unit_price
                    for j in arrpipe:
                        if(str(i.item_description) == str(j['item_d'])):
                            i.unit_price=j['rate']
                            i.total_price=(i.w_qty+i.sb_qty+i.ssb_qty)*i.unit_price
                    for j in diff:
                        if(str(i.item_description) == str(j['item_d'])):
                            i.unit_price=j['rate']
                            i.total_price=float(i.w_qty) * float(i.unit_price)
                    if(i.item_description in ["BIO BLOWER","EQT BLOWER"]):
                        fl=i.flow
                        cost=0
                        if(fl>0 and fl<=200):
                            cost=275000
                        elif(fl>200 and fl<=400):
                            cost=360000
                        elif(fl>400 and fl<=800):
                            cost=440000
                        elif(fl>800 and fl<=1200):
                            cost=550000
                        elif(fl>1200 and fl<=1600):
                            cost=670000
                        elif(fl>1600 and fl<=2100):
                            cost=670000
                        elif(fl>2100):
                            cost=1125000
                        # motor_cost for bio_blower and eq_blower
                        kw=0
                        motor_cost=0
                        bio_flow=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"each_blower")
                        if(frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"seperate_blower_for_equalization_tank")==1):
                            bio_flow=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"bio_blower")
                        
                        if(i.item_description=="EQT BLOWER"):bio_flow=frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"eq_blower")
                        tank_height = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"tank_height")
                        flow3min = bio_flow * 0.588578
                        bio_range = (tank_height + 0.5)/10
                        inchh2 = bio_range * 401.865
                        power = ((flow3min * inchh2)/(6356 * 0.67))/1.34
                        if(power<=0.045): kw=0.045; 
                        elif(power<=0.18): kw=0.18; 
                        elif(power<=0.37): kw=0.37; motor_cost=9622; 
                        elif(power<=0.55): kw=0.55; motor_cost=10476; 
                        elif(power<=0.75): kw=0.75; motor_cost=11117; 
                        elif(power<=1.1): kw=1.1; motor_cost=12078; 
                        elif(power<=1.5): kw=1.5; motor_cost=13547; 
                        elif(power<=2.2): kw=2.2; motor_cost=15789; 
                        elif(power<=3.7): kw=3.7; motor_cost=21503; 
                        elif(power<=4): kw=4; motor_cost=24888; 
                        elif(power<=5.5): kw=5.5; motor_cost=30800; 
                        elif(power<=7.5): kw=7.5; motor_cost=52931; 
                        elif(power<=11): kw=11; motor_cost=53813; 
                        elif(power<=15): kw=15; motor_cost=74261; 
                        elif(power<=18.5): kw=18.5; motor_cost=83169; 
                        elif(power<=22): kw=22; motor_cost=104988; 
                        elif(power<=30): kw=30; motor_cost=119441; 
                        elif(power<=37): kw=37; motor_cost=170992; 
                        elif(power<=45): kw=45; motor_cost=249535; 
                        elif(power<=55): kw=55; motor_cost=286980; 
                        elif(power<=75): kw=75; motor_cost=330045; 
                        elif(power<=90): kw=90; motor_cost=387308; 
                        elif(power<=110): kw=110; motor_cost=471705; 
                        elif(power<=160): kw=160; motor_cost=516345;
                        
                        if(frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"type_of_blower")!="Screw"):
                            i.unit_price=cost
                            i.motor_cost = motor_cost*(i.w_qty+i.sb_qty+i.ssb_qty)
                            i.total_price=(i.unit_price)*(i.w_qty+i.sb_qty+i.ssb_qty)+i.motor_cost
                        else:
                            i.unit_price=0
                            i.total_price=0
                        
                
                ##bio_full_system
                array=[]
                for i in self.bio_full_system:
                    arr=[]
                    for j in self.pre_treatment_table:
                        if(i.item_description==j.system):
                            if(j.total_price!=None):
                                arr.append(0)
                    array.append({"system":str(i.item_description),"amount":0})
                
                for i in self.bio_full_system:
                    if(i.pipes_per is None):
                        i.pipes_per=0
                    if(i.w_qty is None or i.w_qty==0):
                        if(i.item_description == "DAF (Dissolved Air Flotation)"):
                            if(self.flow<1152):
                                i.w_qty=1
                            elif(self.flow>1152 and self.flow<=1728):
                                i.w_qty=1
                            elif(self.flow>1728 and self.flow<=2300):
                                i.w_qty=2
                            elif(self.flow>2300):
                                i.w_qty=2
                            for k in self.pre_treatment_table:
                                if(k.item_description == "DAF BUBBLE GENERATION PUMP"):
                                    k.flow= float(((self.flow/24)*0.3)/i.w_qty)
                                    k.w_qty=i.w_qty
                                    if(float(k.flow)<=1):
                                        unprice= 140000 + 7500
                                    elif(float(k.flow)<=1.5):
                                        unprice=170000 + 10000
                                    elif(float(k.flow)<=3.0):
                                        unprice=201000 + 15000
                                    elif(float(k.flow)<=4.8):
                                        unprice=250000 + 20000
                                    elif(float(k.flow)<=8.0):
                                        unprice=350000 + 26000
                                    elif(float(k.flow)<=12.0):
                                        unprice=450000 + 31000
                                    elif(float(k.flow)<=15.0):
                                        unprice=517500 + 47000
                                    elif(float(k.flow)<=20.0):
                                        unprice=690000 + 56000
                                    elif(float(k.flow)<=42.0):
                                        unprice=775000 + 86000
                                    k.unit_price = unprice
                                    k.total_price = unprice * (k.w_qty + k.sb_qty)
                                elif(k.item_description == "DAF PRESSURE GAUGE"):
                                    k.w_qty=i.w_qty
                                    dbp=[]
                                    for ll in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='PRESSURE GAUGE' and flow>='1'",as_dict=1):
                                        for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(ll.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                            dbp.append(g.base_rate)
                                    if(dbp):
                                        k.unit_price = dbp[0]
                                        k.total_price = dbp[0] * k.w_qty
                                    else:
                                        k.unit_price = 0
                                        k.total_price = 0
                                elif(k.item_description == "DAF COMPOUND GAUGE"):
                                    k.w_qty=i.w_qty
                                    k.unit_price=4500
                                    k.total_price=4500 * k.w_qty
                                elif(k.item_description == "DAF AIR FLOWMETER"):
                                    k.w_qty=i.w_qty
                                    k.sb_qty=1
                                    k.unit_price=5000
                                    k.total_price= 5000 * (i.w_qty+1)
                                elif(k.item_description == "DAF SLUDGE PUMP"):
                                    k.flow= ((self.flow/24)*0.15)/i.w_qty
                                    k.w_qty=i.w_qty
                                    addflow=float(k.flow)+10
                                    dsp=[]
                                    for ll in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='SURFACE MOUNTED PUMP' and flow>='"+str(k.flow)+"' and flow<='"+str(addflow)+"' ",as_dict=1):
                                        for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(ll.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                            dsp.append(g.base_rate)
                                    if(dsp):
                                        k.unit_price = dsp[0]
                                        k.total_price = dsp[0] * k.w_qty
                                    else:
                                        k.unit_price=0
                                        k.total_price=0
                                    
                        elif(i.item_description == "Cooling Tower"):
                            if(self.flow<=750):
                                i.w_qty=1
                            elif(self.flow>750 and self.flow<1500):
                                i.w_qty=1
                            else:
                                i.w_qty = int(-1 * (self.flow/1500) // 1 * -1)
                        else:
                            i.w_qty=1
                    if(i.item_description in ["Rotary Brush Screener","Ammonia Striper","DAF (Dissolved Air Flotation)","Cooling Tower","Circular Clarifier System","Sludge Thickener with mech","Belt Press","Screw Press","Drum Screener"]):
                        mapping_bom=frappe.db.sql("SELECT distinct(`tabMapping BOM`.`name`)as 'name',parent,process_system,`tabProcess System Parameter Threshold`.`value` as val FROM `tabMapping BOM` INNER JOIN `tabProcess System Parameter Threshold` ON `tabMapping BOM`.`name`=`tabProcess System Parameter Threshold`.`parent` WHERE `tabMapping BOM`.`process_system`='"+str(i.item_description)+"'",as_dict=1)
                        if(mapping_bom):
                            for j in mapping_bom:
                                # if(j.process_system=="Circular Clarifier System"):
                                #     frappe.msgprint(str(j.name))
                                if(j.val == str(i.range)):
                                    rate_from_bom=[]
                                    for bb in frappe.db.sql("SELECT distinct(name),item_code,parent,stock_qty,stock_uom,total_weight,weight_per_unit,qty from `tabBOM Item` where parent='"+str(j.name)+"' ",as_dict=1):
                                        if(str(bb.item_code)[slice(3)]!="S60"):
                                            for rate in frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,`tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(bb.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                                rate_from_bom.append(rate.base_rate*bb.stock_qty)
                                        else:
                                            if(bb.total_weight>0):
                                                rate_from_bom.append(480*bb.total_weight)
                                            else:
                                                rate_from_bom.append(480*bb.weight_per_unit*bb.qty)
                                    for ii in array:
                                        if(i.item_description==ii["system"]):
                                            rate_from_bom.append(float(ii["amount"]))
                                    mar=1.05
                                    i.unit_price=round(sum(rate_from_bom)*mar,2)
                                    i.total_price=(round(sum(rate_from_bom)*mar,2))*i.w_qty
                                    i.bom_reference=j.name
                        elif(i.item_description == "Belt Press"):
                            qq2=1
                            qq=self.without
                            if(self.withcheck==1):
                                qq=self.with_b
                            if(qq>11):
                                qq1=qq/11
                                qq2=int(-1 * float(qq1) // 1 * -1)
                            rate_from_bom=[]
                            query=frappe.db.sql("SELECT item_code from `tabChild Fetch Items` where item_description='Belt Press' and range1>='"+str(i.range)+"' ",as_dict=1)
                            if(query):
                                for bb in query:
                                    for rate in frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,`tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(bb.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                        rate_from_bom.append(rate.base_rate)
                            totalbtp = round(rate_from_bom[0],2)
                            i.w_qty=qq2
                            i.unit_price=totalbtp*1.1
                            i.total_price=(totalbtp*1.1)*i.w_qty
                        
                        elif(i.item_description=="Screw Press"):
                            rate_from_bom=[]
                            rat_e=0
                            if(self.withcheck==1):
                                if(self.with_b>0 and self.with_b<=2):rat_e=1165000
                                elif(self.with_b>2 and self.with_b<=3):rat_e=1265000
                                elif(self.with_b>3 and self.with_b<=5):rat_e=1385000
                                elif(self.with_b>5 and self.with_b<=10):rat_e=1665000
                                elif(self.with_b>10 and self.with_b<=15):rat_e=2087000
                                elif(self.with_b>15 and self.with_b<=20):rat_e=2596000
                            else:
                                if(self.without>0 and self.without<=2):rat_e=1165000
                                elif(self.without>2 and self.without<=3):rat_e=1265000
                                elif(self.without>3 and self.without<=5):rat_e=1385000
                                elif(self.without>5 and self.without<=10):rat_e=1665000
                                elif(self.without>10 and self.without<=15):rat_e=2087000
                                elif(self.without>15 and self.without<=20):rat_e=2596000
                            totalsp = rat_e
                            i.unit_price=totalsp
                            i.total_price=(totalsp)*i.w_qty
                        else:
                            for ii in array:
                                if(i.item_description==ii["system"]):
                                    bio_pipe_cost=float(ii["amount"])*(i.pipes_per/100)
                                    i.unit_price=ii["amount"]
                                    i.total_price=(float(ii["amount"])+bio_pipe_cost)*i.w_qty
                    elif(i.item_description == "Lamella Settler"):
                        tank_he = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"tank_height")
                        lamella= ((self.flow/24)*4)/(tank_he-2)
                        # i.w_qty = lamella
                        i.w_qty=1
                        i.unit_price = 7600 * lamella
                        i.total_price = 7600 * lamella
                        i.pipes_per=0
                    elif(i.item_description=="Oil & grease trap"):
                        i.w_qty=1
                        i.unit_price=250000
                        i.total_price=250000*i.w_qty
                    elif(i.item_description == "Sludge Thickener"):
                        i.w_qty=1
                        i.unit_price=80000
                        i.total_price=80000*i.w_qty
                    else:
                        for ii in array:
                            if(i.item_description==ii["system"]):
                                bio_pipe_cost=float(ii["amount"])*(i.pipes_per/100)
                                i.unit_price=ii["amount"]
                                i.total_price=(float(ii["amount"])+bio_pipe_cost)*i.w_qty
                
                ##bio_full_system
                ##Chemical Treatment System
                bb = ["FEED PUMP", "SLUDGE PUMP", "ELECTROMAGNETIC FLOWMETER","AGITATOR", "PH SENSOR","LEVEL TRANSMITTER","PIPE FLOCCULATION","DOSING PUMP-1", "DOSING PUMP-2", "DOSING PUMP-3", "DOSING PUMP-4", "DOSING PUMP-5"]
                vs = ["SURFACE MOUNTED PUMP","SURFACE MOUNTED PUMP","ELECTROMAGNETIC FLOWMETER", "AGITATOR", "PH SENSOR","LEVEL TRANSMITTER","PIPE FLOCCULATION","DOSING PUMP", "DOSING PUMP", "DOSING PUMP", "DOSING PUMP", "DOSING PUMP"]
                self.cts_items=[]
                for i in range(len(bb)):
                    self.append('cts_items', {
                        "item_description":bb[i],
                        "renamed":vs[i]
                    })
                for m in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    for i in self.cts_items:
                        if(i.item_description == "PH SENSOR"):
                            i.w_qty = 1
                            i.flow = 1
                        elif(i.item_description == "LEVEL TRANSMITTER"):
                            i.flow =1
                            i.range = m.tank_height
                            i.w_qty = 1
                ardiff=[]
                flow = self.flow*0.1/1000
                fl=0
                if(flow>0 and flow<=0.1):fl=0.1
                elif(flow>0.1 and flow<=0.25):fl=0.25
                elif(flow>0.25 and flow<=0.5):fl=0.5
                elif(flow>0.5 and flow<=0.75):fl=0.75
                elif(flow>0.75 and flow<=1):fl=1
                cts_cap=frappe.db.sql("SELECT cts_capacity from `tabStartup Sheet` where name='"+str(self.project_startup_sheet)+"' ",as_dict=1)[0].cts_capacity
                for i in self.cts_items:
                    if(i.renamed=="PIPE FLOCCULATION"):
                        price_ar=[]
                        for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='FLOCCULATION"+str(fl)+"' ",as_dict=1):
                            for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                price_ar.append(rate.base_rate)
                        i.w_qty=1
                        i.unit_price=sum(price_ar)
                        i.total_price=sum(price_ar)
                    elif(i.item_description=="AGITATOR"):
                        i.flow=1
                        i.w_qty=4
                        i.unit_price=60000
                        i.total_price=i.unit_price*4
                    elif(i.renamed == 'PH SENSOR' or i.renamed == 'LEVEL TRANSMITTER'):
                        if(i.flow==0):
                            pass
                        else:
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='"+str(i.renamed)+"' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    ardiff.append({
                                        'item_d':i.item_description,
                                        'item_description':k.item_description,
                                        'rate':g.base_rate
                                    })
                    else:
                        if(i.item_description=="FEED PUMP" or i.item_description=="LAMELLA SETTLER"):
                            i.w_qty=1
                            i.sb_qty=1
                            i.flow=cts_cap/16
                        elif(i.item_description=="SLUDGE PUMP"):
                            i.w_qty=1
                            i.sb_qty=1
                            i.flow=round((cts_cap/16)*0.3,2)
                        elif(i.item_description == "ELECTROMAGNETIC FLOWMETER"):
                            i.flow=cts_cap/16
                            i.w_qty=1
                        elif(i.item_description in ["DOSING PUMP-1","DOSING PUMP-2","DOSING PUMP-3","DOSING PUMP-4","DOSING PUMP-5"]):
                            i.w_qty=1
                            if(i.item_description=="DOSING PUMP-1"):
                                i.ssb_qty=1
                            dp_cts=(cts_cap/16)*0.3
                            i.flow=int(-1 * dp_cts // 50 * -50)
                            
                        cts_rate_query=frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='"+str(i.renamed)+"' and flow>='"+str(i.flow)+"' and flow<='"+str(i.flow+10)+"'",as_dict=1)
                        for k in cts_rate_query:
                            for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                i.unit_price=g.base_rate
                                if(i.sb_qty is None):i.sb_qty = 0
                                if(i.w_qty is None):i.w_qty = 0
                                if(i.ssb_qty is None):i.ssb_qty = 0
                                i.total_price=(i.w_qty+i.sb_qty+i.ssb_qty)*i.unit_price
                    chedos=[]
                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='LANISOSS30440X403MM' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                        if(g.base_rate>0):
                            chedos.append(g.base_rate)
                    if(i.item_description == "DOSING PUMP-1"):
                        w_qty1 = i.w_qty * 2.5
                    elif(i.item_description == "DOSING PUMP-2"):
                        w_qty2 = i.w_qty * 2.5
                    elif(i.item_description == "DOSING PUMP-3"):
                        w_qty3 = i.w_qty * 2.5
                    elif(i.item_description == "DOSING PUMP-4"):
                        w_qty4 = i.w_qty * 2.5
                    elif(i.item_description == "DOSING PUMP-5"):
                        w_qty5 = i.w_qty * 2.5
                self.append('cts_items', {
                    "item_description":"DOSING PUMP-1 FRAME",
                    "flow":50,
                    "w_qty":w_qty1,
                    "unit_price":chedos[0],
                    "total_price" : chedos[0] * w_qty1
                })
                self.append('cts_items', {
                    "item_description":"DOSING PUMP-2 FRAME",
                    "flow":50,
                    "w_qty":w_qty2,
                    "unit_price":chedos[0],
                    "total_price" : chedos[0] * w_qty2
                })
                self.append('cts_items', {
                    "item_description":"DOSING PUMP-3 FRAME",
                    "flow":50,
                    "w_qty":w_qty3,
                    "unit_price":chedos[0],
                    "total_price" : chedos[0] * w_qty3
                })
                self.append('cts_items', {
                    "item_description":"DOSING PUMP-4 FRAME",
                    "flow":50,
                    "w_qty":w_qty4,
                    "unit_price":chedos[0],
                    "total_price" : chedos[0] * w_qty4
                })
                self.append('cts_items', {
                    "item_description":"DOSING PUMP-5 FRAME",
                    "flow":50,
                    "w_qty":w_qty5,
                    "unit_price":chedos[0],
                    "total_price" : chedos[0] * w_qty5
                })
                
                for i in self.cts_items:
                    if(i.sb_qty is None):i.sb_qty = 0
                    if(i.w_qty is None):i.w_qty = 0
                    if(i.ssb_qty is None):i.ssb_qty = 0
                    for j in ardiff:
                        if(str(i.item_description) == str(j['item_d'])):
                            i.unit_price=j['rate']
                            i.total_price=(i.w_qty+i.sb_qty+i.ssb_qty)*i.unit_price
                ## degasser
                bb = ['DEGASSER TOWER','BLOWER FAN','PALL RINGS','PH SENSOR','DOSING PUMP']
                vs = ["DEGASSER","AIR BLOWER","PALL RINGS", "PH SENSOR","DOSING PUMP"]
                self.dgt_items=[]
                for i in range(len(bb)):
                    self.append('dgt_items', {
                        "item_description":bb[i],
                        "renamed":vs[i]
                    })
                    
                dia=0
                qq=0
                dt_cost=0
                bf_cost=0
                bf_flow=0
                pall_ring_qty=0
                if(self.flow>=150 and self.flow<=600):dia=1;qq=1
                elif(self.flow>600 and self.flow<=1000):dia=1.4;qq=1
                elif(self.flow>1000 and self.flow<=1600):dia=1.8;qq=1
                elif(self.flow>1600 and self.flow<=2500):dia=2.2;qq=1
                elif(self.flow>2500 and self.flow<=3200):dia=1.8;qq=2
                elif(self.flow>3200 and self.flow<=5000):dia=2.2;qq=2
                elif(self.flow>5000 and self.flow<=7500):dia=2.2;qq=3
                elif(self.flow>7500 and self.flow<=10000):dia=2.2;qq=4
                
                if(dia==1):dt_cost=230000;bf_cost=79000;bf_flow=1000;pall_ring_qty=1.96
                elif(dia==1.4):dt_cost=290000;bf_cost=89000;bf_flow=1550;pall_ring_qty=3.85
                elif(dia==1.8):dt_cost=375000;bf_cost=90000;bf_flow=2800;pall_ring_qty=6.35
                elif(dia==2.2):dt_cost=475000;bf_cost=150000;bf_flow=4200;pall_ring_qty=9.5
                for i in self.dgt_items:
                    if(i.item_description == "DEGASSER TOWER"):
                        i.flow=self.flow
                        i.range = dia
                        i.w_qty = qq
                        i.unit_price = dt_cost
                        i.total_price = dt_cost*qq
                        
                    elif(i.item_description == "BLOWER FAN"):
                        i.flow=self.flow
                        i.range = bf_flow
                        i.w_qty = qq
                        i.unit_price = bf_cost
                        i.total_price = bf_cost*qq
                    
                    elif(i.item_description == "PALL RINGS"):
                        pall_ring=frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='PRPP25X25' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                        i.flow=self.flow
                        i.w_qty = qq*pall_ring_qty
                        i.unit_price = pall_ring[0].base_rate if pall_ring else 0
                        i.total_price = pall_ring[0].base_rate*(qq*pall_ring_qty) if pall_ring else 0
                        
                    elif(i.item_description == "DOSING PUMP"):
                        fl=self.flow*0.04
                        i.flow = int(-1 * fl // 50 * -50)
                        i.w_qty = qq
                        i.sb_qty=1
                        
                    elif(i.item_description == "PH SENSOR"):
                        i.w_qty = qq
                        i.flow = 1
                        
                sulcip=[]
                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='LANISOSS30440X403MM' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                    if(g.base_rate>0):
                        sulcip.append(g.base_rate)
                for vs in self.dgt_items:
                    if(vs.item_description == "DOSING PUMP"):
                        w_qty1 = (vs.w_qty + vs.sb_qty) * 2.5
                self.append('dgt_items', {
                    "item_description":"DOSING PUMP FRAME",
                    "flow":50,
                    "w_qty":w_qty1,
                    "unit_price":sulcip[0],
                    "total_price" : sulcip[0] * w_qty1
                })
                
                for i in self.dgt_items:
                
                    if(i.item_description=="DOSING PUMP"):
                        dgt_rate_query=frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='"+str(i.renamed)+"' and flow>='"+str(i.flow)+"' and flow<='"+str(i.flow+10)+"'",as_dict=1)
                        for k in dgt_rate_query:
                            for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                i.unit_price=g.base_rate
                                if(i.sb_qty is None):
                                    i.sb_qty = 0
                                if(i.w_qty is None):
                                    i.w_qty = 0
                                if(i.ssb_qty is None):
                                    i.ssb_qty = 0
                                i.total_price=(i.w_qty+i.sb_qty+i.ssb_qty)*i.unit_price
                        
                ardiff=[]
                for i in self.dgt_items:
                    if(i.renamed == 'PH SENSOR'):
                        if(i.flow==0):
                            pass
                        else:
                            for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='"+str(i.renamed)+"' and flow='1'",as_dict=1):
                                for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    ardiff.append({
                                        'item_d':i.item_description,
                                        'item_description':k.item_description,
                                        'rate':g.base_rate
                                    })
                
                for i in self.dgt_items:
                    if(i.sb_qty is None):
                        i.sb_qty = 0
                    if(i.w_qty is None):
                        i.w_qty = 0
                    if(i.ssb_qty is None):
                        i.ssb_qty = 0
                    for j in ardiff:
                        if(str(i.item_description) == str(j['item_d'])):
                            i.unit_price=j['rate']
                            i.total_price=(i.w_qty+i.sb_qty+i.ssb_qty)*i.unit_price
                ##PLC calculation
                plc_item=["PLC CPU", "MONITOR", "MODEM", "ETHERNET SWITCH", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE"]
                ml_item=['PLCCBOIPC6015-0010W10IOTIA2NIL24VDCNIL4GBUPTO 4 GBNILIP 20NILNIL','MNTAM7"-15"24VDCS-SPMWTWDVIMBWBES-S','PCAMDMAM4GPMNILNILSIMLAN','PCAENSAM1GB/ SPMUMS3NILNIL','HDMI3MM-MDP-HDMIAMPLC-MONI','POWER ADAPTERREPUTED230 VAC24 VDC2A50HZMONISUP','TSUSBCREPUTEDUSB-AB3METERTSM']
                
                ### PLC calculation
                ###kw calculation
                ddoc=self.mf_table
                if(self.mf_full_system):
                    ddoc=self.mf_full_system
                for mech in ddoc:
                    for elec in self.mf_electrical_items:
                        if(mech.item_description==elec.item_description):
                            if(mech.flow==None or mech.flow==""):
                                mech.flow=1
                            elif(mech.range==None or mech.range==""):
                                mech.range=1
                            theoritical_power = (float(mech.flow)/3600)*(float(mech.range)*10*10*10*10*10)/1000
                            pump_shaft_power = (theoritical_power/70)*100
                            absorbed_motor_power = (pump_shaft_power/90)*100
                            kw=0
                            if(absorbed_motor_power<=0.045):kw=0.045
                            elif(absorbed_motor_power<=0.18):kw=0.18
                            elif(absorbed_motor_power<=0.37):kw=0.37
                            elif(absorbed_motor_power<=0.55):kw=0.55
                            elif(absorbed_motor_power<=0.75):kw=0.75
                            elif(absorbed_motor_power<=1.1):kw=1.1
                            elif(absorbed_motor_power<=1.5):kw=1.5
                            elif(absorbed_motor_power<=2.2):kw=2.2
                            elif(absorbed_motor_power<=3.7):kw=3.7
                            elif(absorbed_motor_power<=4):kw=4
                            elif(absorbed_motor_power<=5.5):kw=5.5
                            elif(absorbed_motor_power<=7.5):kw=7.5
                            elif(absorbed_motor_power<=11):kw=11
                            elif(absorbed_motor_power<=15):kw=15
                            elif(absorbed_motor_power<=18.5):kw=18.5
                            elif(absorbed_motor_power<=22):kw=22
                            elif(absorbed_motor_power<=30):kw=30
                            elif(absorbed_motor_power<=37):kw=37
                            elif(absorbed_motor_power<=45):kw=45
                            elif(absorbed_motor_power<=55):kw=55
                            elif(absorbed_motor_power<=75):kw=75
                            elif(absorbed_motor_power<=90):kw=90
                            elec.kw=kw if elec.item_description!="PRE-FILTER" else elec.kw
                            if(kw>5.5):i.type="S/D FEEDER"
                            else:i.type="DOL FEEDER"
                ddoc=self.mbr_koch_table
                if(self.mbrk_full_system):
                    ddoc=self.mbrk_full_system
                for mech in ddoc:
                    for elec in self.mbr_electrical_items:
                        if(mech.item_description==elec.item_description):
                            if(mech.flow==None or mech.flow==""):
                                mech.flow=1
                            elif(mech.range==None or mech.range==""):
                                mech.range=1
                            theoritical_power = (float(mech.flow)/3600)*(float(mech.range)*10*10*10*10*10)/1000
                            pump_shaft_power = (theoritical_power/70)*100
                            absorbed_motor_power = (pump_shaft_power/90)*100
                            kw=0
                            if(absorbed_motor_power<=0.045):kw=0.045
                            elif(absorbed_motor_power<=0.18):kw=0.18
                            elif(absorbed_motor_power<=0.37):kw=0.37
                            elif(absorbed_motor_power<=0.55):kw=0.55
                            elif(absorbed_motor_power<=0.75):kw=0.75
                            elif(absorbed_motor_power<=1.1):kw=1.1
                            elif(absorbed_motor_power<=1.5):kw=1.5
                            elif(absorbed_motor_power<=2.2):kw=2.2
                            elif(absorbed_motor_power<=3.7):kw=3.7
                            elif(absorbed_motor_power<=4):kw=4
                            elif(absorbed_motor_power<=5.5):kw=5.5
                            elif(absorbed_motor_power<=7.5):kw=7.5
                            elif(absorbed_motor_power<=11):kw=11
                            elif(absorbed_motor_power<=15):kw=15
                            elif(absorbed_motor_power<=18.5):kw=18.5
                            elif(absorbed_motor_power<=22):kw=22
                            elif(absorbed_motor_power<=30):kw=30
                            elif(absorbed_motor_power<=37):kw=37
                            elif(absorbed_motor_power<=45):kw=45
                            elif(absorbed_motor_power<=55):kw=55
                            elif(absorbed_motor_power<=75):kw=75
                            elif(absorbed_motor_power<=90):kw=90
                            elec.kw=kw
                            if(kw>5.5):i.type="S/D FEEDER"
                            else:i.type="DOL FEEDER"
                ddoc=self.mbr_ovivo_table
                if(self.mbro_full_system):
                    ddoc=self.mbro_full_system
                for mech in ddoc:
                    for elec in self.ovivo_electrical_items:
                        if(mech.item_description==elec.item_description):
                            if(mech.flow==None or mech.flow==""):
                                mech.flow=1
                            elif(mech.range==None or mech.range==""):
                                mech.range=1
                            if(elec.item_description in mbr_ovivo_dos):
                                elec.kw=0.37
                                elec.type="DOL FEEDER"
                            else:
                                theoritical_power = (float(mech.flow)/3600)*(float(mech.range)*10*10*10*10*10)/1000
                                pump_shaft_power = (theoritical_power/70)*100
                                absorbed_motor_power = (pump_shaft_power/90)*100
                                kw=0
                                if(absorbed_motor_power<=0.045):kw=0.045
                                elif(absorbed_motor_power<=0.18):kw=0.18
                                elif(absorbed_motor_power<=0.37):kw=0.37
                                elif(absorbed_motor_power<=0.55):kw=0.55
                                elif(absorbed_motor_power<=0.75):kw=0.75
                                elif(absorbed_motor_power<=1.1):kw=1.1
                                elif(absorbed_motor_power<=1.5):kw=1.5
                                elif(absorbed_motor_power<=2.2):kw=2.2
                                elif(absorbed_motor_power<=3.7):kw=3.7
                                elif(absorbed_motor_power<=4):kw=4
                                elif(absorbed_motor_power<=5.5):kw=5.5
                                elif(absorbed_motor_power<=7.5):kw=7.5
                                elif(absorbed_motor_power<=11):kw=11
                                elif(absorbed_motor_power<=15):kw=15
                                elif(absorbed_motor_power<=18.5):kw=18.5
                                elif(absorbed_motor_power<=22):kw=22
                                elif(absorbed_motor_power<=30):kw=30
                                elif(absorbed_motor_power<=37):kw=37
                                elif(absorbed_motor_power<=45):kw=45
                                elif(absorbed_motor_power<=55):kw=55
                                elif(absorbed_motor_power<=75):kw=75
                                elif(absorbed_motor_power<=90):kw=90
                                elec.kw=kw
                                if(kw>5.5):i.type="S/D FEEDER"
                                else:i.type="DOL FEEDER"
                ddoc=self.cts_items
                if(self.cts_full_system):
                    ddoc=self.cts_full_system
                for mech in ddoc:
                    for elec in self.cts_electrical_items:
                        if(mech.item_description==elec.item_description):
                            if(mech.flow==None or mech.flow==""):
                                mech.flow=1
                            elif(mech.range==None or mech.range==""):
                                mech.range=1
                            theoritical_power = (float(mech.flow)/3600)*(float(mech.range)*10*10*10*10*10)/1000
                            pump_shaft_power = (theoritical_power/70)*100
                            absorbed_motor_power = (pump_shaft_power/90)*100
                            kw=0
                            if(absorbed_motor_power<=0.045):kw=0.045
                            elif(absorbed_motor_power<=0.18):kw=0.18
                            elif(absorbed_motor_power<=0.37):kw=0.37
                            elif(absorbed_motor_power<=0.55):kw=0.55
                            elif(absorbed_motor_power<=0.75):kw=0.75
                            elif(absorbed_motor_power<=1.1):kw=1.1
                            elif(absorbed_motor_power<=1.5):kw=1.5
                            elif(absorbed_motor_power<=2.2):kw=2.2
                            elif(absorbed_motor_power<=3.7):kw=3.7
                            elif(absorbed_motor_power<=4):kw=4
                            elif(absorbed_motor_power<=5.5):kw=5.5
                            elif(absorbed_motor_power<=7.5):kw=7.5
                            elif(absorbed_motor_power<=11):kw=11
                            elif(absorbed_motor_power<=15):kw=15
                            elif(absorbed_motor_power<=18.5):kw=18.5
                            elif(absorbed_motor_power<=22):kw=22
                            elif(absorbed_motor_power<=30):kw=30
                            elif(absorbed_motor_power<=37):kw=37
                            elif(absorbed_motor_power<=45):kw=45
                            elif(absorbed_motor_power<=55):kw=55
                            elif(absorbed_motor_power<=75):kw=75
                            elif(absorbed_motor_power<=90):kw=90
                            elec.kw=kw
                            if(kw>5.5):i.type="S/D FEEDER"
                            else:i.type="DOL FEEDER"
                ddoc=self.dgt_items
                if(self.dgt_full_system):
                    ddoc=self.dgt_full_system
                for mech in ddoc:
                    for elec in self.dgt_electrical_items:
                        if(mech.item_description==elec.item_description):
                            if(mech.flow==None or mech.flow==""):
                                mech.flow=1
                            elif(mech.range==None or mech.range==""):
                                mech.range=1
                            theoritical_power = (float(mech.flow)/3600)*(float(mech.range)*10*10*10*10*10)/1000
                            pump_shaft_power = (theoritical_power/70)*100
                            absorbed_motor_power = (pump_shaft_power/90)*100
                            kw=0
                            if(absorbed_motor_power<=0.045):kw=0.045
                            elif(absorbed_motor_power<=0.18):kw=0.18
                            elif(absorbed_motor_power<=0.37):kw=0.37
                            elif(absorbed_motor_power<=0.55):kw=0.55
                            elif(absorbed_motor_power<=0.75):kw=0.75
                            elif(absorbed_motor_power<=1.1):kw=1.1
                            elif(absorbed_motor_power<=1.5):kw=1.5
                            elif(absorbed_motor_power<=2.2):kw=2.2
                            elif(absorbed_motor_power<=3.7):kw=3.7
                            elif(absorbed_motor_power<=4):kw=4
                            elif(absorbed_motor_power<=5.5):kw=5.5
                            elif(absorbed_motor_power<=7.5):kw=7.5
                            elif(absorbed_motor_power<=11):kw=11
                            elif(absorbed_motor_power<=15):kw=15
                            elif(absorbed_motor_power<=18.5):kw=18.5
                            elif(absorbed_motor_power<=22):kw=22
                            elif(absorbed_motor_power<=30):kw=30
                            elif(absorbed_motor_power<=37):kw=37
                            elif(absorbed_motor_power<=45):kw=45
                            elif(absorbed_motor_power<=55):kw=55
                            elif(absorbed_motor_power<=75):kw=75
                            elif(absorbed_motor_power<=90):kw=90
                            elec.kw=kw
                            if(kw>5.5):i.type="S/D FEEDER"
                            else:i.type="DOL FEEDER"
                ddoc=self.mbr_cts_table
                if(self.mbr_cts_full_system):
                    ddoc=self.mbr_cts_full_system
                for mech in ddoc:
                    for elec in self.mbr_cts_electrical_items:
                        if(mech.item_description==elec.item_description):
                            if(mech.flow==None or mech.flow==""):
                                mech.flow=1
                            elif(mech.range==None or mech.range==""):
                                mech.range=1
                            if(elec.item_description in mbr_cts_ovivo_dos):
                                elec.kw=0.37
                                elec.type="DOL FEEDER"
                            else:
                                theoritical_power = (float(mech.flow)/3600)*(float(mech.range)*10*10*10*10*10)/1000
                                pump_shaft_power = (theoritical_power/70)*100
                                absorbed_motor_power = (pump_shaft_power/90)*100
                                kw=0
                                if(absorbed_motor_power<=0.045):kw=0.045
                                elif(absorbed_motor_power<=0.18):kw=0.18
                                elif(absorbed_motor_power<=0.37):kw=0.37
                                elif(absorbed_motor_power<=0.55):kw=0.55
                                elif(absorbed_motor_power<=0.75):kw=0.75
                                elif(absorbed_motor_power<=1.1):kw=1.1
                                elif(absorbed_motor_power<=1.5):kw=1.5
                                elif(absorbed_motor_power<=2.2):kw=2.2
                                elif(absorbed_motor_power<=3.7):kw=3.7
                                elif(absorbed_motor_power<=4):kw=4
                                elif(absorbed_motor_power<=5.5):kw=5.5
                                elif(absorbed_motor_power<=7.5):kw=7.5
                                elif(absorbed_motor_power<=11):kw=11
                                elif(absorbed_motor_power<=15):kw=15
                                elif(absorbed_motor_power<=18.5):kw=18.5
                                elif(absorbed_motor_power<=22):kw=22
                                elif(absorbed_motor_power<=30):kw=30
                                elif(absorbed_motor_power<=37):kw=37
                                elif(absorbed_motor_power<=45):kw=45
                                elif(absorbed_motor_power<=55):kw=55
                                elif(absorbed_motor_power<=75):kw=75
                                elif(absorbed_motor_power<=90):kw=90
                                elec.kw=kw
                                if(kw>5.5):i.type="S/D FEEDER"
                                else:i.type="DOL FEEDER"
                    
                ### Card Calculation
                #mf
                mf_non_vfd_tot = 0
                mf_vfd_tot = 0
                mf_wire2_tot = 0
                mf_wire4_tot = 0
                mf_level_float_tot = 0
                mf_non_vfd=["FEED PUMP", "BACKWASH PUMP", "CIP PUMP", "SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "SULPHUR BLACK DOSING PUMP"]
                mf_vfd=["BACKWASH PUMP"]
                mf_wire2=["LEVEL TRANSMITTER", "PRESSURE TRANSMITTER"]
                mf_wire4=["ELECTROMAGNETIC FLOWMETER", "PH SENSOR"]
                mf_level_float=["LEVEL FLOAT"]
                for i in self.mf_table:
                    if(i.sb_qty is None):
                        i.sb_qty = 0
                    if(i.w_qty is None):
                        i.w_qty = 0
                    if(i.ssb_qty is None):
                        i.ssb_qty = 0
                    if(i.item_description in mf_non_vfd):
                        if(i.item_description=="BACKWASH PUMP"):
                            mf_non_vfd_tot = mf_non_vfd_tot+i.sb_qty+i.ssb_qty    
                        else:
                            mf_non_vfd_tot = mf_non_vfd_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description in mf_vfd):
                        mf_vfd_tot = mf_vfd_tot+i.w_qty
                        
                    elif(i.item_description in mf_wire2):
                        mf_wire2_tot = mf_wire2_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description in mf_wire4):
                        mf_wire4_tot = mf_wire4_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description  in mf_level_float):
                        mf_level_float_tot = mf_level_float_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                self.mf_digital_input=(mf_non_vfd_tot+mf_vfd_tot)*3+mf_level_float_tot+40+10
                self.mf_digital_output=mf_non_vfd_tot+mf_vfd_tot+5+40
                self.mf_analog_input2=(mf_vfd_tot*2)+mf_wire2_tot
                self.mf_analog_input=mf_wire4_tot
                self.mf_analog_output=mf_vfd_tot
                #mbr_koch
                mbr_non_vfd_tot = 0
                mbr_vfd_tot = 0
                mbr_wire2_tot = 0
                mbr_wire4_tot = 0
                mbr_level_float_tot = 0
                mbr_non_vfd=["FEED PUMP", "PERMEATE/BACKWASH/CIP PUMP", "SLUDGE EXTRACT PUMP","SLUDGE RECIRCULATION PUMP","SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1","CIP DOSING PUMP-2","CIP DOSING PUMP-3"]
                mbr_vfd=["PERMEATE/BACKWASH/CIP PUMP"]
                mbr_wire2=["LEVEL TRANSMITTER", "PRESSURE TRANSMITTER"]
                mbr_wire4=["ELECTROMAGNETIC FLOWMETER"]
                mbr_level_float=["LEVEL FLOAT"]
                for i in self.mbr_koch_table:
                    if(i.sb_qty is None):
                        i.sb_qty = 0
                    if(i.w_qty is None):
                        i.w_qty = 0
                    if(i.ssb_qty is None):
                        i.ssb_qty = 0
                    if(i.item_description in mbr_non_vfd):
                        if(i.item_description=="PERMEATE/BACKWASH/CIP PUMP"):
                            mbr_non_vfd_tot = mbr_non_vfd_tot+i.sb_qty+i.ssb_qty    
                        else:
                            mbr_non_vfd_tot = mbr_non_vfd_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description in mbr_vfd):
                        mbr_vfd_tot = mbr_vfd_tot+i.w_qty
                        
                    elif(i.item_description in mbr_wire2):
                        mbr_wire2_tot = mbr_wire2_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description in mbr_wire4):
                        mbr_wire4_tot = mbr_wire4_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description  in mbr_level_float):
                        mbr_level_float_tot = mbr_level_float_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                self.mbr_digital_input=(mbr_non_vfd_tot+mbr_vfd_tot)*3+mbr_level_float_tot+40+10
                self.mbr_digital_output=mbr_non_vfd_tot+mbr_vfd_tot+5+40
                self.mbr_analog_input2=(mbr_vfd_tot*2)+mbr_wire2_tot
                self.mbr_analog_input=mbr_wire4_tot
                self.mbr_analog_output=mbr_vfd_tot
                #mbr_ovivo
                ovivo_non_vfd_tot = 0
                ovivo_vfd_tot = 0
                ovivo_wire2_tot = 0
                ovivo_wire4_tot = 0
                ovivo_level_float_tot = 0
                ovivo_non_vfd=["FEED PUMP","PERMEATE PUMP", "BACKWASH/CIP PUMP", "SLUDGE EXTRACT PUMP", "SLUDGE RECIRCULATION PUMP", "SPRINKLER PUMP", "SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1","CIP DOSING PUMP-2","CIP DOSING PUMP-3","SULPHUR BLACK DOSING PUMP"]
                ovivo_vfd=["BACKWASH/CIP PUMP","SPRINKLER PUMP"]
                ovivo_wire2=["LEVEL TRANSMITTER", "PRESSURE TRANSMITTER"]
                ovivo_wire4=["ELECTROMAGNETIC FLOWMETER", "TURBIDITY SENSOR"]
                ovivo_level_float=["LEVEL FLOAT"]
                for i in self.mbr_ovivo_table:
                    if(i.sb_qty is None):
                        i.sb_qty = 0
                    if(i.w_qty is None):
                        i.w_qty = 0
                    if(i.ssb_qty is None):
                        i.ssb_qty = 0
                    if(i.item_description in ovivo_non_vfd):
                        if(i.item_description in ovivo_vfd):
                            ovivo_non_vfd_tot = ovivo_non_vfd_tot+i.sb_qty+i.ssb_qty    
                        else:
                            ovivo_non_vfd_tot = ovivo_non_vfd_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description in ovivo_vfd):
                        ovivo_vfd_tot = ovivo_vfd_tot+i.w_qty
                        
                    elif(i.item_description in ovivo_wire2):
                        ovivo_wire2_tot = ovivo_wire2_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description in ovivo_wire4):
                        ovivo_wire4_tot = ovivo_wire4_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description  in ovivo_level_float):
                        ovivo_level_float_tot = ovivo_level_float_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                self.ovivo_digital_input=(ovivo_non_vfd_tot+ovivo_vfd_tot)*3+ovivo_level_float_tot+40+10
                self.ovivo_digital_output=ovivo_non_vfd_tot+ovivo_vfd_tot+5+40
                self.ovivo_analog_input2=(ovivo_vfd_tot*2)+ovivo_wire2_tot
                self.ovivo_analog_input=ovivo_wire4_tot
                self.ovivo_analog_output=ovivo_vfd_tot
                #mbr_cts
                mbr_cts_non_vfd_tot = 0
                mbr_cts_vfd_tot = 0
                mbr_cts_wire2_tot = 0
                mbr_cts_wire4_tot = 0
                mbr_cts_level_float_tot = 0
                mbr_cts_non_vfd=["FEED PUMP","PERMEATE PUMP", "BACKWASH/CIP PUMP", "SLUDGE EXTRACT PUMP", "SLUDGE RECIRCULATION PUMP", "SPRINKLER PUMP", "SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1","CIP DOSING PUMP-2","CIP DOSING PUMP-3","SULPHUR BLACK DOSING PUMP"]
                mbr_cts_vfd=["BACKWASH/CIP PUMP","SPRINKLER PUMP"]
                mbr_cts_wire2=["LEVEL TRANSMITTER", "PRESSURE TRANSMITTER"]
                mbr_cts_wire4=["ELECTROMAGNETIC FLOWMETER", "TURBIDITY SENSOR"]
                mbr_cts_level_float=["LEVEL FLOAT"]
                for i in self.mbr_cts_table:
                    if(i.sb_qty is None):
                        i.sb_qty = 0
                    if(i.w_qty is None):
                        i.w_qty = 0
                    if(i.ssb_qty is None):
                        i.ssb_qty = 0
                    if(i.item_description in mbr_cts_non_vfd):
                        if(i.item_description in mbr_cts_vfd):
                            mbr_cts_non_vfd_tot = mbr_cts_non_vfd_tot+i.sb_qty+i.ssb_qty    
                        else:
                            mbr_cts_non_vfd_tot = mbr_cts_non_vfd_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description in mbr_cts_vfd):
                        mbr_cts_vfd_tot = mbr_cts_vfd_tot+i.w_qty
                        
                    elif(i.item_description in mbr_cts_wire2):
                        mbr_cts_wire2_tot = mbr_cts_wire2_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description in mbr_cts_wire4):
                        mbr_cts_wire4_tot = mbr_cts_wire4_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description  in mbr_cts_level_float):
                        mbr_cts_level_float_tot = mbr_cts_level_float_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                self.mbr_cts_digital_input=(mbr_cts_non_vfd_tot+mbr_cts_vfd_tot)*3+mbr_cts_level_float_tot+40+10
                self.mbr_cts_digital_output=mbr_cts_non_vfd_tot+mbr_cts_vfd_tot+5+40
                self.mbr_cts_analog_input2=(mbr_cts_vfd_tot*2)+mbr_cts_wire2_tot
                self.mbr_cts_analog_input=mbr_cts_wire4_tot
                self.mbr_cts_analog_output=mbr_cts_vfd_tot
                ##pre treatment
                bio_non_vfd_tot = 0
                bio_vfd_tot = 0
                bio_wire2_tot = 0
                bio_wire4_tot = 0
                bio_level_float_tot = 0
                bio_non_vfd=["FEED PUMP", "PERMEATE/BACKWASH/CIP PUMP", "SLUDGE EXTRACT PUMP","SLUDGE RECIRCULATION PUMP","SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1","CIP DOSING PUMP-2","CIP DOSING PUMP-3"]
                bio_vfd=["PERMEATE/BACKWASH/CIP PUMP"]
                bio_wire2=["LEVEL TRANSMITTER", "PRESSURE TRANSMITTER"]
                bio_wire4=["ELECTROMAGNETIC FLOWMETER"]
                bio_level_float=["LEVEL FLOAT"]
                for i in self.pre_treatment_table:
                    if(i.sb_qty is None):
                        i.sb_qty = 0
                    if(i.w_qty is None):
                        i.w_qty = 0
                    if(i.ssb_qty is None):
                        i.ssb_qty = 0
                    if(i.item_description in bio_non_vfd):
                        if(i.item_description in bio_vfd):
                            bio_non_vfd_tot = bio_non_vfd_tot+i.sb_qty+i.ssb_qty    
                        else:
                            bio_non_vfd_tot = bio_non_vfd_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description in bio_vfd):
                        bio_vfd_tot = bio_vfd_tot+i.w_qty
                        
                    elif(i.item_description in bio_wire2):
                        bio_wire2_tot = bio_wire2_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description in bio_wire4):
                        bio_wire4_tot = bio_wire4_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description  in bio_level_float):
                        bio_level_float_tot = bio_level_float_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                self.bio_digital_input=(bio_non_vfd_tot+bio_vfd_tot)*3+bio_level_float_tot+40+10
                self.bio_digital_output=bio_non_vfd_tot+bio_vfd_tot+5+40
                self.bio_analog_input2=(bio_vfd_tot*2)+bio_wire2_tot
                self.bio_analog_input=bio_wire4_tot
                self.bio_analog_output=bio_vfd_tot
                #Chemical Treatment System
                cts_non_vfd_tot = 0
                cts_vfd_tot = 0
                cts_wire2_tot = 0
                cts_wire4_tot = 0
                cts_level_float_tot = 0
                cts_non_vfd=["FEED PUMP", "SLUDGE PUMP", "DOSING PUMP-1", "DOSING PUMP-2", "DOSING PUMP-3", "DOSING PUMP-4", "DOSING PUMP-5", "AGITATOR", "CIRCULAR CLARIFIER"]
                cts_vfd=[]
                cts_wire2=["LEVEL TRANSMITTER"]
                cts_wire4=[]
                cts_level_float=[]
                for i in self.cts_items:
                    if(i.sb_qty is None):
                        i.sb_qty = 0
                    if(i.w_qty is None):
                        i.w_qty = 0
                    if(i.ssb_qty is None):
                        i.ssb_qty = 0
                    if(i.item_description in cts_non_vfd):
                        if(i.item_description in cts_vfd):
                            cts_non_vfd_tot = cts_non_vfd_tot+i.sb_qty+i.ssb_qty    
                        else:
                            cts_non_vfd_tot = cts_non_vfd_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description in cts_vfd):
                        cts_vfd_tot = cts_vfd_tot+i.w_qty
                        
                    elif(i.item_description in cts_wire2):
                        cts_wire2_tot = cts_wire2_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description in cts_wire4):
                        cts_wire4_tot = cts_wire4_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                    elif(i.item_description  in cts_level_float):
                        cts_level_float_tot = cts_level_float_tot+i.w_qty+i.sb_qty+i.ssb_qty
                    
                self.cts_digital_input=(cts_non_vfd_tot+cts_vfd_tot)*3+cts_level_float_tot+40+10
                self.cts_digital_output=cts_non_vfd_tot+cts_vfd_tot+5+40
                self.cts_analog_input2=(cts_vfd_tot*2)+cts_wire2_tot
                self.cts_analog_input=cts_wire4_tot
                self.cts_analog_output=cts_vfd_tot
                
                # Electrical Cost
                # mf
                ddoc=self.mf_table
                if(self.mf_full_system):
                    ddoc=self.mf_full_system
                for i in ddoc:
                    for j in self.mf_electrical_items:
                        if(i.item_description==j.item_description):
                            if(j.item_description in item19):
                                j.kw=0.37
                                j.type="DOL FEEDER"
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                            else:
                                theoritical_power=float(i.flow)/3600*(float(i.range)*10*10*10*10*10)/1000
                                pump_shaft_power=(theoritical_power/70)*100
                                absorbed_motor_power=(pump_shaft_power/90)*100
                                if(absorbed_motor_power<=0.045):kw=0.045
                                elif(absorbed_motor_power<=0.18):kw=0.18
                                elif(absorbed_motor_power<=0.37):kw=0.37
                                elif(absorbed_motor_power<=0.55):kw=0.55
                                elif(absorbed_motor_power<=0.75):kw=0.75
                                elif(absorbed_motor_power<=1.1):kw=1.1
                                elif(absorbed_motor_power<=1.5):kw=1.5
                                elif(absorbed_motor_power<=2.2):kw=2.2
                                elif(absorbed_motor_power<=3.7):kw=3.7
                                elif(absorbed_motor_power<=4):kw=4
                                elif(absorbed_motor_power<=5.5):kw=5.5
                                elif(absorbed_motor_power<=7.5):kw=7.5
                                elif(absorbed_motor_power<=11):kw=11
                                elif(absorbed_motor_power<=15):kw=15
                                elif(absorbed_motor_power<=18.5):kw=18.5
                                elif(absorbed_motor_power<=22):kw=22
                                elif(absorbed_motor_power<=30):kw=30
                                elif(absorbed_motor_power<=37):kw=37
                                elif(absorbed_motor_power<=45):kw=45
                                elif(absorbed_motor_power<=55):kw=55
                                elif(absorbed_motor_power<=75):kw=75
                                elif(absorbed_motor_power<=90):kw=90
                                j.kw=kw if j.item_description!="PRE-FILTER" else j.kw
                                if(kw>5.5):j.type="S/D FEEDER"
                                else:j.type="DOL FEEDER"
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                        elif(j.item_description in ["PANEL","PLC"]):
                            j.w_qty=1
                for i in self.mf_electrical_items:
                    ic=i.item_description
                    kw=i.kw
                    tty=i.type
                    di=self.mf_digital_input
                    do=self.mf_digital_output
                    ai=self.mf_analog_input
                    ai2=self.mf_analog_input2
                    ao=self.mf_analog_output
                    ml_el=[]
                    vfd_up=[]
                    if(ic in ["PANEL","PLC"]):# condition to club the rate for electrical panel and plc items
                        panel_items=("PANEL ENCLOSURE","INCOMER MCCB","BUS BAR")
                        plc_items=("PLC CPU", "REMOTE CPU", "BUS END COVER", "POWER SUPPLY CARD", "16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)", "MONITOR", "MODEM", "ETHERNET SWITCH", "SMPS", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE")
                        if(ic=="PANEL"):
                            query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(panel_items)+" ",as_dict=1)
                            for k in query:
                                if(k.item_description=="BUS BAR"):
                                    k.qty = 3
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    ml_el.append(g.base_rate)
                        elif(ic=="PLC"):
                            ml_el=[50000]
                            cards = ["16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)"]
                            query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description as 'test' FROM `tabElectrical Child Items` WHERE item_description IN "+str(plc_items)+" ",as_dict=1)
                            for k in query:
                                if(k.test in cards):
                                    di_cal = float(di)/16
                                    do_cal = float(do)/16
                                    ai_cal = float(ai)/4
                                    ao_cal = float(ao)/8
                                    ai2_cal = float(ai2)/8
                                    # quantity calulation for cards based on input output calculatuion
                                    ar=[di_cal,do_cal,ai2_cal,ai_cal,ao_cal]
                                    for val in range(5):
                                        if(k.item_description==cards[val]):
                                            k.qty = round(ar[val])
                                            if(round(ar[val])<ar[val]):
                                                k.qty = round(ar[val])+1                        
                
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    ml_el.append(g.base_rate)
                    else:
                        query=frappe.db.sql("SELECT item_code,qty FROM `tabElectrical Child Items` WHERE kw='"+str(kw)+"' and type='"+str(tty)+"' GROUP BY item_code",as_dict=1)
                        for k in query:
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                ml_el.append(g.base_rate)
                        if(i.vfd_type=="VFD FEEDER"):
                            tty = i.vfd_type
                            query=frappe.db.sql("SELECT item_code,qty FROM `tabElectrical Child Items` WHERE kw='"+str(kw)+"' and type='"+str(tty)+"' GROUP BY item_code",as_dict=1)
                            for k in query:
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    vfd_up.append(g.base_rate)
                    if(i.w_qty is None):
                        i.w_qty=0
                    if(i.sb_qty is None):
                        i.sb_qty=0
                    if(i.ssb_qty is None):
                        i.ssb_qty=0
                    i.unit_price = sum(ml_el)
                    i.vfd_unit_price = sum(vfd_up)
                    if(i.vfd_type=="VFD FEEDER"):
                        w_qty=i.w_qty-1 if i.w_qty>0 else 0
                        i.total_price = (sum(ml_el)*(w_qty+i.sb_qty+i.ssb_qty))+sum(vfd_up)
                    else:
                        i.total_price = sum(ml_el)*(i.w_qty+i.sb_qty+i.ssb_qty)
                
                mf_pp=[]
                mf_pl=[]
                panel_items=("PANEL ENCLOSURE","INCOMER MCCB","BUS BAR")
                plc_items=("PLC CPU", "REMOTE CPU", "BUS END COVER", "POWER SUPPLY CARD", "16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)", "MONITOR", "MODEM", "ETHERNET SWITCH", "SMPS", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE")
                for i in self.mf_plc_items:
                    if(i.item_description=="PANEL"):
                        query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(panel_items)+" ",as_dict=1)
                        for k in query:
                            if(k.item_description=="BUS BAR"):
                                k.qty = 3
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                mf_pp.append(g.base_rate)
                        i.unit_price=sum(mf_pp)
                        i.total_price=i.unit_price * i.w_qty
                    
                    elif(i.item_description=="PLC"):
                        mf_pl=[50000]
                        cards = ["16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)"]
                        query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description as 'test' FROM `tabElectrical Child Items` WHERE item_description IN "+str(plc_items)+" ",as_dict=1)
                        for k in query:
                            if(k.test in cards):
                                di_cal = float(di)/16
                                do_cal = float(do)/16
                                ai_cal = float(ai)/4
                                ao_cal = float(ao)/8
                                ai2_cal = float(ai2)/8
                                ar=[di_cal,do_cal,ai2_cal,ai_cal,ao_cal]
                                for val in range(5):
                                    if(k.item_description==cards[val]):
                                        k.qty = round(ar[val])
                                        if(round(ar[val])<ar[val]):
                                            k.qty = round(ar[val])+1                        
            
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                mf_pl.append(g.base_rate)
                        i.unit_price=sum(mf_pl)
                        i.total_price=i.unit_price * i.w_qty
                    
                
                # mbr_koch
                ddoc=self.mbr_koch_table
                if(self.mbrk_full_system):
                    ddoc=self.mbrk_full_system
                for i in ddoc:
                    for j in self.mbr_electrical_items:
                        if(i.item_description==j.item_description):
                            if(j.item_description in items018):
                                j.kw=0.37
                                j.type="DOL FEEDER"
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                            else:
                                theoritical_power=float(i.flow)/3600*(float(i.range)*10*10*10*10*10)/1000
                                pump_shaft_power=(theoritical_power/70)*100
                                absorbed_motor_power=(pump_shaft_power/90)*100
                                if(absorbed_motor_power<=0.045):kw=0.045
                                elif(absorbed_motor_power<=0.18):kw=0.18
                                elif(absorbed_motor_power<=0.37):kw=0.37
                                elif(absorbed_motor_power<=0.55):kw=0.55
                                elif(absorbed_motor_power<=0.75):kw=0.75
                                elif(absorbed_motor_power<=1.1):kw=1.1
                                elif(absorbed_motor_power<=1.5):kw=1.5
                                elif(absorbed_motor_power<=2.2):kw=2.2
                                elif(absorbed_motor_power<=3.7):kw=3.7
                                elif(absorbed_motor_power<=4):kw=4
                                elif(absorbed_motor_power<=5.5):kw=5.5
                                elif(absorbed_motor_power<=7.5):kw=7.5
                                elif(absorbed_motor_power<=11):kw=11
                                elif(absorbed_motor_power<=15):kw=15
                                elif(absorbed_motor_power<=18.5):kw=18.5
                                elif(absorbed_motor_power<=22):kw=22
                                elif(absorbed_motor_power<=30):kw=30
                                elif(absorbed_motor_power<=37):kw=37
                                elif(absorbed_motor_power<=45):kw=45
                                elif(absorbed_motor_power<=55):kw=55
                                elif(absorbed_motor_power<=75):kw=75
                                elif(absorbed_motor_power<=90):kw=90
                                j.kw=kw
                                if(kw>5.5):j.type="S/D FEEDER"
                                else:j.type="DOL FEEDER"
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                        elif(j.item_description in ["PANEL","PLC"]):
                            j.w_qty=1
                for i in self.mbr_electrical_items:
                    ic=i.item_description
                    kw=i.kw
                    tty=i.type
                    di=self.mbr_digital_input
                    do=self.mbr_digital_output
                    ai=self.mbr_analog_input
                    ai2=self.mbr_analog_input2
                    ao=self.mbr_analog_output
                    ml_el=[]
                    vfd_up = []
                    if(ic in ["PANEL","PLC"]):# condition to club the rate for electrical panel and plc items
                        panel_items=("PANEL ENCLOSURE","INCOMER MCCB","BUS BAR")
                        plc_items=("PLC CPU", "REMOTE CPU", "BUS END COVER", "POWER SUPPLY CARD", "16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)", "MONITOR", "MODEM", "ETHERNET SWITCH", "SMPS", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE")
                        if(ic=="PANEL"):
                            query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(panel_items)+" ",as_dict=1)
                            for k in query:
                                if(k.item_description=="BUS BAR"):
                                    k.qty = 3
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    ml_el.append(g.base_rate)
                        elif(ic=="PLC"):
                            ml_el=[50000]
                            cards = ["16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)"]
                            query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(plc_items)+" ",as_dict=1)
                            for k in query:
                                if(k.item_description in cards):
                                    di_cal = float(di)/16
                                    do_cal = float(do)/16
                                    ai_cal = float(ai)/4
                                    ao_cal = float(ao)/8
                                    ai2_cal = float(ai2)/8
                                    # quantity calulation for cards based on input output calculatuion
                                    ar=[di_cal,do_cal,ai2_cal,ai_cal,ao_cal]
                                    for val in range(5):
                                        if(k.item_description==cards[val]):
                                            k.qty = round(ar[val])
                                            if(round(ar[val])<ar[val]):
                                                k.qty = round(ar[val])+1                        
                
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    ml_el.append(g.base_rate)
                    else:
                        query=frappe.db.sql("SELECT item_code,qty FROM `tabElectrical Child Items` WHERE kw='"+str(kw)+"' and type='"+str(tty)+"' GROUP BY item_code",as_dict=1)
                        for k in query:
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                ml_el.append(g.base_rate)
                        if(i.vfd_type=="VFD FEEDER"):
                            tty = i.vfd_type
                            query=frappe.db.sql("SELECT item_code,qty FROM `tabElectrical Child Items` WHERE kw='"+str(kw)+"' and type='"+str(tty)+"' GROUP BY item_code",as_dict=1)
                            for k in query:
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    vfd_up.append(g.base_rate)
                    if(i.w_qty is None):
                        i.w_qty=0
                    if(i.sb_qty is None):
                        i.sb_qty=0
                    if(i.ssb_qty is None):
                        i.ssb_qty=0
                    i.unit_price = sum(ml_el)
                    i.vfd_unit_price = sum(vfd_up)
                    if(i.vfd_type=="VFD FEEDER"):
                        w_qty=i.w_qty-1 if i.w_qty>0 else 0
                        i.total_price = (sum(ml_el)*(w_qty+i.sb_qty+i.ssb_qty))+sum(vfd_up)
                    else:
                        i.total_price = sum(ml_el)*(i.w_qty+i.sb_qty+i.ssb_qty)
                        
                
                mf_pp=[]
                mf_pl=[]
                panel_items=("PANEL ENCLOSURE","INCOMER MCCB","BUS BAR")
                plc_items=("PLC CPU", "REMOTE CPU", "BUS END COVER", "POWER SUPPLY CARD", "16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)", "MONITOR", "MODEM", "ETHERNET SWITCH", "SMPS", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE")
                for i in self.mbrk_plc_items:
                    if(i.item_description=="PANEL"):
                        query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(panel_items)+" ",as_dict=1)
                        for k in query:
                            if(k.item_description=="BUS BAR"):
                                k.qty = 3
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                mf_pp.append(g.base_rate)
                        i.unit_price=sum(mf_pp)
                        i.total_price=i.unit_price * i.w_qty
                    
                    elif(i.item_description=="PLC"):
                        mf_pl=[50000]
                        cards = ["16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)"]
                        query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description as 'test' FROM `tabElectrical Child Items` WHERE item_description IN "+str(plc_items)+" ",as_dict=1)
                        for k in query:
                            if(k.test in cards):
                                di_cal = float(di)/16
                                do_cal = float(do)/16
                                ai_cal = float(ai)/4
                                ao_cal = float(ao)/8
                                ai2_cal = float(ai2)/8
                                ar=[di_cal,do_cal,ai2_cal,ai_cal,ao_cal]
                                for val in range(5):
                                    if(k.item_description==cards[val]):
                                        k.qty = round(ar[val])
                                        if(round(ar[val])<ar[val]):
                                            k.qty = round(ar[val])+1                        
            
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                mf_pl.append(g.base_rate)
                        i.unit_price=sum(mf_pl)
                        i.total_price=i.unit_price * i.w_qty
                
                #mbr ovivo electrical items
                ddoc=self.mbr_ovivo_table
                if(self.mbro_full_system):
                    ddoc=self.mbro_full_system
                for i in ddoc:
                    for j in self.ovivo_electrical_items:
                        if(i.item_description==j.item_description):
                            if(j.item_description in mbr_ovivo_dos):
                                j.kw=0.37
                                j.type="DOL FEEDER"
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                            else:
                                theoritical_power=float(i.flow)/3600*(float(i.range)*10*10*10*10*10)/1000
                                pump_shaft_power=(theoritical_power/70)*100
                                absorbed_motor_power=(pump_shaft_power/90)*100
                                if(absorbed_motor_power<=0.045):kw=0.045
                                elif(absorbed_motor_power<=0.18):kw=0.18
                                elif(absorbed_motor_power<=0.37):kw=0.37
                                elif(absorbed_motor_power<=0.55):kw=0.55
                                elif(absorbed_motor_power<=0.75):kw=0.75
                                elif(absorbed_motor_power<=1.1):kw=1.1
                                elif(absorbed_motor_power<=1.5):kw=1.5
                                elif(absorbed_motor_power<=2.2):kw=2.2
                                elif(absorbed_motor_power<=3.7):kw=3.7
                                elif(absorbed_motor_power<=4):kw=4
                                elif(absorbed_motor_power<=5.5):kw=5.5
                                elif(absorbed_motor_power<=7.5):kw=7.5
                                elif(absorbed_motor_power<=11):kw=11
                                elif(absorbed_motor_power<=15):kw=15
                                elif(absorbed_motor_power<=18.5):kw=18.5
                                elif(absorbed_motor_power<=22):kw=22
                                elif(absorbed_motor_power<=30):kw=30
                                elif(absorbed_motor_power<=37):kw=37
                                elif(absorbed_motor_power<=45):kw=45
                                elif(absorbed_motor_power<=55):kw=55
                                elif(absorbed_motor_power<=75):kw=75
                                elif(absorbed_motor_power<=90):kw=90
                                j.kw=kw
                                if(kw>5.5):j.type="S/D FEEDER"
                                else:j.type="DOL FEEDER"
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                        elif(j.item_description in ["PANEL","PLC"]):
                            j.w_qty=1
                for i in self.ovivo_electrical_items:
                    ic=i.item_description
                    kw=i.kw
                    tty=i.type
                    di=self.ovivo_digital_input
                    do=self.ovivo_digital_output
                    ai=self.ovivo_analog_input
                    ai2=self.ovivo_analog_input2
                    ao=self.ovivo_analog_output
                    ml_el=[]
                    vfd_up=[]
                    if(ic in ["PANEL","PLC"]):# condition to club the rate for electrical panel and plc items
                        panel_items=("PANEL ENCLOSURE","INCOMER MCCB","BUS BAR")
                        plc_items=("PLC CPU", "REMOTE CPU", "BUS END COVER", "POWER SUPPLY CARD", "16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)", "MONITOR", "MODEM", "ETHERNET SWITCH", "SMPS", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE")
                        if(ic=="PANEL"):
                            query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(panel_items)+" ",as_dict=1)
                            for k in query:
                                if(k.item_description=="BUS BAR"):
                                    k.qty = 3
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    ml_el.append(g.base_rate)
                        elif(ic=="PLC"):
                            ml_el=[50000]
                            cards = ["16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)"]
                            query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(plc_items)+" ",as_dict=1)
                            for k in query:
                                if(k.item_description in cards):
                                    di_cal = float(di)/16
                                    do_cal = float(do)/16
                                    ai_cal = float(ai)/4
                                    ao_cal = float(ao)/8
                                    ai2_cal = float(ai2)/8
                                    # quantity calulation for cards based on input output calculatuion
                                    ar=[di_cal,do_cal,ai2_cal,ai_cal,ao_cal]
                                    for val in range(5):
                                        if(k.item_description==cards[val]):
                                            k.qty = round(ar[val])
                                            if(round(ar[val])<ar[val]):
                                                k.qty = round(ar[val])+1                        
                
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    ml_el.append(g.base_rate)
                    else:
                        query=frappe.db.sql("SELECT item_code,qty FROM `tabElectrical Child Items` WHERE kw='"+str(kw)+"' and type='"+str(tty)+"' GROUP BY item_code",as_dict=1)
                        for k in query:
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                ml_el.append(g.base_rate)
                        if(i.vfd_type=="VFD FEEDER"):
                            tty = i.vfd_type
                            query=frappe.db.sql("SELECT item_code,qty FROM `tabElectrical Child Items` WHERE kw='"+str(kw)+"' and type='"+str(tty)+"' GROUP BY item_code",as_dict=1)
                            for k in query:
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    vfd_up.append(g.base_rate)
                    if(i.w_qty is None):
                        i.w_qty=0
                    if(i.sb_qty is None):
                        i.sb_qty=0
                    if(i.ssb_qty is None):
                        i.ssb_qty=0
                    i.unit_price = sum(ml_el)
                    i.vfd_unit_price = sum(vfd_up)
                    if(i.vfd_type=="VFD FEEDER"):
                        w_qty=i.w_qty-1 if i.w_qty>0 else 0
                        i.total_price = (sum(ml_el)*(w_qty+i.sb_qty+i.ssb_qty))+sum(vfd_up)
                    else:
                        i.total_price = sum(ml_el)*(i.w_qty+i.sb_qty+i.ssb_qty)
                        
                mf_pp=[]
                mf_pl=[]
                panel_items=("PANEL ENCLOSURE","INCOMER MCCB","BUS BAR")
                plc_items=("PLC CPU", "REMOTE CPU", "BUS END COVER", "POWER SUPPLY CARD", "16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)", "MONITOR", "MODEM", "ETHERNET SWITCH", "SMPS", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE")
                for i in self.mbro_plc_items:
                    if(i.item_description=="PANEL"):
                        query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(panel_items)+" ",as_dict=1)
                        for k in query:
                            if(k.item_description=="BUS BAR"):
                                k.qty = 3
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                mf_pp.append(g.base_rate)
                        i.unit_price=sum(mf_pp)
                        i.total_price=i.unit_price * i.w_qty
                    
                    elif(i.item_description=="PLC"):
                        mf_pl=[50000]
                        cards = ["16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)"]
                        query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description as 'test' FROM `tabElectrical Child Items` WHERE item_description IN "+str(plc_items)+" ",as_dict=1)
                        for k in query:
                            if(k.test in cards):
                                di_cal = float(di)/16
                                do_cal = float(do)/16
                                ai_cal = float(ai)/4
                                ao_cal = float(ao)/8
                                ai2_cal = float(ai2)/8
                                ar=[di_cal,do_cal,ai2_cal,ai_cal,ao_cal]
                                for val in range(5):
                                    if(k.item_description==cards[val]):
                                        k.qty = round(ar[val])
                                        if(round(ar[val])<ar[val]):
                                            k.qty = round(ar[val])+1                        
            
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                mf_pl.append(g.base_rate)
                        i.unit_price=sum(mf_pl)
                        i.total_price=i.unit_price * i.w_qty
                
                #mbr cts electrical items
                ddoc=self.mbr_cts_table
                if(self.mbr_cts_full_system):
                    ddoc=self.mbr_cts_full_system
                for i in ddoc:
                    for j in self.mbr_cts_electrical_items:
                        if(i.item_description==j.item_description):
                            if(j.item_description in mbr_cts_ovivo_dos):
                                j.kw=0.37
                                j.type="DOL FEEDER"
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                            else:
                                theoritical_power=float(i.flow)/3600*(float(i.range)*10*10*10*10*10)/1000
                                pump_shaft_power=(theoritical_power/70)*100
                                absorbed_motor_power=(pump_shaft_power/90)*100
                                if(absorbed_motor_power<=0.045):kw=0.045
                                elif(absorbed_motor_power<=0.18):kw=0.18
                                elif(absorbed_motor_power<=0.37):kw=0.37
                                elif(absorbed_motor_power<=0.55):kw=0.55
                                elif(absorbed_motor_power<=0.75):kw=0.75
                                elif(absorbed_motor_power<=1.1):kw=1.1
                                elif(absorbed_motor_power<=1.5):kw=1.5
                                elif(absorbed_motor_power<=2.2):kw=2.2
                                elif(absorbed_motor_power<=3.7):kw=3.7
                                elif(absorbed_motor_power<=4):kw=4
                                elif(absorbed_motor_power<=5.5):kw=5.5
                                elif(absorbed_motor_power<=7.5):kw=7.5
                                elif(absorbed_motor_power<=11):kw=11
                                elif(absorbed_motor_power<=15):kw=15
                                elif(absorbed_motor_power<=18.5):kw=18.5
                                elif(absorbed_motor_power<=22):kw=22
                                elif(absorbed_motor_power<=30):kw=30
                                elif(absorbed_motor_power<=37):kw=37
                                elif(absorbed_motor_power<=45):kw=45
                                elif(absorbed_motor_power<=55):kw=55
                                elif(absorbed_motor_power<=75):kw=75
                                elif(absorbed_motor_power<=90):kw=90
                                j.kw=kw
                                if(kw>5.5):j.type="S/D FEEDER"
                                else:j.type="DOL FEEDER"
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                        elif(j.item_description in ["PANEL","PLC"]):
                            j.w_qty=1
                
                # for i in self.mbr_cts_table:
                #     for j in self.mbr_cts_electrical_items:
                #         if(i.item_description==j.item_description):
                #             theoritical_power=float(i.flow)/3600*(float(i.range)*10*10*10*10*10)/1000
                #             pump_shaft_power=(theoritical_power/70)*100
                #             absorbed_motor_power=(pump_shaft_power/90)*100
                #             if(absorbed_motor_power<=0.045):kw=0.045
                #             elif(absorbed_motor_power<=0.18):kw=0.18
                #             elif(absorbed_motor_power<=0.37):kw=0.37
                #             elif(absorbed_motor_power<=0.55):kw=0.55
                #             elif(absorbed_motor_power<=0.75):kw=0.75
                #             elif(absorbed_motor_power<=1.1):kw=1.1
                #             elif(absorbed_motor_power<=1.5):kw=1.5
                #             elif(absorbed_motor_power<=2.2):kw=2.2
                #             elif(absorbed_motor_power<=3.7):kw=3.7
                #             elif(absorbed_motor_power<=4):kw=4
                #             elif(absorbed_motor_power<=5.5):kw=5.5
                #             elif(absorbed_motor_power<=7.5):kw=7.5
                #             elif(absorbed_motor_power<=11):kw=11
                #             elif(absorbed_motor_power<=15):kw=15
                #             elif(absorbed_motor_power<=18.5):kw=18.5
                #             elif(absorbed_motor_power<=22):kw=22
                #             elif(absorbed_motor_power<=30):kw=30
                #             elif(absorbed_motor_power<=37):kw=37
                #             elif(absorbed_motor_power<=45):kw=45
                #             elif(absorbed_motor_power<=55):kw=55
                #             elif(absorbed_motor_power<=75):kw=75
                #             elif(absorbed_motor_power<=90):kw=90
                #             j.kw=kw
                #             if(kw>5.5):j.type="S/D FEEDER"
                #             else:j.type="DOL FEEDER"
                #             j.w_qty=i.w_qty
                #             j.sb_qty=i.sb_qty
                #             j.ssb_qty=i.ssb_qty
                #         elif(j.item_description in ["PANEL","PLC"]):
                #             j.w_qty=1
                for i in self.mbr_cts_electrical_items:
                    ic=i.item_description
                    kw=i.kw
                    tty=i.type
                    di=self.mbr_cts_digital_input
                    do=self.mbr_cts_digital_output
                    ai=self.mbr_cts_analog_input
                    ai2=self.mbr_cts_analog_input2
                    ao=self.mbr_cts_analog_output
                    ml_el=[]
                    vfd_up = []
                    if(ic in ["PANEL","PLC"]):# condition to club the rate for electrical panel and plc items
                        panel_items=("PANEL ENCLOSURE","INCOMER MCCB","BUS BAR")
                        plc_items=("PLC CPU", "REMOTE CPU", "BUS END COVER", "POWER SUPPLY CARD", "16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)", "MONITOR", "MODEM", "ETHERNET SWITCH", "SMPS", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE")
                        if(ic=="PANEL"):
                            query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(panel_items)+" ",as_dict=1)
                            for k in query:
                                if(k.item_description=="BUS BAR"):
                                    k.qty = 3
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    ml_el.append(g.base_rate)
                        elif(ic=="PLC"):
                            ml_el=[50000]
                            cards = ["16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)"]
                            query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(plc_items)+" ",as_dict=1)
                            for k in query:
                                if(k.item_description in cards):
                                    di_cal = float(di)/16
                                    do_cal = float(do)/16
                                    ai_cal = float(ai)/4
                                    ao_cal = float(ao)/8
                                    ai2_cal = float(ai2)/8
                                    # quantity calulation for cards based on input output calculatuion
                                    ar=[di_cal,do_cal,ai2_cal,ai_cal,ao_cal]
                                    for val in range(5):
                                        if(k.item_description==cards[val]):
                                            k.qty = round(ar[val])
                                            if(round(ar[val])<ar[val]):
                                                k.qty = round(ar[val])+1                        
                
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    ml_el.append(g.base_rate)
                    else:
                        query=frappe.db.sql("SELECT item_code,qty FROM `tabElectrical Child Items` WHERE kw='"+str(kw)+"' and type='"+str(tty)+"' GROUP BY item_code",as_dict=1)
                        for k in query:
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                ml_el.append(g.base_rate)
                        if(i.vfd_type=="VFD FEEDER"):
                            tty = i.vfd_type
                            query=frappe.db.sql("SELECT item_code,qty FROM `tabElectrical Child Items` WHERE kw='"+str(kw)+"' and type='"+str(tty)+"' GROUP BY item_code",as_dict=1)
                            for k in query:
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    vfd_up.append(g.base_rate)
                    if(i.w_qty is None):
                        i.w_qty=0
                    if(i.sb_qty is None):
                        i.sb_qty=0
                    if(i.ssb_qty is None):
                        i.ssb_qty=0
                    i.unit_price = sum(ml_el)
                    i.vfd_unit_price = sum(vfd_up)
                    if(i.vfd_type=="VFD FEEDER"):
                        w_qty=i.w_qty-1 if i.w_qty>0 else 0
                        i.total_price = (sum(ml_el)*(w_qty+i.sb_qty+i.ssb_qty))+sum(vfd_up)
                    else:
                        i.total_price = sum(ml_el)*(i.w_qty+i.sb_qty+i.ssb_qty)
                
                mf_pp=[]
                mf_pl=[]
                panel_items=("PANEL ENCLOSURE","INCOMER MCCB","BUS BAR")
                plc_items=("PLC CPU", "REMOTE CPU", "BUS END COVER", "POWER SUPPLY CARD", "16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)", "MONITOR", "MODEM", "ETHERNET SWITCH", "SMPS", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE")
                for i in self.mbr_cts_plc_items:
                    if(i.item_description=="PANEL"):
                        query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(panel_items)+" ",as_dict=1)
                        for k in query:
                            if(k.item_description=="BUS BAR"):
                                k.qty = 3
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                mf_pp.append(g.base_rate)
                        i.unit_price=sum(mf_pp)
                        i.total_price=i.unit_price * i.w_qty
                    
                    elif(i.item_description=="PLC"):
                        mf_pl=[50000]
                        cards = ["16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)"]
                        query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description as 'test' FROM `tabElectrical Child Items` WHERE item_description IN "+str(plc_items)+" ",as_dict=1)
                        for k in query:
                            if(k.test in cards):
                                di_cal = float(di)/16
                                do_cal = float(do)/16
                                ai_cal = float(ai)/4
                                ao_cal = float(ao)/8
                                ai2_cal = float(ai2)/8
                                ar=[di_cal,do_cal,ai2_cal,ai_cal,ao_cal]
                                for val in range(5):
                                    if(k.item_description==cards[val]):
                                        k.qty = round(ar[val])
                                        if(round(ar[val])<ar[val]):
                                            k.qty = round(ar[val])+1                        
            
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                mf_pl.append(g.base_rate)
                        i.unit_price=sum(mf_pl)
                        i.total_price=i.unit_price * i.w_qty
                
                
                
                ##CTS ELECTRICAL COST
                ddoc=self.cts_items
                if(self.cts_full_system):
                    ddoc=self.cts_full_system
                for i in ddoc:
                    for j in self.cts_electrical_items:
                        if(j.item_description in dos):
                            j.kw=0.37
                            if(kw>5.5):j.type="S/D FEEDER"
                            else:j.type="DOL FEEDER"
                            j.w_qty=i.w_qty
                            j.sb_qty=i.sb_qty
                            j.ssb_qty=i.ssb_qty
                        elif(j.item_description == "AGITATOR"):
                            j.kw=0.75
                            if(kw>5.5):j.type="S/D FEEDER"
                            else:j.type="DOL FEEDER"
                            j.w_qty=i.w_qty
                            j.sb_qty=i.sb_qty
                            j.ssb_qty=i.ssb_qty
                        elif(i.item_description==j.item_description):
                            theoritical_power=float(i.flow)/3600*(float(i.range)*10*10*10*10*10)/1000
                            pump_shaft_power=(theoritical_power/70)*100
                            absorbed_motor_power=(pump_shaft_power/90)*100
                            if(absorbed_motor_power<=0.045):kw=0.045
                            elif(absorbed_motor_power<=0.18):kw=0.18
                            elif(absorbed_motor_power<=0.37):kw=0.37
                            elif(absorbed_motor_power<=0.55):kw=0.55
                            elif(absorbed_motor_power<=0.75):kw=0.75
                            elif(absorbed_motor_power<=1.1):kw=1.1
                            elif(absorbed_motor_power<=1.5):kw=1.5
                            elif(absorbed_motor_power<=2.2):kw=2.2
                            elif(absorbed_motor_power<=3.7):kw=3.7
                            elif(absorbed_motor_power<=4):kw=4
                            elif(absorbed_motor_power<=5.5):kw=5.5
                            elif(absorbed_motor_power<=7.5):kw=7.5
                            elif(absorbed_motor_power<=11):kw=11
                            elif(absorbed_motor_power<=15):kw=15
                            elif(absorbed_motor_power<=18.5):kw=18.5
                            elif(absorbed_motor_power<=22):kw=22
                            elif(absorbed_motor_power<=30):kw=30
                            elif(absorbed_motor_power<=37):kw=37
                            elif(absorbed_motor_power<=45):kw=45
                            elif(absorbed_motor_power<=55):kw=55
                            elif(absorbed_motor_power<=75):kw=75
                            elif(absorbed_motor_power<=90):kw=90
                            j.kw=kw
                            if(kw>5.5):j.type="S/D FEEDER"
                            else:j.type="DOL FEEDER"
                            j.w_qty=i.w_qty
                            j.sb_qty=i.sb_qty
                            j.ssb_qty=i.ssb_qty
                        elif(j.item_description in ["PANEL","PLC"]):
                            j.w_qty=1
                for i in self.cts_electrical_items:
                    ic=i.item_description
                    kw=i.kw
                    tty=i.type
                    di=self.cts_digital_input
                    do=self.cts_digital_output
                    ai=self.cts_analog_input
                    ai2=self.cts_analog_input2
                    ao=self.cts_analog_output
                    ml_el=[]
                    vfd_up=[]
                    if(ic in ["PANEL","PLC"]):# condition to club the rate for electrical panel and plc items
                        panel_items=("PANEL ENCLOSURE","INCOMER MCCB","BUS BAR")
                        plc_items=("PLC CPU", "REMOTE CPU", "BUS END COVER", "POWER SUPPLY CARD", "16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)", "MONITOR", "MODEM", "ETHERNET SWITCH", "SMPS", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE")
                        if(ic=="PANEL"):
                            query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(panel_items)+" ",as_dict=1)
                            for k in query:
                                if(k.item_description=="BUS BAR"):
                                    k.qty = 3
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    ml_el.append(g.base_rate)
                        elif(ic=="PLC"):
                            ml_el=[50000]
                            cards = ["16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)"]
                            query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(plc_items)+" ",as_dict=1)
                            for k in query:
                                if(k.item_description in cards):
                                    di_cal = float(di)/16
                                    do_cal = float(do)/16
                                    ai_cal = float(ai)/4
                                    ao_cal = float(ao)/8
                                    ai2_cal = float(ai2)/8
                                    # quantity calulation for cards based on input output calculatuion
                                    ar=[di_cal,do_cal,ai2_cal,ai_cal,ao_cal]
                                    for val in range(5):
                                        if(k.item_description==cards[val]):
                                            k.qty = round(ar[val])
                                            if(round(ar[val])<ar[val]):
                                                k.qty = round(ar[val])+1                        
                
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    ml_el.append(g.base_rate)
                    else:
                        query=frappe.db.sql("SELECT item_code,qty FROM `tabElectrical Child Items` WHERE kw='"+str(kw)+"' and type='"+str(tty)+"' GROUP BY item_code",as_dict=1)
                        for k in query:
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                ml_el.append(g.base_rate)
                        if(i.vfd_type=="VFD FEEDER"):
                            tty = i.vfd_type
                            query=frappe.db.sql("SELECT item_code,qty FROM `tabElectrical Child Items` WHERE kw='"+str(kw)+"' and type='"+str(tty)+"' GROUP BY item_code",as_dict=1)
                            for k in query:
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    vfd_up.append(g.base_rate)
                    if(i.w_qty is None):
                        i.w_qty=0
                    if(i.sb_qty is None):
                        i.sb_qty=0
                    if(i.ssb_qty is None):
                        i.ssb_qty=0
                    i.unit_price = sum(ml_el)
                    i.vfd_unit_price = sum(vfd_up)
                    if(i.vfd_type=="VFD FEEDER"):
                        w_qty=i.w_qty-1 if i.w_qty>0 else 0
                        i.total_price = (sum(ml_el)*(w_qty+i.sb_qty+i.ssb_qty))+sum(vfd_up)
                    else:
                        i.total_price = sum(ml_el)*(i.w_qty+i.sb_qty+i.ssb_qty)
                
                
                mf_pp=[]
                mf_pl=[]
                panel_items=("PANEL ENCLOSURE","INCOMER MCCB","BUS BAR")
                plc_items=("PLC CPU", "REMOTE CPU", "BUS END COVER", "POWER SUPPLY CARD", "16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)", "MONITOR", "MODEM", "ETHERNET SWITCH", "SMPS", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE")
                for i in self.cts_plc_items:
                    if(i.item_description=="PANEL"):
                        query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(panel_items)+" ",as_dict=1)
                        for k in query:
                            if(k.item_description=="BUS BAR"):
                                k.qty = 3
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                mf_pp.append(g.base_rate)
                        i.unit_price=sum(mf_pp)
                        i.total_price=i.unit_price * i.w_qty
                    
                    elif(i.item_description=="PLC"):
                        mf_pl=[50000]
                        cards = ["16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)"]
                        query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description as 'test' FROM `tabElectrical Child Items` WHERE item_description IN "+str(plc_items)+" ",as_dict=1)
                        for k in query:
                            if(k.test in cards):
                                di_cal = float(di)/16
                                do_cal = float(do)/16
                                ai_cal = float(ai)/4
                                ao_cal = float(ao)/8
                                ai2_cal = float(ai2)/8
                                ar=[di_cal,do_cal,ai2_cal,ai_cal,ao_cal]
                                for val in range(5):
                                    if(k.item_description==cards[val]):
                                        k.qty = round(ar[val])
                                        if(round(ar[val])<ar[val]):
                                            k.qty = round(ar[val])+1                        
            
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                mf_pl.append(g.base_rate)
                        i.unit_price=sum(mf_pl)
                        i.total_price=i.unit_price * i.w_qty
                
                ##DEGASSER ELECTRICAL COST
                ddoc=self.dgt_items
                if(self.dgt_full_system):
                    ddoc=self.dgt_full_system
                for i in ddoc:
                    for j in self.dgt_electrical_items:
                        if(i.item_description==j.item_description):
                            if(j.item_description == "DOSING PUMP"):
                                kw=0.37
                                j.kw=kw
                                if(kw>5.5):j.type="S/D FEEDER"
                                else:j.type="DOL FEEDER"
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                        elif(j.item_description=="BLOWER" and i.item_description=="BLOWER FAN"):
                            j.w_qty=i.w_qty
                            j.sb_qty=i.sb_qty
                            j.ssb_qty=i.ssb_qty

                for j in self.dgt_electrical_items:
                    for i in ddoc:
                        if(j.item_description == "BLOWER"):
                            if(i.item_description == "BLOWER FAN"):
                                if(float(i.range) <=1000):
                                    kw=1.1
                                elif(float(i.range) <=1550):
                                    kw=2.2
                                elif(float(i.range) <=2800):
                                    kw=3.7
                                elif(float(i.range) <=4200):
                                    kw=5.5
                                elif(float(i.range)>4200):
                                    kw=5.5
                            j.kw=kw
                            if(kw>5.5):j.type="S/D FEEDER"
                            else:j.type="DOL FEEDER"
                            if(i.item_description == "DEGASSER TOWER"):
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                for i in self.dgt_electrical_items:
                    ic=i.item_description
                    kw=i.kw
                    tty=i.type
                    di=self.dgt_digital_input
                    do=self.dgt_digital_output
                    ai=self.dgt_analog_input
                    ai2=self.dgt_analog_input2
                    ao=self.dgt_analog_output
                    ml_el=[]
                    vfd_up=[]
                    if(ic in ["PANEL","PLC"]):# condition to club the rate for electrical panel and plc items
                        panel_items=("PANEL ENCLOSURE","INCOMER MCCB","BUS BAR")
                        plc_items=("PLC CPU", "REMOTE CPU", "BUS END COVER", "POWER SUPPLY CARD", "16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)", "MONITOR", "MODEM", "ETHERNET SWITCH", "SMPS", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE")
                        if(ic=="PANEL"):
                            query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(panel_items)+" ",as_dict=1)
                            for k in query:
                                if(k.item_description=="BUS BAR"):
                                    k.qty = 3
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    ml_el.append(g.base_rate)
                        elif(ic=="PLC"):
                            ml_el=[50000]
                            cards = ["16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)"]
                            query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(plc_items)+" ",as_dict=1)
                            for k in query:
                                if(k.item_description in cards):
                                    di_cal = float(di)/16
                                    do_cal = float(do)/16
                                    ai_cal = float(ai)/4
                                    ao_cal = float(ao)/8
                                    ai2_cal = float(ai2)/8
                                    # quantity calulation for cards based on input output calculatuion
                                    ar=[di_cal,do_cal,ai2_cal,ai_cal,ao_cal]
                                    for val in range(5):
                                        if(k.item_description==cards[val]):
                                            k.qty = round(ar[val])
                                            if(round(ar[val])<ar[val]):
                                                k.qty = round(ar[val])+1                        
                
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    ml_el.append(g.base_rate)
                    else:
                        query=frappe.db.sql("SELECT item_code,qty FROM `tabElectrical Child Items` WHERE kw='"+str(kw)+"' and type='"+str(tty)+"' GROUP BY item_code",as_dict=1)
                        for k in query:
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                ml_el.append(g.base_rate)
                        if(i.vfd_type=="VFD FEEDER"):
                            tty = i.vfd_type
                            query=frappe.db.sql("SELECT item_code,qty FROM `tabElectrical Child Items` WHERE kw='"+str(kw)+"' and type='"+str(tty)+"' GROUP BY item_code",as_dict=1)
                            for k in query:
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    vfd_up.append(g.base_rate)
                    if(i.w_qty is None):
                        i.w_qty=0
                    if(i.sb_qty is None):
                        i.sb_qty=0
                    if(i.ssb_qty is None):
                        i.ssb_qty=0
                    i.unit_price = sum(ml_el)
                    i.vfd_unit_price = sum(vfd_up)
                    if(i.vfd_type=="VFD FEEDER"):
                        w_qty=i.w_qty-1 if i.w_qty>0 else 0
                        i.total_price = (sum(ml_el)*(w_qty+i.sb_qty+i.ssb_qty))+sum(vfd_up)
                    else:
                        i.total_price = sum(ml_el)*(i.w_qty+i.sb_qty+i.ssb_qty)
                        
                mf_pp=[]
                mf_pl=[]
                panel_items=("PANEL ENCLOSURE","INCOMER MCCB","BUS BAR")
                plc_items=("PLC CPU", "REMOTE CPU", "BUS END COVER", "POWER SUPPLY CARD", "16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)", "MONITOR", "MODEM", "ETHERNET SWITCH", "SMPS", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE")
                for i in self.dgt_plc_items:
                    if(i.item_description=="PANEL"):
                        query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(panel_items)+" ",as_dict=1)
                        for k in query:
                            if(k.item_description=="BUS BAR"):
                                k.qty = 3
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                mf_pp.append(g.base_rate)
                        i.unit_price=sum(mf_pp)
                        i.total_price=i.unit_price * i.w_qty
                    
                    elif(i.item_description=="PLC"):
                        mf_pl=[50000]
                        cards = ["16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)"]
                        query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description as 'test' FROM `tabElectrical Child Items` WHERE item_description IN "+str(plc_items)+" ",as_dict=1)
                        for k in query:
                            if(k.test in cards):
                                di_cal = float(di)/16
                                do_cal = float(do)/16
                                ai_cal = float(ai)/4
                                ao_cal = float(ao)/8
                                ai2_cal = float(ai2)/8
                                ar=[di_cal,do_cal,ai2_cal,ai_cal,ao_cal]
                                for val in range(5):
                                    if(k.item_description==cards[val]):
                                        k.qty = round(ar[val])
                                        if(round(ar[val])<ar[val]):
                                            k.qty = round(ar[val])+1                        
            
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                mf_pl.append(g.base_rate)
                        i.unit_price=sum(mf_pl)
                        i.total_price=i.unit_price * i.w_qty
                
                
                ##bio electrical items
                ddoc=self.pre_treatment_table
                if self.bio_all_items:
                    ddoc=self.bio_all_items
                for i in ddoc:
                    for j in self.bio_electrical_items:
                        if(j.item_description == "BLOWER"):
                            if(i.item_description == "BLOWER FAN"):
                                if(float(i.range) <=1000):
                                    kw=1.1
                                elif(float(i.range) <=1550):
                                    kw=2.2
                                elif(float(i.range) <=2800):
                                    kw=3.7
                                elif(float(i.range) <=4200):
                                    kw=5.5
                                elif(float(i.range)>4200):
                                    kw=5.5
                            j.kw=kw
                            if(kw>5.5):j.type="S/D FEEDER"
                            else:j.type="DOL FEEDER"
                            if(i.item_description == "AMMONIA TOWER"):
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                for i in ddoc:
                    for j in self.bio_electrical_items:
                        if(j.item_description in ["ROTARY BRUSH SCREENER", "DRUM SCREENER", "DAF SCRAPPER", "DAF DOSING PUMP-1", "DAF DOSING PUMP-2", "EQT FLOW MAKER", "NT DOSING PUMP", "COOLING TOWER", "DNT FLOW MIXER", "BIO FLOW MAKER", "CIRCULAR CLARIFIER SYSTEM", "SLUDGE THICKENER WITH MECH", "BELT PRESS", "BELT POLY UNIT MODEL", "BELT PRESS DOSING PUMP", "BELT PRESS AGITATOR", "SCREW PRESS", "SCREW POLY UNIT MODEL", "SCREW PRESS DOSING PUMP", "SCREW PRESS AGITATOR","BIO BLOWER","EQT BLOWER"]):
                            kw=j.kw
                            if(j.item_description in ["DAF DOSING PUMP-1","DAF DOSING PUMP-2","NT DOSING PUMP","BELT DOSING PUMP","SCREW DOSING PUMP"]):
                                kw=0.37
                            elif(j.item_description in ["ROTARY BRUSH SCREENER", "DAF SCRAPPER", "CIRCULAR CLARIFIER SYSTEM", "SLUDGE THICKENER WITH MECH", "BELT PRESS", "BELT POLY UNIT MODEL", "SCREW PRESS", "SCREW POLY UNIT MODEL", "SCREW PRESS DOSING PUMP"]):
                                kw=0.37
                            elif(j.item_description in ["DRUM SCREENER","BELT PRESS AGITATOR","SCREW PRESS AGITATOR"]):
                                kw=0.75
                            elif(j.item_description in ["EQT FLOW MAKER","BIO FLOW MAKER","COOLING TOWER"]):
                                kw=5.5
                            elif(j.item_description=="DNT FLOW MIXER"):
                                kw=11
                            elif(j.item_description == "DAF BUBBLE GENERATION PUMP"):
                                if(i.item_description == "DAF BUBBLE GENERATION PUMP"):
                                    if(i.flow<=1):
                                        kw=0.75
                                    elif(i.flow<=1.5):
                                        kw=1.5
                                    elif(i.flow<=3.0):
                                        kw=2.2
                                    elif(i.flow<=4.8):
                                        kw=3.7
                                    elif(i.flow<=8.0):
                                        kw=5.5
                                    elif(i.flow<=12.0):
                                        kw=7.5
                                    elif(i.flow<=15.0):
                                        kw=11
                                    elif(i.flow<=20.0):
                                        kw=15
                                    elif(i.flow<=42.0):
                                        kw=22
                            elif(j.item_description in ["BIO BLOWER","EQT BLOWER"]):
                                if(m.seperate_blower_for_equalization_tank == 1):
                                    if(j.item_description=="BIO BLOWER"):
                                        bio_flow=m.bio_blower
                                        flow3min = bio_flow * 0.588578
                                        bio_range = (m.tank_height + 0.5)/10
                                        inchh2 = bio_range * 401.865
                                        power = ((flow3min * inchh2)/(6356 * 0.67))/1.34
                                        if(power<=0.045):kw=0.045
                                        elif(power<=0.18):kw=0.18
                                        elif(power<=0.37):kw=0.37
                                        elif(power<=0.55):kw=0.55
                                        elif(power<=0.75):kw=0.75
                                        elif(power<=1.1):kw=1.1
                                        elif(power<=1.5):kw=1.5
                                        elif(power<=2.2):kw=2.2
                                        elif(power<=3.7):kw=3.7
                                        elif(power<=4):kw=4
                                        elif(power<=5.5):kw=5.5
                                        elif(power<=7.5):kw=7.5
                                        elif(power<=11):kw=11
                                        elif(power<=15):kw=15
                                        elif(power<=18.5):kw=18.5
                                        elif(power<=22):kw=22
                                        elif(power<=30):kw=30
                                        elif(power<=37):kw=37
                                        elif(power<=45):kw=45
                                        elif(power<=55):kw=55
                                        elif(power<=75):kw=75
                                        elif(power<=90):kw=90
                                        elif(power<=110):kw=110
                                        elif(power<=160):kw=160
                                        elif(power>160):kw=0
                                    elif(j.item_description=="EQT BLOWER"):
                                        eqt_flow=m.eq_blower
                                        flow3min = eqt_flow * 0.588578
                                        eqt_range = (m.tank_height + 0.5)/10
                                        inchh2 = eqt_range * 401.865
                                        power = ((flow3min * inchh2)/(6356 * 0.67))/1.34
                                        if(power<=0.045):kw=0.045
                                        elif(power<=0.18):kw=0.18
                                        elif(power<=0.37):kw=0.37
                                        elif(power<=0.55):kw=0.55
                                        elif(power<=0.75):kw=0.75
                                        elif(power<=1.1):kw=1.1
                                        elif(power<=1.5):kw=1.5
                                        elif(power<=2.2):kw=2.2
                                        elif(power<=3.7):kw=3.7
                                        elif(power<=4):kw=4
                                        elif(power<=5.5):kw=5.5
                                        elif(power<=7.5):kw=7.5
                                        elif(power<=11):kw=11
                                        elif(power<=15):kw=15
                                        elif(power<=18.5):kw=18.5
                                        elif(power<=22):kw=22
                                        elif(power<=30):kw=30
                                        elif(power<=37):kw=37
                                        elif(power<=45):kw=45
                                        elif(power<=55):kw=55
                                        elif(power<=75):kw=75
                                        elif(power<=90):kw=90
                                        elif(power<=110):kw=110
                                        elif(power<=160):kw=160
                                        elif(power>160):kw=0
                                else:
                                    if(j.item_description=="BIO BLOWER"):
                                        bio_flow=m.each_blower
                                        flow3min = bio_flow * 0.588578
                                        bio_range = (m.tank_height + 0.5)/10
                                        inchh2 = bio_range * 401.865
                                        power = ((flow3min * inchh2)/(6356 * 0.67))/1.34
                                        if(power<=0.045):kw=0.045
                                        elif(power<=0.18):kw=0.18
                                        elif(power<=0.37):kw=0.37
                                        elif(power<=0.55):kw=0.55
                                        elif(power<=0.75):kw=0.75
                                        elif(power<=1.1):kw=1.1
                                        elif(power<=1.5):kw=1.5
                                        elif(power<=2.2):kw=2.2
                                        elif(power<=3.7):kw=3.7
                                        elif(power<=4):kw=4
                                        elif(power<=5.5):kw=5.5
                                        elif(power<=7.5):kw=7.5
                                        elif(power<=11):kw=11
                                        elif(power<=15):kw=15
                                        elif(power<=18.5):kw=18.5
                                        elif(power<=22):kw=22
                                        elif(power<=30):kw=30
                                        elif(power<=37):kw=37
                                        elif(power<=45):kw=45
                                        elif(power<=55):kw=55
                                        elif(power<=75):kw=75
                                        elif(power<=90):kw=90
                                        elif(power<=110):kw=110
                                        elif(power<=160):kw=160
                                        elif(power>160):kw=0
                                    elif(j.item_description=="EQT BLOWER"):
                                        kw=0
                            j.kw=kw
                            if(kw>5.5):j.type="S/D FEEDER"
                            else:j.type="DOL FEEDER"
                            if(i.item_description==j.item_description):
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                            
                        elif(i.item_description==j.item_description):
                            if(j.item_description in ["BELT DOSING PUMP","SCREW DOSING PUMP"]):
                                j.kw=0.37
                                j.type="DOL FEEDER"
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                            elif(j.item_description == "DAF BUBBLE GENERATION PUMP"):
                                if(i.item_description == "DAF BUBBLE GENERATION PUMP"):
                                    if(float(i.flow)<=1):
                                        kw=0.75
                                    elif(float(i.flow)<=1.5):
                                        kw=1.5
                                    elif(float(i.flow)<=3.0):
                                        kw=2.2
                                    elif(float(i.flow)<=4.8):
                                        kw=3.7
                                    elif(float(i.flow)<=8.0):
                                        kw=5.5
                                    elif(float(i.flow)<=12.0):
                                        kw=7.5
                                    elif(float(i.flow)<=15.0):
                                        kw=11
                                    elif(float(i.flow)<=20.0):
                                        kw=15
                                    elif(float(i.flow)<=42.0):
                                        kw=22
                                j.kw=kw
                                if(kw>5.5):j.type="S/D FEEDER"
                                else:j.type="DOL FEEDER"
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                            else:
                                try:
                                    cal=float(i.flow)/3600*(float(i.range)*10*10*10*10*10)/1000
                                except:
                                    cal=0
                                theoritical_power=cal
                                pump_shaft_power=(theoritical_power/70)*100
                                absorbed_motor_power=(pump_shaft_power/90)*100
                                if(absorbed_motor_power<=0.045):kw=0.045
                                elif(absorbed_motor_power<=0.18):kw=0.18
                                elif(absorbed_motor_power<=0.37):kw=0.37
                                elif(absorbed_motor_power<=0.55):kw=0.55
                                elif(absorbed_motor_power<=0.75):kw=0.75
                                elif(absorbed_motor_power<=1.1):kw=1.1
                                elif(absorbed_motor_power<=1.5):kw=1.5
                                elif(absorbed_motor_power<=2.2):kw=2.2
                                elif(absorbed_motor_power<=3.7):kw=3.7
                                elif(absorbed_motor_power<=4):kw=4
                                elif(absorbed_motor_power<=5.5):kw=5.5
                                elif(absorbed_motor_power<=7.5):kw=7.5
                                elif(absorbed_motor_power<=11):kw=11
                                elif(absorbed_motor_power<=15):kw=15
                                elif(absorbed_motor_power<=18.5):kw=18.5
                                elif(absorbed_motor_power<=22):kw=22
                                elif(absorbed_motor_power<=30):kw=30
                                elif(absorbed_motor_power<=37):kw=37
                                elif(absorbed_motor_power<=45):kw=45
                                elif(absorbed_motor_power<=55):kw=55
                                elif(absorbed_motor_power<=75):kw=75
                                elif(absorbed_motor_power<=90):kw=90
                                j.kw=kw
                                if(kw>5.5):j.type="S/D FEEDER"
                                else:j.type="DOL FEEDER"
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                            if(j.item_description == "DOSING PUMP"):
                                kw=0.37
                                j.kw=kw
                                if(kw>5.5):j.type="S/D FEEDER"
                                else:j.type="DOL FEEDER"
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                        elif(j.item_description=="BLOWER" and i.item_description=="BLOWER FAN"):
                            j.w_qty=i.w_qty
                            j.sb_qty=i.sb_qty
                            j.ssb_qty=i.ssb_qty

                for j in self.dgt_electrical_items:
                    for i in ddoc:
                        if(j.item_description == "BLOWER"):
                            if(i.item_description == "BLOWER FAN"):
                                if(float(i.range) <=1000):
                                    kw=1.1
                                elif(float(i.range) <=1550):
                                    kw=2.2
                                elif(float(i.range) <=2800):
                                    kw=3.7
                                elif(float(i.range) <=4200):
                                    kw=5.5
                                elif(float(i.range)>4200):
                                    kw=5.5
                            j.kw=kw
                            if(kw>5.5):j.type="S/D FEEDER"
                            else:j.type="DOL FEEDER"
                            if(i.item_description == "DEGASSER TOWER"):
                                j.w_qty=i.w_qty
                                j.sb_qty=i.sb_qty
                                j.ssb_qty=i.ssb_qty
                        elif(j.item_description in ["PANEL","PLC"]):
                            j.w_qty=1
                
                
                for i in self.bio_full_system:
                    for j in self.bio_electrical_items:
                        if(i.item_description == "Belt Press"):
                            if(j.item_description == "BELT PRESS" or j.item_description == "BELT PRESS AGITATOR"):
                                j.w_qty=i.w_qty
                                # j.sb_qty=i.sb_qty
                                # j.ssb_qty=i.ssb_qty
                        elif(i.item_description == "Screw Press"):
                            if(j.item_description == "SCREW PRESS" or j.item_description == "SCREW PRESS AGITATOR"):
                                j.w_qty=i.w_qty
                                # j.sb_qty=i.sb_qty
                                # j.ssb_qty=i.ssb_qty
                        elif(i.item_description == "Circular Clarifier System"):
                            if(j.item_description == "CIRCULAR CLARIFIER SYSTEM"):
                                j.w_qty=i.w_qty
                                # j.sb_qty=i.sb_qty
                                # j.ssb_qty=i.ssb_qty
                        elif(i.item_description == "Rotary Brush Screener"):
                            if(j.item_description == "ROTARY BRUSH SCREENER"):
                                j.w_qty=i.w_qty
                                # j.sb_qty=i.sb_qty
                                # j.ssb_qty=i.ssb_qty
                        elif(i.item_description == "Drum Screener"):
                            if(j.item_description == "DRUM SCREENER"):
                                j.w_qty=i.w_qty
                                # j.sb_qty=i.sb_qty
                                # j.ssb_qty=i.ssb_qty
                        elif(i.item_description == "Cooling Tower"):
                            if(j.item_description == "COOLING TOWER"):
                                j.w_qty=i.w_qty
                                # j.sb_qty=i.sb_qty
                                # j.ssb_qty=i.ssb_qty
                        elif(i.item_description == "Sludge Thickener with mech"):
                            if(j.item_description == "SLUDGE THICKENER WITH MECH"):
                                j.w_qty=i.w_qty
                                # j.sb_qty=i.sb_qty
                                # j.ssb_qty=i.ssb_qty
                        elif(i.item_description == "DAF (Dissolved Air Flotation)"):
                            if(j.item_description == "DAF SCRAPPER"):
                                j.w_qty=i.w_qty
                                # j.sb_qty=i.sb_qty
                                # j.ssb_qty=i.ssb_qty
                            elif(j.item_description == "DAF FEED PUMP"):
                                j.w_qty=i.w_qty
                                # j.sb_qty=i.sb_qty
                                # j.ssb_qty=i.ssb_qty
                            
                for i in self.bio_electrical_items:
                    ic=i.item_description
                    kw=i.kw
                    tty=i.type
                    # if(i.vfd_type=="VFD FEEDER"):
                    #     tty = i.vfd_type
                    di=self.bio_digital_input
                    do=self.bio_digital_output
                    ai=self.bio_analog_input
                    ai2=self.bio_analog_input2
                    ao=self.bio_analog_output
                    ml_el=[]
                    vfd_up=[]
                    if(ic in ["PANEL","PLC"]):# condition to club the rate for electrical panel and plc items
                        panel_items=("PANEL ENCLOSURE","INCOMER MCCB","BUS BAR")
                        plc_items=("PLC CPU", "REMOTE CPU", "BUS END COVER", "POWER SUPPLY CARD", "16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)", "MONITOR", "MODEM", "ETHERNET SWITCH", "SMPS", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE")
                        if(ic=="PANEL"):
                            query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(panel_items)+" ",as_dict=1)
                            for k in query:
                                if(k.item_description=="BUS BAR"):
                                    k.qty = 3
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    ml_el.append(g.base_rate)
                        elif(ic=="PLC"):
                            ml_el=[50000]
                            cards = ["16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)"]
                            query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(plc_items)+" ",as_dict=1)
                            for k in query:
                                if(k.item_description in cards):
                                    di_cal = float(di)/16
                                    do_cal = float(do)/16
                                    ai_cal = float(ai)/4
                                    ao_cal = float(ao)/8
                                    ai2_cal = float(ai2)/8
                                    # quantity calulation for cards based on input output calculatuion
                                    ar=[di_cal,do_cal,ai2_cal,ai_cal,ao_cal]
                                    for val in range(5):
                                        if(k.item_description==cards[val]):
                                            k.qty = round(ar[val])
                                            if(round(ar[val])<ar[val]):
                                                k.qty = round(ar[val])+1                        
                
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    ml_el.append(g.base_rate)
                    else:
                        query=frappe.db.sql("SELECT item_code,qty FROM `tabElectrical Child Items` WHERE kw='"+str(kw)+"' and type='"+str(tty)+"' GROUP BY item_code",as_dict=1)
                        for k in query:
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                ml_el.append(g.base_rate)
                        if(i.vfd_type=="VFD FEEDER"):
                            tty = i.vfd_type
                            query=frappe.db.sql("SELECT item_code,qty FROM `tabElectrical Child Items` WHERE kw='"+str(kw)+"' and type='"+str(tty)+"' GROUP BY item_code",as_dict=1)
                            for k in query:
                                query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                                for g in query2:
                                    vfd_up.append(g.base_rate)
                    if(i.w_qty is None):
                        i.w_qty=0
                    if(i.sb_qty is None):
                        i.sb_qty=0
                    if(i.ssb_qty is None):
                        i.ssb_qty=0
                    i.unit_price = sum(ml_el)
                    i.vfd_unit_price = sum(vfd_up)
                    if(i.vfd_type=="VFD FEEDER"):
                        w_qty=i.w_qty-1 if i.w_qty>0 else 0
                        i.total_price = ((sum(ml_el))*(w_qty+i.sb_qty+i.ssb_qty))+sum(vfd_up)
                    else:
                        i.total_price = (sum(ml_el))*(i.w_qty+i.sb_qty+i.ssb_qty)
                
                #bio_plc_items
                mf_pp=[]
                mf_pl=[]
                panel_items=("PANEL ENCLOSURE","INCOMER MCCB","BUS BAR")
                plc_items=("PLC CPU", "REMOTE CPU", "BUS END COVER", "POWER SUPPLY CARD", "16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)", "MONITOR", "MODEM", "ETHERNET SWITCH", "SMPS", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE")
                for i in self.bio_plc_items:
                    if(i.item_description=="PANEL"):
                        query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(panel_items)+" ",as_dict=1)
                        for k in query:
                            if(k.item_description=="BUS BAR"):
                                k.qty = 3
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                mf_pp.append(g.base_rate)
                        i.unit_price=sum(mf_pp)
                        i.total_price=i.unit_price * i.w_qty
                    
                    elif(i.item_description=="PLC"):
                        mf_pl=[50000]
                        cards = ["16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)"]
                        query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description as 'test' FROM `tabElectrical Child Items` WHERE item_description IN "+str(plc_items)+" ",as_dict=1)
                        for k in query:
                            if(k.test in cards):
                                di_cal = float(di)/16
                                do_cal = float(do)/16
                                ai_cal = float(ai)/4
                                ao_cal = float(ao)/8
                                ai2_cal = float(ai2)/8
                                ar=[di_cal,do_cal,ai2_cal,ai_cal,ao_cal]
                                for val in range(5):
                                    if(k.item_description==cards[val]):
                                        k.qty = round(ar[val])
                                        if(round(ar[val])<ar[val]):
                                            k.qty = round(ar[val])+1                        
            
                            query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
                            for g in query2:
                                mf_pl.append(g.base_rate)
                        i.unit_price=sum(mf_pl)
                        i.total_price=i.unit_price * i.w_qty
                
                sel_system=[]
                for v in frappe.db.sql("SELECT selected_system_name FROM `tabSelected Process System` where parent='"+str(self.project_startup_sheet)+"'",as_dict=1):
                    sel_system.append(v.selected_system_name)
                
                panelcount=0
                if "Biological Oxidation System" in sel_system:
                    panelcount=panelcount+1
                if "Micro Filtration - ASAHI" in sel_system:
                    panelcount=panelcount+1
                # if self.additional_mf:
                if "Submerged MBR system - KOCH" in sel_system:
                    panelcount=panelcount+1
                if "Submerged MBR system - OVIVO" in sel_system:
                    panelcount=panelcount+1
                if "Bar Screener" in sel_system:
                    for i in self.bio_full_system:
                        if(i.item_description == "Bar Screener"):
                            for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='PSISOSS3161590MM796MM2MM' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                i.unit_price = g.base_rate
                bb_cost=[]
                if(self.system_list!=None):
                    for jj in array:
                        if(jj["system"]==self.system_list):
                            bb_cost.append(float(jj["amount"]))
                            if(float(jj["amount"])>0):self.remarks="Cost added from Pre Treatment Table "+str(jj["amount"])
                            else:self.remarks=''
                for i in self.bom_item_rate:
                    array=[]
                    for j in self.pre_treatment_table:
                        if(i.item_description==j.system):
                            if(j.total_price!=None):
                                arr.append(j.total_price)
                    array.append({"system":str(i.item_description),"amount":str(round(sum(arr)))})
                    if(i.total_price is not None):
                        bb_cost.append(i.total_price)
                self.total_bom_cost = sum(bb_cost)
                #erection and commision
                cost=[]
                if(self.edit_qty2!=1):
                    self.cost_table=[]
                    for i in self.bio_full_system:
                        query2=frappe.db.sql("SELECT category,no_of_days,unit_price,total_price from `tabErection and Commisioning Table` where parent='"+str(i.item_description)+"'",as_dict=1)
                        if(query2):
                            ec_ar=[]
                            for ii in query2:
                                qt=i.w_qty
                                if(ii.category=="ERECTION"):
                                    if(i.item_description=="Lifting sump"):
                                        for bio in self.pre_treatment_table:
                                            if(bio.item_description=="LIFTING SUMP PUMP"):
                                                qt=bio.w_qty
                                    elif(i.item_description=="Neutralization System"):
                                        for bio in self.pre_treatment_table:
                                            if(bio.item_description=="NT PUMP"):
                                                qt=bio.w_qty
                                    elif(i.item_description=="De-Nitrification System"):
                                        for bio in self.pre_treatment_table:
                                            if(bio.item_description=="DNT PUMP"):
                                                qt=bio.w_qty
                                    elif(i.item_description=="SRS System"):
                                        for bio in self.pre_treatment_table:
                                            if(bio.item_description=="SRS PUMP"):
                                                qt=bio.w_qty
                                    elif(i.item_description=="Equalization System"):
                                        if(self.flow>0 and self.flow<=1500):qt=5
                                        elif(self.flow>1500 and self.flow<=3000):qt=7
                                        elif(self.flow>3000 and self.flow<=4500):qt=10
                                        elif(self.flow>4500):qt=12
                                    elif(i.item_description=="Clarifier Feed Tank"):
                                        qt=1
                                    elif(i.item_description=="Biological Oxidation System"):
                                        if(self.flow>0 and self.flow<=1000):qt=7
                                        elif(self.flow>1000 and self.flow<=2000):qt=10
                                        elif(self.flow>2000 and self.flow<=3000):qt=14
                                        elif(self.flow>3000 and self.flow<=4000):qt=18
                                        elif(self.flow>4000 and self.flow<=5000):qt=20
                                        elif(self.flow>5000):qt=25
                                    elif(i.item_description=="Circular Clarifier System"):
                                        if(float(i.range)>0 and float(i.range)<=10):qt=7
                                        elif(float(i.range)>10 and float(i.range)<=16):qt=8
                                        elif(float(i.range)>16):qt=10
                                    elif(i.item_description=="DO increase system"):
                                        if(self.flow>0 and self.flow<=3000):qt=3
                                        elif(self.flow>200):qt=7
                                    elif(i.item_description in ["Belt Press","Screw Press"]):
                                        if(i.w_qty>1):qt=5*((i.w_qty-1)*1.5)
                                    elif(i.item_description=="CTS MBR"):                        
                                        qt=7
                                    elif(i.item_description=="Lamella Settler"):
                                        qt=1
                                else:
                                    qt=1
                                    if(i.item_description=="Equalization System"):
                                        if(ii.category=="DRAWING"):
                                            if(self.flow>0 and self.flow<=3000):
                                                qt=2
                                            elif(self.flow>3000):
                                                qt=3
                                    elif(i.item_description=="Biological Oxidation System"):
                                        if(ii.category=="COMMISSIONING"):
                                            if(self.flow>0 and self.flow<=1500):qt=2
                                            elif(self.flow>1500 and self.flow<=3000):qt=3
                                            elif(self.flow>3000 and self.flow<=4500):qt=4
                                            elif(self.flow>4500):qt=5
                                        elif(ii.category=="DRAWING"):
                                            if(self.flow>0 and self.flow<=1500):qt=4
                                            elif(self.flow>1500 and self.flow<=3000):qt=6
                                            elif(self.flow>3000 and self.flow<=4500):qt=8
                                            elif(self.flow>4500):qt=10
                                        elif(ii.category=="VISIT CHARGES"):
                                            if(self.flow>0 and self.flow<=3000):qt=2
                                            elif(self.flow>3000):qt=3
                                    elif(i.item_description=="Circular Clarifier System"):
                                        if(ii.category=="DRAWING"):
                                            if(i.range in ["9","10"]):qt=5
                                            elif(i.range in ["13","16"]):qt=6
                                            elif(i.range in ["22","30"]):qt=7
                                    elif(i.item_description=="DO increase system"):
                                        if(ii.category=="COMMISSIONING"):
                                            if(self.flow>0 and self.flow<=3000):qt=2
                                            elif(self.flow>200):qt=3
                                ec_ar.append(ii.total_price*qt)
                            self.append("cost_table",{
                                    "system":i.item_description,
                                    "erection_template":i.item_description,
                                    "qty":i.w_qty,
                                    "unit_price":sum(ec_ar),
                                    "total_price":sum(ec_ar)
                                })
                    for sys in selected_s:
                        if(sys in ["CTS MBR","Micro Filtration - ASAHI","Degasser System","Hardness and Silica Removal System","Submerged MBR system - OVIVO","Submerged MBR system - KOCH"]):
                            query2=frappe.db.sql("SELECT category,no_of_days,unit_price,total_price from `tabErection and Commisioning Table` where parent='"+str(sys)+"'  ",as_dict=1)
                            if(query2):
                                ec_ar=[]
                                for ii in query2:
                                    qt=1
                                    if(ii.category=="ERECTION"):
                                        if(sys=="Micro Filtration - ASAHI"):
                                            if(self.flow>0 and self.flow<=1000):qt=8
                                            elif(self.flow>1000 and self.flow<=2000):qt=10
                                            elif(self.flow>2000 and self.flow<=3000):qt=12
                                            elif(self.flow>3000 and self.flow<=4000):qt=15
                                            elif(self.flow>4000 and self.flow<=5000):qt=18
                                            elif(self.flow>5000):qt=20
                                        elif(sys=="Reverse Osmosis"):
                                            if(self.flow>0 and self.flow<=1000):qt=7
                                            elif(self.flow>1000 and self.flow<=2000):qt=8
                                            elif(self.flow>2000 and self.flow<=3000):qt=10
                                            elif(self.flow>3000 and self.flow<=4000):qt=14
                                            elif(self.flow>4000 and self.flow<=5000):qt=20
                                            elif(self.flow>5000):qt=25
                                        elif(sys=="Reject Reverse Osmosis"):
                                            qt=7
                                        elif(sys=="Degasser System"):
                                            if(self.flow>0 and self.flow<=2500):qt=2
                                            elif(self.flow>2500 and self.flow<=5000):qt=3
                                            elif(self.flow>5000 and self.flow<=7500):qt=4
                                            elif(self.flow>7500):qt=5
                                        elif(sys=="Hardness and Silica Removal System"):
                                            if(self.flow>0 and self.flow<=200):qt=7
                                            elif(self.flow>200):qt=10
                                        elif(sys in ["Submerged MBR system - OVIVO","Submerged MBR system - KOCH"]):                        
                                            if(self.flow>0 and self.flow<=2000):qt=7
                                            elif(self.flow>2000 and self.flow<=4000):qt=10
                                            elif(self.flow>4000):qt=14
                                        elif(i.item_description=="CTS MBR"):                        
                                            qt=7
                                    else:
                                        qt=1
                                        if(sys=="Micro Filtration - ASAHI"):
                                            if(ii.category=="COMMISSIONING"):
                                                if(self.flow>0 and self.flow<=2000):qt=7
                                                elif(self.flow>2000 and self.flow<=4000):qt=10
                                                elif(self.flow>4000):qt=12
                                            if(ii.category=="DRAWING"):
                                                if(self.flow>0 and self.flow<=2000):qt=7
                                                elif(self.flow>2000 and self.flow<=4000):qt=10
                                                elif(self.flow>4000):qt=14
                                            elif(ii.category=="VISIT CHARGES"):
                                                if(self.flow>0 and self.flow<=2000):qt=2
                                                elif(self.flow>2000 and self.flow<=4000):qt=3
                                                elif(self.flow>4000):qt=4
                                        elif(sys=="Reverse Osmosis"):
                                            if(ii.category=="COMMISSIONING"):
                                                if(self.flow>0 and self.flow<=1000):qt=5
                                                elif(self.flow>1000 and self.flow<=3000):qt=7
                                                elif(self.flow>3000 and self.flow<=5000):qt=10
                                                elif(self.flow>5000):qt=14
                                            elif(ii.category=="DRAWING"):
                                                if(self.flow>0 and self.flow<=2000):qt=7
                                                elif(self.flow>2000 and self.flow<=3000):qt=10
                                                elif(self.flow>3000 and self.flow<=5000):qt=14
                                                elif(self.flow>5000):qt=20
                                            elif(ii.category=="VISIT CHARGES"):
                                                if(self.flow>0 and self.flow<=2000):qt=2
                                                elif(self.flow>2000 and self.flow<=4000):qt=3
                                                elif(self.flow>4000):qt=4
                                        elif(sys=="Reject Reverse Osmosis"):
                                            if(ii.category=="COMMISSIONING"):
                                                qt=5
                                            elif(ii.category=="DRAWING"):
                                                qt=7
                                            elif(ii.category=="VISIT CHARGES"):
                                                qt=2
                                        elif(sys=="Degasser System"):
                                            if(ii.category=="COMMISSIONING"):
                                                if(self.flow>0 and self.flow<=2500):qt=2
                                                elif(self.flow>2500 and self.flow<=5000):qt=3
                                                elif(self.flow>5000 and self.flow<=7500):qt=4
                                                elif(self.flow>7500):qt=5
                                            elif(ii.category=="DRAWING"):
                                                if(self.flow>0 and self.flow<=5000):qt=2
                                                elif(self.flow>5000 and self.flow<=7500):qt=3
                                                elif(self.flow>7500):qt=4
                                            elif(ii.category=="VISIT CHARGES"):
                                                if(self.flow>0 and self.flow<=3200):qt=1
                                                elif(self.flow>3200):qt=2
                                        elif(sys=="Hardness and Silica Removal System"):
                                            if(self.flow>0 and self.flow<=200):
                                                if(ii.category=="COMMISSIONING"):qt=3
                                                elif(ii.category=="DRAWING"):qt=5
                                                elif(ii.category=="VISIT CHARGES"):qt=3
                                            elif(self.flow>200):
                                                if(ii.category=="COMMISSIONING"):qt=5
                                                elif(ii.category=="DRAWING"):qt=10
                                                elif(ii.category=="VISIT CHARGES"):qt=5
                                        elif(sys in ["Submerged MBR system - OVIVO","Submerged MBR system - KOCH"]):
                                            if(ii.category=="COMMISSIONING"):
                                                if(self.flow>0 and self.flow<=2000):qt=5
                                                elif(self.flow>2000 and self.flow<=4000):qt=7
                                                elif(self.flow>4000):qt=10
                                            elif(ii.category=="VISIT CHARGES"):
                                                if(self.flow>0 and self.flow<=2000):qt=2
                                                elif(self.flow>2000 and self.flow<=4000):qt=3
                                                elif(self.flow>4000):qt=4
                                        elif(i.item_description=="CTS MBR"):
                                            if(ii.category=="COMMISSIONING"):
                                                qt=5
                                            elif(ii.category=="VISIT CHARGES"):
                                                qt=2
                                    ec_ar.append(ii.total_price*qt)
                                self.append("cost_table",{
                                        "system":sys,
                                        "erection_template":sys,
                                        "qty":1,
                                        "unit_price":sum(ec_ar),
                                        "total_price":sum(ec_ar)
                                    })
                for i in self.cost_table:
                    if(i.total_price is not None):
                        cost.append(i.total_price)
                self.erection_cost=sum(cost)
            
            
                #fabrication
                for i in self.fabrication_table:
                    if(i.system == 'MICRO FILTRATION' and self.edit_mffe!=1):
                        self.mf_fabrication_cost = i.total_charges
                        
                #erection
                for i in self.cost_table:
                    if(i.erection_template == 'Submerged MBR system - KOCH' and self.edit_kochfe!=1):
                        self.mbrk_erection_cost = i.total_price
                    elif(i.erection_template == 'Submerged MBR system - OVIVO' and self.edit_ovivofe!=1):
                        self.mbro_erection_cost = i.total_price
                    elif(i.erection_template == 'Micro Filtration - ASAHI' and self.edit_mffe!=1):
                        self.mf_erection_cost = i.total_price
                    elif(i.erection_template == 'Degasser System' and self.edit_dgtfe!=1):
                        self.dgt_erection_price = i.total_price
                    elif(i.erection_template == 'CTS' and self.edit_ctsfe!=1):
                        self.cts_erection = i.total_price
                    elif(i.erection_template == 'CTS MBR' and self.edit_mbr_ctsfe!=1):
                        self.mbr_cts_erection = i.total_price
                        
                not_linked=[]
                self.not_linked_cost=0
                for i in self.mf_not_linked_table:
                    if(i.total_price is not None):
                        not_linked.append(i.total_price)
                self.not_linked_cost=sum(not_linked)
                
                #mf_total
                mf_total=[]
                # for i in self.mf_table:
                #     if(i.total_price is not None):
                #         mf_total.append(i.total_price)
                # self.mf_line_item_cost = sum(mf_total)
                # if(self.mf_fabrication_cost is None):
                #     self.mf_fabrication_cost=0
                # if(self.mf_erection_cost is None):
                #     self.mf_erection_cost=0
                
                for i in self.mf_full_system:
                    if(i.total_price is not None):
                        mf_total.append(i.total_price)
                #self.mf_cost = sum(mf_total) + self.not_linked_cost
                self.mf_cost = sum(mf_total)
                self.mf_pipe_cost = self.mf_cost*(self.mf_pipes_fittings_valves/100)
                self.total_mf_cost=self.mf_cost+self.mf_pipe_cost + self.mf_fabrication_cost + self.mf_erection_cost
                
                mf_electrical=[]
                for i in self.mf_electrical_items:
                    if(i.total_price is not None):
                        mf_electrical.append(i.total_price)
                
                mf_plc=[]
                for i in self.mf_plc_items:
                    if(i.total_price is not None):mf_plc.append(i.total_price)        
                        
                self.mf_electrical_cost=sum(mf_electrical) + sum(mf_plc)
                self.overall_mf_cost=self.total_mf_cost+self.mf_electrical_cost
                
                #mbr_total
                mbr_not_linked=[]
                self.cost_for_not_linked_items=0
                for i in self.mbr_koch_not_linked:
                    if(i.total_price is not None):
                        mbr_not_linked.append(i.total_price)
                self.cost_for_not_linked_items=sum(mbr_not_linked)
                
                mbr_total=[]
                # for i in self.mbr_koch_table:
                #     if(i.total_price is not None):
                #         mbr_total.append(i.total_price)
                # self.mbrk_line_items_cost = sum(mbr_total) 
                if(self.mbrk_erection_cost is None):
                    self.mbrk_erection_cost=0
                
                for i in self.mbrk_full_system:
                    if(i.total_price is not None):
                        mbr_total.append(i.total_price)
                    
                # self.mbr_cost = sum(mbr_total) + self.cost_for_not_linked_items
                self.mbr_cost = sum(mbr_total)
                self.mbr_pipe_cost = self.mbr_cost*(self.mbr_pipes_fittings_valves/100)
                self.mbrk_cost=self.mbr_cost+self.mbr_pipe_cost+self.mbrk_erection_cost
                
                mbr_electrical=[]
                for i in self.mbr_electrical_items:
                    if(i.total_price is not None):
                        mbr_electrical.append(i.total_price)
                        
                mbrk_plc=[]
                for i in self.mbrk_plc_items:
                    if(i.total_price is not None):
                        mbrk_plc.append(i.total_price)
                
                self.mbr_electrical_cost=sum(mbr_electrical) + sum(mbrk_plc)
                self.mbr_overall_cost=self.mbrk_cost+self.mbr_electrical_cost
                
                #mbr_ovivo
                mbr_ovivo_not_linked=[]
                self.ovivo_not_linked_cost=0
                for i in self.mbr_ovivo_not_linked_items:
                    if(i.total_price is not None):
                        mbr_ovivo_not_linked.append(i.total_price)
                self.ovivo_not_linked_cost=sum(mbr_ovivo_not_linked)
                
                mbr_ovivo_total=[]
                # for i in self.mbr_ovivo_table:
                #     if(i.total_price is not None):
                #         mbr_ovivo_total.append(i.total_price)
                # self.ovivo_line_items_cost = sum(mbr_ovivo_total)
                
                for i in self.mbro_full_system:
                    if(i.total_price is not None):
                        mbr_ovivo_total.append(i.total_price)
                        
                # self.ovivo_cost = sum(mbr_ovivo_total)+self.ovivo_not_linked_cost
                self.ovivo_cost = sum(mbr_ovivo_total)
                self.ovivo_pipe_cost = self.ovivo_cost*(self.ovivo_pipes_fittings_valves/100)
                self.mbr_ovivo_cost=self.ovivo_cost + self.ovivo_pipe_cost + self.mbro_erection_cost
                
                ovivo_electrical=[]
                for i in self.ovivo_electrical_items:
                    if(i.total_price is not None):
                        ovivo_electrical.append(i.total_price)
                        
                ovivo_plc=[]
                for i in self.mbro_plc_items:
                    if(i.total_price is not None):
                        ovivo_plc.append(i.total_price)
                        
                self.ovivo_electrical_cost=sum(ovivo_electrical) + sum(ovivo_plc)
                self.overall_mbr_ovivo_cost=self.mbr_ovivo_cost+self.ovivo_electrical_cost
                
                #mbr_cts
                mbr_cts_not_linked=[]
                self.mbr_cts_not_linked_cost=0
                for i in self.mbr_cts_not_linked_items:
                    if(i.total_price is not None):
                        mbr_cts_not_linked.append(i.total_price)
                self.mbr_cts_not_linked_cost=sum(mbr_cts_not_linked)
                
                mbr_cts_total=[]
                # for i in self.mbr_cts_table:
                #     if(i.total_price is not None):
                #         mbr_cts_total.append(i.total_price)
                
                for i in self.mbr_cts_full_system:
                    if(i.total_price is not None):
                        mbr_cts_total.append(i.total_price)
                
                self.mbr_cts_cost_without_pipes = sum(mbr_cts_total)
                self.mbr_cts_pipe_cost = self.mbr_cts_cost_without_pipes*(self.mbr_cts_pipes_fittings_valves/100)
                self.mbr_cts_cost=self.mbr_cts_cost_without_pipes+self.mbr_cts_pipe_cost+self.mbr_cts_erection
                
                mbr_cts_electrical=[]
                for i in self.mbr_cts_electrical_items:
                    if(i.total_price is not None):
                        mbr_cts_electrical.append(i.total_price)
                    
                mbr_cts_plc=[]
                for i in self.mbr_cts_plc_items:
                    if(i.total_price is not None):
                        mbr_cts_plc.append(i.total_price)
                        
                self.mbr_cts_electrical_cost=sum(mbr_cts_electrical) + sum(mbr_cts_plc)
                self.overall_mbr_cts_cost=self.mbr_cts_cost+self.mbr_cts_electrical_cost
                
                ##Chemical Treatment System
                
                cts_not_linked=[]
                self.cts_not_linked_cost=0
                for i in self.cts_not_linked_items:
                    if(i.total_price==None):
                        i.total_price=0
                    cts_not_linked.append(i.total_price)
                self.cts_not_linked_cost=sum(cts_not_linked)
                
                cts_total=[]
                # for i in self.cts_items:
                #     if(i.total_price==None):
                #         i.total_price=0
                #     cts_total.append(i.total_price)
                
                for i in self.cts_full_system:
                    if(i.total_price==None):
                        i.total_price=0
                    cts_total.append(i.total_price)
                    
                self.cts_total=sum(cts_total)
                self.cts_pipe_cost = self.cts_total*(self.cts_pipes_fittings_valves/100)
                self.cts_final_cost=sum(cts_total)+self.cts_pipe_cost+self.cts_erection
                
                
                cts_electrical_cost=[]
                for i in self.cts_electrical_items:
                    if(i.total_price==None):
                        i.total_price=0
                    cts_electrical_cost.append(i.total_price)
                    
                
                cts_plc=[]
                for i in self.cts_plc_items:
                    if(i.total_price is not None):cts_plc.append(i.total_price)
                
                self.cts_electrical_cost=sum(cts_electrical_cost) + sum(cts_plc)
                self.cts_overall_cost=self.cts_final_cost+self.cts_electrical_cost
                ##Degasser System
                dgt_not_linked=[]
                self.dgt_not_linked_cost=0
                for i in self.dgt_not_linked_items:
                    if(i.total_price==None):
                        i.total_price=0
                    dgt_not_linked.append(i.total_price)
                self.dgt_not_linked_cost=sum(dgt_not_linked)
                
                if(self.dgt_erection_price is None):
                    self.dgt_erection_price=0
                    
                dgt_total=[]
                # for i in self.dgt_items:
                #     if(i.total_price==None):
                #         i.total_price=0
                #     dgt_total.append(i.total_price)
                    
                for i in self.dgt_full_system:
                    if(i.total_price==None):
                        i.total_price=0
                    dgt_total.append(i.total_price)
                    
                # self.dgt_line_items_cost = sum(dgt_total)
                self.dgt_cost=sum(dgt_total)
                self.dgt_pipe_cost = self.dgt_cost*(self.dgt_pipes_fittings_valves/100)
                self.dgt_total_cost=self.dgt_cost+self.dgt_pipe_cost+self.dgt_erection_price
                
                dgt_electrical_cost=[]
                for i in self.dgt_electrical_items:
                    if(i.total_price==None):
                        i.total_price=0
                    dgt_electrical_cost.append(i.total_price)
                
                dgt_plc=[]
                for i in self.dgt_plc_items:
                    if(i.total_price is not None):dgt_plc.append(i.total_price)
                 
                self.dgt_electrical_cost=sum(dgt_electrical_cost) + sum(dgt_plc)
                self.dgt_overall_cost=self.dgt_total_cost+self.dgt_electrical_cost
                
                ##ANAEROBIC SYSTEM
                ana_arr1=[]
                ana_arr2=[]
                if "Anaerobic Bar Screener" in selected_s:
                    ana_arr1.append("BAR SCREENER")
                    ana_arr2.append("Bar Screener")
                if "Anaerobic Lifting Pump" in selected_s:
                    ana_arr1.extend(["LIFTING PUMP", "LPS LEVEL FLOAT", "LPS LEVEL TRANSMITTER", "LPS PIPES"])
                    ana_arr2.extend(["Lifting Pump", "Lifting Pump", "Lifting Pump", "Lifting Pump"])
                if "Anaerobic Ammonia Striper" in selected_s:
                    ana_arr1.extend(["AMMONIA STRIPPER", "AS. BLOWER FAN", "AS. PALL RINGS", "AS. PH SENSOR", "AS. DOSING PUMP", "AS. DOSING PUMP FRAME"])
                    ana_arr2.extend(["Ammonia Striper", "Ammonia Striper", "Ammonia Striper", "Ammonia Striper", "Ammonia Striper", "Ammonia Striper"])
                if "Anaerobic Neutralization" in selected_s:
                    ana_arr1.extend(["FEED PUMP", "NT EMFM", "NT DOSING PUMP", "NT. DOSING PUMP FRAME", "NT PH SENSOR", "NT PIPES", "NT LEVEL FLOAT", "NT LEVEL TRANSMITTER", "NT LIFTING"])
                    ana_arr2.extend(["Anaerobic Neutralization", "Anaerobic Neutralization", "Anaerobic Neutralization", "Anaerobic Neutralization", "Anaerobic Neutralization", "Anaerobic Neutralization", "Anaerobic Neutralization", "Anaerobic Neutralization", "Anaerobic Neutralization"])
                if "Anaerobic Settler" in selected_s:
                    ana_arr1.extend(["ANAEROBIC SETTLER", "AN. SLUDGE PUMP", "AN. SRS PUMP", "AN. SRS EMFM", "AN. SRS LEVEL FLOAT", "AN. SRS LEVEL TRANSMITTER"])
                    ana_arr2.extend(["Anaerobic Settler", "Anaerobic Settler", "Anaerobic Settler", "Anaerobic Settler", "Anaerobic Settler", "Anaerobic Settler"])
                if "Anaerobic Lamella Settler" in selected_s:
                    ana_arr1.extend(["LAMELLA SETTLER", "LAM. SLUDGE PUMP", "LAM. SLUDGE PUMP PIPES", "LAM. SLUDGE PUMP LEVEL FLOAT", "LAM. DOSING PUMP-1", "LAM. DOSING PUMP-2", "LAM. DOSING PUMP-3", "LAM. DOSING PUMP-1 FRAME", "LAM. DOSING PUMP-2 FRAME", "LAM. DOSING PUMP-3 FRAME", "LAM. STATIC MIXER - PVDF", "LAM. STATIC MIXER - SS316"])
                    ana_arr2.extend(["Anaerobic Lamella Settler", "Anaerobic Lamella Settler", "Anaerobic Lamella Settler", "Anaerobic Lamella Settler", "Anaerobic Lamella Settler", "Anaerobic Lamella Settler", "Anaerobic Lamella Settler", "Anaerobic Lamella Settler", "Anaerobic Lamella Settler", "Anaerobic Lamella Settler", "Anaerobic Lamella Settler", "Anaerobic Lamella Settler"])
                if "Anaerobic CTS" in selected_s:
                    ana_arr1.extend(["CTS. FEED PUMP", "CTS. SLUDGE PUMP", "CTS. EMFM", "CTS. AGITATOR", "CTS. PH SENSOR", "CTS. LEVEL FLOAT", "CTS. PIPE FLOCCULATION", "CTS. DOSING PUMP-1", "CTS. DOSING PUMP-2", "CTS. DOSING PUMP-3", "CTS. DOSING PUMP-4", "CTS. DOSING PUMP-5", "CTS. DOSING PUMP-1 FRAME", "CTS. DOSING PUMP-2 FRAME", "CTS. DOSING PUMP-3 FRAME", "CTS. DOSING PUMP-4 FRAME", "CTS. DOSING PUMP-5 FRAME"])
                    ana_arr2.extend(["Anaerobic CTS", "Anaerobic CTS", "Anaerobic CTS", "Anaerobic CTS", "Anaerobic CTS", "Anaerobic CTS", "Anaerobic CTS", "Anaerobic CTS", "Anaerobic CTS", "Anaerobic CTS", "Anaerobic CTS", "Anaerobic CTS", "Anaerobic CTS", "Anaerobic CTS", "Anaerobic CTS", "Anaerobic CTS", "Anaerobic CTS"])
                
                one_time_arr=[]
                self.anaerobic_items=[]
                self.anaerobic_full_system=[]
                for ana in range(len(ana_arr1)):
                    self.append("anaerobic_items",{
                        "item_description":ana_arr1[ana],
                        "system":ana_arr2[ana]
                    })
                    if(ana_arr2[ana] not in one_time_arr):
                        one_time_arr.append(ana_arr2[ana])
                        self.append("anaerobic_full_system",{
                            "item_description":ana_arr2[ana]
                        })
                
                #margin-cost
                self.mf_tax_cost = self.overall_mf_cost * (float(self.mftax)/100)
                self.mf_transport_cost = self.overall_mf_cost * (float(self.mftransport)/100)
                self.include_tax_cost = (self.overall_mf_cost + self.mf_tax_cost + self.mf_transport_cost)
                self.total_cost_for_mf = (self.overall_mf_cost + self.mf_tax_cost + self.mf_transport_cost)
                if(self.margin_for_expense_calculation is not None):
                    self.margin_for_expense_calculation_cost = self.include_tax_cost * (float(self.margin_for_expense_calculation)/100)
                self.mf_overhead_cost =self.margin_for_expense_calculation_cost * (float(self.overhead_percentage)/100)
                self.e_c=self.margin_for_expense_calculation_cost * (float(self.e_c_)/100)
                self.mf_agent_commission_cost=self.margin_for_expense_calculation_cost * (float(self.agent_commission)/100)
                self.mf_guarantee_clause_cost=(self.e_c+self.margin_for_expense_calculation_cost + self.mf_overhead_cost + self.mf_agent_commission_cost) * (float(self.guarantee_clause_charge)/100)
                self.margin_cost_without_margin = (self.include_tax_cost+self.e_c + self.mf_overhead_cost + self.mf_agent_commission_cost + self.mf_guarantee_clause_cost)
                self.mf_cost_with_margin = self.margin_cost_without_margin * (float(self.margin_percentage)/100)
                ##mbr koch
                self.mbr_tax_cost = self.mbr_overall_cost * (float(self.mbr_tax)/100)
                self.mbr_transport_cost = self.mbr_overall_cost * (float(self.mbr_transport)/100)
                self.total_mbr_cost = (self.mbr_overall_cost + self.mbr_tax_cost + self.mbr_transport_cost)
                self.total_cost_for_mbrk = (self.mbr_overall_cost + self.mbr_tax_cost + self.mbr_transport_cost)
                if(self.mbr_margin_for_expense_calculation is not None):
                    self.mbr_marginal_cost_for_expense_calculation = self.total_mbr_cost * (float(self.mbr_margin_for_expense_calculation)/100)
                self.mbr_overhead_cost =self.mbr_marginal_cost_for_expense_calculation * (float(self.mbr_overhead_percentage)/100)
                self.mbr_e_c=self.mbr_marginal_cost_for_expense_calculation * (float(self.mbr_e_c_)/100)
                self.mbr_agent_commission_cost=self.mbr_marginal_cost_for_expense_calculation * (float(self.mbr_agent_commission)/100)
                self.mbr_guarantee_clause_cost=(self.mbr_e_c+self.mbr_marginal_cost_for_expense_calculation + self.mbr_overhead_cost + self.mbr_agent_commission_cost) * (float(self.mbr_guarantee_clause_charge)/100)
                self.mbr_grand_total = (self.total_mbr_cost+self.mbr_e_c + self.mbr_overhead_cost + self.mbr_agent_commission_cost + self.mbr_guarantee_clause_cost)
                self.mbr_selling_price = self.mbr_grand_total * (float(self.mbr_margin_percentage)/100)
                ##mbr ovivo
                self.ovivo_tax_cost = self.overall_mbr_ovivo_cost * (float(self.ovivo_tax)/100)
                self.ovivo_transport_cost = self.overall_mbr_ovivo_cost * (float(self.ovivo_transport)/100)
                self.total_ovivo_cost = (self.overall_mbr_ovivo_cost + self.ovivo_tax_cost + self.ovivo_transport_cost)
                self.total_cost_for_mbro = (self.overall_mbr_ovivo_cost + self.ovivo_tax_cost + self.ovivo_transport_cost)
                if(self.ovivo_margin_for_expense_calculation is not None):
                    self.ovivo_marginal_cost_for_expense_calculation = self.total_ovivo_cost * (float(self.ovivo_margin_for_expense_calculation)/100)
                self.ovivo_overhead_cost =self.ovivo_marginal_cost_for_expense_calculation * (float(self.ovivo_overhead_percentage)/100)
                self.ovivo_e_c=self.ovivo_marginal_cost_for_expense_calculation * (float(self.ovivo_e_c_)/100)
                self.ovivo_agent_commission_cost=self.ovivo_marginal_cost_for_expense_calculation * (float(self.ovivo_agent_commission)/100)
                self.ovivo_guarantee_clause_cost=(self.ovivo_e_c+self.ovivo_marginal_cost_for_expense_calculation + self.ovivo_overhead_cost + self.ovivo_agent_commission_cost) * (float(self.ovivo_guarantee_clause_charge)/100)
                self.ovivo_grand_total = (self.total_ovivo_cost+self.ovivo_e_c + self.ovivo_overhead_cost + self.ovivo_agent_commission_cost + self.ovivo_guarantee_clause_cost)
                self.ovivo_selling_price = self.ovivo_grand_total * (float(self.ovivo_margin_percentage)/100)
                ##mbr cts
                self.mbr_cts_tax_cost = self.overall_mbr_cts_cost * (float(self.mbr_cts_tax)/100)
                self.mbr_cts_transport_cost = self.overall_mbr_cts_cost * (float(self.mbr_cts_transport)/100)
                self.total_mbr_cts_cost = (self.overall_mbr_cts_cost + self.mbr_cts_tax_cost + self.mbr_cts_transport_cost)
                self.total_cost_for_mbr_cts = (self.overall_mbr_cts_cost + self.mbr_cts_tax_cost + self.mbr_cts_transport_cost)
                if(self.mbr_cts_margin_for_expense_calculation is not None):
                    self.mbr_cts_marginal_cost_for_expense_calculation = self.total_mbr_cts_cost * (float(self.mbr_cts_margin_for_expense_calculation)/100)
                self.mbr_cts_overhead_cost =self.mbr_cts_marginal_cost_for_expense_calculation * (float(self.mbr_cts_overhead_percentage)/100)
                self.mbr_cts_e_c=self.mbr_cts_marginal_cost_for_expense_calculation * (float(self.mbr_cts_e_c_)/100)
                self.mbr_cts_agent_commission_cost=self.mbr_cts_marginal_cost_for_expense_calculation * (float(self.mbr_cts_agent_commission)/100)
                self.mbr_cts_guarantee_clause_cost=(self.mbr_cts_e_c+self.mbr_cts_marginal_cost_for_expense_calculation + self.mbr_cts_overhead_cost + self.mbr_cts_agent_commission_cost) * (float(self.mbr_cts_guarantee_clause_charge)/100)
                self.mbr_cts_grand_total = (self.total_mbr_cts_cost+self.mbr_cts_e_c + self.mbr_cts_overhead_cost + self.mbr_cts_agent_commission_cost + self.mbr_cts_guarantee_clause_cost)
                self.mbr_cts_selling_price = self.mbr_cts_grand_total * (float(self.mbr_cts_margin_percentage)/100)
                ##cts
                self.cts_tax_cost = self.cts_overall_cost * (float(self.cts_tax)/100)
                self.cts_transport_cost = self.cts_overall_cost * (float(self.cts_transport)/100)
                self.total_cts_cost = (self.cts_overall_cost + self.cts_tax_cost + self.cts_transport_cost)
                self.total_cost_for_cts = (self.cts_overall_cost + self.cts_tax_cost + self.cts_transport_cost)
                if(self.cts_margin_for_expense_calculation is not None):
                    self.cts_marginal_cost_for_expense_calculation = self.total_cts_cost * (float(self.cts_margin_for_expense_calculation)/100)
                self.cts_overhead_cost =self.cts_marginal_cost_for_expense_calculation * (float(self.cts_overhead)/100)
                self.cts_e_c_cost=self.cts_marginal_cost_for_expense_calculation * (float(self.cts_e_c)/100)
                self.cts_agent_commission_cost=self.cts_marginal_cost_for_expense_calculation * (float(self.cts_agent_commission)/100)
                self.cts_guarantee_clause_cost=(self.cts_e_c_cost+self.cts_marginal_cost_for_expense_calculation + self.cts_overhead_cost + self.cts_agent_commission_cost) * (float(self.cts_guarantee_clause_charge)/100)
                self.cts_grand_total = (self.total_cts_cost+self.cts_e_c_cost + self.cts_overhead_cost + self.cts_agent_commission_cost + self.cts_guarantee_clause_cost)
                self.cts_selling_price = self.cts_grand_total * (float(self.cts_margin)/100)
                ##Chlorination
                self.clt_tax_cost = self.chlorination_total * (float(self.clt_tax)/100)
                self.clt_transport_cost = self.chlorination_total * (float(self.clt_transport)/100)
                self.total_clt_cost = (self.chlorination_total + self.clt_tax_cost + self.clt_transport_cost)
                self.total_cost_for_chlorination = (self.chlorination_total + self.clt_tax_cost + self.clt_transport_cost)
                if(self.clt_margin_for_expense_calculation is not None):
                    self.clt_marginal_cost_for_expense_calculation = self.total_clt_cost * (float(self.clt_margin_for_expense_calculation)/100)
                self.clt_overhead_cost =self.clt_marginal_cost_for_expense_calculation * (float(self.clt_overhead)/100)
                self.clt_e_c_cost=self.clt_marginal_cost_for_expense_calculation * (float(self.clt_e_c)/100)
                self.clt_agent_commission_cost=self.clt_marginal_cost_for_expense_calculation * (float(self.clt_agent_commission)/100)
                self.clt_guarantee_clause_cost=(self.clt_e_c_cost+self.clt_marginal_cost_for_expense_calculation + self.clt_overhead_cost + self.clt_agent_commission_cost) * (float(self.clt_guarantee_clause_charge)/100)
                self.clt_grand_total = (self.total_clt_cost+self.clt_e_c_cost + self.clt_overhead_cost + self.clt_agent_commission_cost + self.clt_guarantee_clause_cost)
                self.clt_selling_price = self.clt_grand_total * (float(self.clt_margin)/100)
                ##CTS COOLING TOWER
                self.cts_cooling_tower_tax_cost = self.cts_cooling_tower_cost * (float(self.cts_cooling_tower_tax)/100)
                self.cts_cooling_tower_transport_cost = self.cts_cooling_tower_cost * (float(self.cts_cooling_tower_transport)/100)
                self.total_cts_cooling_tower_cost = (self.cts_cooling_tower_cost + self.cts_cooling_tower_tax_cost + self.cts_cooling_tower_transport_cost)
                self.total_cost_for_cts_cooling_tower = (self.cts_cooling_tower_cost + self.cts_cooling_tower_tax_cost + self.cts_cooling_tower_transport_cost)
                if(self.cts_cooling_tower_margin_for_expense_calculation is not None):
                    self.cts_cooling_tower_marginal_cost_for_expense_calculation = self.total_cts_cooling_tower_cost * (float(self.cts_cooling_tower_margin_for_expense_calculation)/100)
                self.cts_cooling_tower_overhead_cost =self.cts_cooling_tower_marginal_cost_for_expense_calculation * (float(self.cts_cooling_tower_overhead)/100)
                self.cts_cooling_tower_e_c_cost=self.cts_cooling_tower_marginal_cost_for_expense_calculation * (float(self.cts_cooling_tower_e_c)/100)
                self.cts_cooling_tower_agent_commission_cost=self.cts_cooling_tower_marginal_cost_for_expense_calculation * (float(self.cts_cooling_tower_agent_commission)/100)
                self.cts_cooling_tower_guarantee_clause_cost=(self.cts_cooling_tower_e_c_cost+self.cts_cooling_tower_marginal_cost_for_expense_calculation + self.cts_cooling_tower_overhead_cost + self.cts_cooling_tower_agent_commission_cost) * (float(self.cts_cooling_tower_guarantee_clause_charge)/100)
                self.cts_cooling_tower_grand_total = (self.total_cts_cooling_tower_cost+self.cts_cooling_tower_e_c_cost + self.cts_cooling_tower_overhead_cost + self.cts_cooling_tower_agent_commission_cost + self.cts_cooling_tower_guarantee_clause_cost)
                self.cts_cooling_tower_selling_price = self.cts_cooling_tower_grand_total * (float(self.cts_cooling_tower_margin)/100)
                ##Degasser System
                self.dgt_tax_cost = self.dgt_overall_cost * (float(self.dgt_tax)/100)
                self.dgt_transport_cost = self.dgt_overall_cost * (float(self.dgt_transport)/100)
                self.total_dgt_cost = (self.dgt_overall_cost + self.dgt_tax_cost + self.dgt_transport_cost)
                self.total_cost_for_degasser = (self.dgt_overall_cost + self.dgt_tax_cost + self.dgt_transport_cost)
                if(self.dgt_margin_for_expense_calculation is not None):
                    self.dgt_marginal_cost_for_expense_calculation = self.total_dgt_cost * (float(self.dgt_margin_for_expense_calculation)/100)
                self.dgt_overhead_cost =self.dgt_marginal_cost_for_expense_calculation * (float(self.dgt_overhead)/100)
                self.dgt_e_c_cost=self.dgt_marginal_cost_for_expense_calculation * (float(self.dgt_e_c)/100)
                self.dgt_agent_commission_cost=self.dgt_marginal_cost_for_expense_calculation * (float(self.dgt_agent_commission)/100)
                self.dgt_guarantee_clause_cost=(self.dgt_e_c_cost+self.dgt_marginal_cost_for_expense_calculation + self.dgt_overhead_cost + self.dgt_agent_commission_cost) * (float(self.dgt_guarantee_clause_charge)/100)
                self.dgt_grand_total = (self.total_dgt_cost+self.dgt_e_c_cost + self.dgt_overhead_cost + self.dgt_agent_commission_cost + self.dgt_guarantee_clause_cost)
                self.dgt_selling_price = self.dgt_grand_total * (float(self.dgt_margin)/100)
                ##bio
                for i in self.bio_full_system:
                    if(i.item_description == "Hardness and Color Removal System"):
                        i.w_qty=1
                        i.unit_price = self.chlorination_total + self.cts_selling_price
                        i.total_price = i.unit_price * i.w_qty
                
                bio_arr=[]
                self.bio_cost=0
                for k in self.pre_treatment_full_system:
                    k.pipe = 0 if k.pipe is None else k.pipe
                    k.total_price_with_erefab = (float(k.unit_price)+float(k.bom_unit_price)+float(k.pipe))*float(k.w_qty)+float(k.erection)+float(k.fabrication)
                    if(k.total_price_with_erefab is not None):
                        bio_arr.append(k.total_price_with_erefab)
                self.bio_cost=sum(bio_arr)
                for k in self.pre_treatment_special_table:
                    k.pipe = 0 if k.pipe is None else k.pipe
                    k.total_price_with_erefab = (float(k.unit_price)+float(k.bom_unit_price)+float(k.pipe))*float(k.w_qty)+float(k.erection)+float(k.fabrication)
                    
                bio_electrical=[]
                for i in self.bio_electrical_items:
                    if(i.total_price is not None):bio_electrical.append(i.total_price)
                    
                bio_plc=[]
                for i in self.bio_plc_items:
                    if(i.total_price is not None):bio_plc.append(i.total_price)
                    
                self.bio_electrical_cost=sum(bio_electrical) + sum(bio_plc)
                # self.overall_bio_cost=sum(bio_not_linked)+sum(bio_cost)+sum(bio_electrical)
                self.overall_bio_cost = self.bio_cost + self.bio_electrical_cost
                self.bio_tax_cost = self.overall_bio_cost * (float(self.bio_tax)/100)
                self.bio_transport_cost = self.overall_bio_cost * (float(self.bio_transport)/100)
                self.total_bio_cost = (self.overall_bio_cost + self.bio_tax_cost + self.bio_transport_cost)
                self.total_cost_for_bio = (self.overall_bio_cost + self.bio_tax_cost + self.bio_transport_cost)
                if(self.bio_margin_for_expense_calculation is not None):
                    self.bio_marginal_cost_for_expense_calculation = self.total_bio_cost * (float(self.bio_margin_for_expense_calculation)/100)
                self.bio_overhead_cost =self.bio_marginal_cost_for_expense_calculation * (float(self.bio_overhead_percentage)/100)
                self.bio_e_c=self.bio_marginal_cost_for_expense_calculation * (float(self.bio_e_c_)/100)
                self.bio_agent_commission_cost=self.bio_marginal_cost_for_expense_calculation * (float(self.bio_agent_commission)/100)
                self.bio_guarantee_clause_cost=(self.bio_e_c+self.bio_marginal_cost_for_expense_calculation + self.bio_overhead_cost + self.bio_agent_commission_cost) * (float(self.bio_guarantee_clause_charge)/100)
                self.bio_grand_total = (self.total_bio_cost+self.bio_e_c + self.bio_overhead_cost + self.bio_agent_commission_cost + self.bio_guarantee_clause_cost)
                self.bio_selling_price = self.bio_grand_total * (float(self.bio_margin_percentage)/100)
                ro_price1=0
                ro_price2=0
                ro_price3=0
                if(self.choose_ro_template is not None and self.choose_ro_template!=''):
                    ro_price1 = frappe.db.sql("SELECT include_tax_cost from `tabRO Standard Items` where name='"+str(self.choose_ro_template)+"' ",as_dict=1)[0].include_tax_cost if "Reverse Osmosis" in selected_s else 0
                if(self.rewolutte_ro is not None and self.rewolutte_ro!=''):
                    ro_price2 = frappe.db.sql("SELECT include_tax_cost from `tabRO Standard Items` where name='"+str(self.rewolutte_ro)+"' ",as_dict=1)[0].include_tax_cost if "Rewolutte RO" in selected_s else 0
                if(self.choose_rro_template is not None and self.choose_rro_template!=''):
                    ro_price3 = frappe.db.sql("SELECT include_tax_cost from `tabRO Standard Items` where name='"+str(self.choose_rro_template)+"' ",as_dict=1)[0].include_tax_cost if "Reject Reverse Osmosis" in selected_s else 0
                self.ro_cost = ro_price1
                self.rewro_cost = ro_price2
                self.rro_cost = ro_price3
                self.cip_cost = 0
                self.cip_cost2 = 0
                self.cip_cost3 = 0
                if(frappe.db.get_value("Startup Sheet",self.project_startup_sheet,"choose_cip")!=None):
                    self.choose_cip=frappe.db.get_value("Startup Sheet",self.project_startup_sheet,"choose_cip")
                if(self.choose_cip):
                    cip_cost1 = frappe.db.get_value("CIP Standard Items",self.choose_cip,"include_tax_cost")
                    self.cip_cost = cip_cost1*float(frappe.db.get_value("Startup Sheet",self.project_startup_sheet,"cip_quantity"))
                if(self.choose_cip2):
                    cip_cost2 = frappe.db.get_value("CIP Standard Items",self.choose_cip2,"include_tax_cost")
                    self.cip_cost2 = cip_cost2*float(frappe.db.get_value("Startup Sheet",self.project_startup_sheet,"cip_quantity2"))
                if(self.choose_cip3):
                    cip_cost3 = frappe.db.get_value("CIP Standard Items",self.choose_cip3,"include_tax_cost")
                    self.cip_cost3 = cip_cost3*float(frappe.db.get_value("Startup Sheet",self.project_startup_sheet,"cip_quantity3"))
                    
                
                frappe.db.set_value('Startup Sheet',self.project_startup_sheet, 'cost_working', self.name)
                if(self.ro_cost>0):
                    self.ro_with_cip = self.ro_cost+self.cip_cost
                    self.rocip_margin_cost_for_expense_calculation = float(self.ro_with_cip) * (float(self.rocip_margin_for_expense_calculation)/100)
                    self.rocip_overhead_cost =self.rocip_margin_cost_for_expense_calculation * (float(self.rocip_overhead)/100)
                    self.rocip_e_c_cost=self.rocip_margin_cost_for_expense_calculation * (float(self.rocip_e_c)/100)
                    self.rocip_agent_commission_cost=self.rocip_margin_cost_for_expense_calculation * (float(self.rocip_agent_commission)/100)
                    self.rocip_guarantee_clause_cost=(self.rocip_e_c_cost+self.rocip_margin_cost_for_expense_calculation + self.rocip_overhead_cost + self.rocip_agent_commission_cost) * (float(self.rocip_guarantee_clause_charge)/100)
                    self.rocip_grand_total = (self.ro_with_cip+self.rocip_e_c_cost + self.rocip_overhead_cost + self.rocip_agent_commission_cost + self.rocip_guarantee_clause_cost)
                    self.rocip_price = self.rocip_grand_total * (float(self.rocip_margin)/100)
                if(self.rro_cost>0):
                    self.rro_with_cip = self.rro_cost+self.cip_cost2
                    self.rrocip_margin_cost_for_expense_calculation = float(self.rro_with_cip) * (float(self.rrocip_margin_for_expense_calculation)/100)
                    self.rrocip_overhead_cost =self.rrocip_margin_cost_for_expense_calculation * (float(self.rrocip_overhead)/100)
                    self.rrocip_e_c_cost=self.rrocip_margin_cost_for_expense_calculation * (float(self.rrocip_e_c)/100)
                    self.rrocip_agent_commission_cost=self.rrocip_margin_cost_for_expense_calculation * (float(self.rrocip_agent_commission)/100)
                    self.rrocip_guarantee_clause_cost=(self.rrocip_e_c_cost+self.rrocip_margin_cost_for_expense_calculation + self.rrocip_overhead_cost + self.rrocip_agent_commission_cost) * (float(self.rrocip_guarantee_clause_charge)/100)
                    self.rrocip_grand_total = (self.rro_with_cip+self.rrocip_e_c_cost + self.rrocip_overhead_cost + self.rrocip_agent_commission_cost + self.rrocip_guarantee_clause_cost)
                    self.rrocip_price = self.rrocip_grand_total * (float(self.rrocip_margin)/100)
                if(self.rewro_cost>0):
                    self.rew_ro_with_cip = self.rewro_cost+self.cip_cost3
                    self.rewrocip_margin_cost_for_expense_calculation = float(self.rew_ro_with_cip) * (float(self.rewrocip_margin_for_expense_calculation)/100)
                    self.rewrocip_overhead_cost =self.rewrocip_margin_cost_for_expense_calculation * (float(self.rewrocip_overhead)/100)
                    self.rewrocip_e_c_cost=self.rewrocip_margin_cost_for_expense_calculation * (float(self.rewrocip_e_c)/100)
                    self.rewrocip_agent_commission_cost=self.rewrocip_margin_cost_for_expense_calculation * (float(self.rewrocip_agent_commission)/100)
                    self.rewrocip_guarantee_clause_cost=(self.rewrocip_e_c_cost+self.rewrocip_margin_cost_for_expense_calculation + self.rewrocip_overhead_cost + self.rewrocip_agent_commission_cost) * (float(self.rewrocip_guarantee_clause_charge)/100)
                    self.rewrocip_grand_total = (self.rew_ro_with_cip+self.rewrocip_e_c_cost + self.rewrocip_overhead_cost + self.rewrocip_agent_commission_cost + self.rewrocip_guarantee_clause_cost)
                    self.rewrocip_price = self.rewrocip_grand_total * (float(self.rewrocip_margin)/100)
                
                
                self.standard_cost=[]
                self.brinex_table=[]
                self.rewolutte_table=[]
                bio_sys="No"
                bio_sys_ar=["Rotary Brush Screener", "Bar Screener", "Drum Screener", "Anaerobic Screener", "Anaerobic Equalization", "Anaerobic Neutralization", "Anaerobic System", "Ammonia Striper", "Lifting sump", "Oil & grease trap", "DAF (Dissolved Air Flotation)", "Equalization System", "Neutralization System","Cooling Tower","De-Nitrification System", "Distribution system", "Biological Oxidation System", "Clarifier Feed Tank", "Circular Clarifier System", "Lamella Settler", "DO increase system", "SRS System", "Sludge Thickener", "Sludge Thickener with mech", "Screw Press", "Belt Press"]
                for i in bio_sys_ar:
                    if(i in selected_s):
                        bio_sys="Yes"
                        break
                        
                if(bio_sys=="Yes"):
                    self.append("standard_cost",{
                        "system_name":"Pre Treatment",
                        "cost":self.bio_selling_price
                    })
                if("Micro Filtration - ASAHI" in selected_s):
                    self.append("standard_cost",{
                        "system_name":"MF",
                        "cost":self.mf_cost_with_margin
                    })
                if("Submerged MBR system - KOCH" in selected_s):
                    self.append("standard_cost",{
                        "system_name":"MBR(K)",
                        "cost":self.mbr_selling_price
                    })
                if("Submerged MBR system - OVIVO" in selected_s):
                    self.append("standard_cost",{
                        "system_name":"MBR(O)",
                        "cost":self.ovivo_selling_price
                    })
                if("Degasser System" in selected_s):
                    self.append("standard_cost",{
                        "system_name":"Degasser System",
                        "cost":self.dgt_selling_price
                    })
                if("Reverse Osmosis" in selected_s):
                    try:
                        self.append("standard_cost",{
                            "system_name":"RO",
                            "cost":self.rocip_price
                        })
                    except:pass
                
                
                if(self.is_rewolutte==1):
                    self.rewolutte_table=[]
                    self.append("rewolutte_table",{
                        "system_name":"REW RO",
                        "cost":self.rewrocip_price
                    })
                    if("Hardness and Silica Removal System" in selected_s):
                        self.append("rewolutte_table",{
                            "system_name":"Chemical Treatment System",
                            "cost":self.cts_selling_price
                        })
                    if("CTS MBR" in selected_s):
                        self.append("rewolutte_table",{
                            "system_name":"MBR CTS",
                            "cost":self.mbr_cts_selling_price
                        })
                    if("Chlorination system" in selected_s):
                        self.append("rewolutte_table",{
                            "system_name":"Chlorination",
                            "cost":self.clt_selling_price
                        })
                elif(self.is_brinex==1):
                    self.brinex_table=[]
                    if("Hardness and Silica Removal System" in selected_s):
                        self.append("brinex_table",{
                            "system_name":"Chemical Treatment System",
                            "cost":self.cts_selling_price
                        })
                    if("CTS MBR" in selected_s):
                        self.append("brinex_table",{
                            "system_name":"CTS MBR",
                            "cost":self.mbr_cts_selling_price
                        })
                    if("Chlorination system" in selected_s):
                        self.append("brinex_table",{
                            "system_name":"Chlorination",
                            "cost":self.clt_selling_price
                        })
                    self.append("brinex_table",{
                        "system_name":"RRO",
                        "cost":self.rrocip_price
                    })
                    if(self.cts_cooling_tower_cost>0):
                        self.append("brinex_table",{
                                "system_name":"CTS Cooling Tower",
                                "cost":self.cts_cooling_tower_selling_price
                            })
                else:
                    if("Chlorination system" in selected_s):
                        self.append("standard_cost",{
                            "system_name":"Chlorination",
                            "cost":self.clt_selling_price
                        })
                    if("CTS MBR" in selected_s):
                        self.append("standard_cost",{
                            "system_name":"CTS MBR",
                            "cost":self.mbr_cts_selling_price
                        })
                    if("Hardness and Silica Removal System" in selected_s):
                        if(self.cts_selling_price>0):
                            self.append("standard_cost",{
                                "system_name":"Chemical Treatment System",
                                "cost":self.cts_selling_price
                            })
                #plc splitup
                plc_item=["PLC CPU", "MONITOR", "MODEM", "ETHERNET SWITCH", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE"]
                ml_item=['PLCCBOIPC6015-0010W10IOTIA2NIL24VDCNIL4GBUPTO 4 GBNILIP 20NILNIL','MNTAM7"-15"24VDCS-SPMWTWDVIMBWBES-S','PCAMDMAM4GPMNILNILSIMLAN','PCAENSAM1GB/ SPMUMS3NILNIL','HDMI3MM-MDP-HDMIAMPLC-MONI','POWER ADAPTERREPUTED230 VAC24 VDC2A50HZMONISUP','TSUSBCREPUTEDUSB-AB3METERTSM']
                self.plc_table_list=[]
                for i in range(len(plc_item)):
                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(ml_item[i])+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                        self.append('plc_table_list',{
                            "item_description":plc_item[i],
                            "item_code":ml_item[i],
                            "w_qty":1,
                            "unit_price":g.base_rate,
                            "amount":g.base_rate
                        })
                plcsum=[]
                for j in self.plc_table_list:
                    if(j.amount!=None):
                        plcsum.append(j.amount)
                self.plc_base_total = sum(plcsum)
                self.plc_tax_cost = self.plc_base_total * (float(self.plc_tax)/100)
                self.plc_transport_cost = self.plc_base_total * (float(self.plc_transport)/100)
                self.plc_cost2 = (self.plc_base_total + self.plc_tax_cost + self.plc_transport_cost)
                self.total_cost_for_plc = (self.plc_base_total + self.plc_tax_cost + self.plc_transport_cost)
                if(self.plc_margin_for_expense_calculation is not None):
                    self.plc_margin_cost_for_expense_calculation = self.plc_cost2 * (float(self.plc_margin_for_expense_calculation)/100)
                self.plc_overhead_cost =self.plc_margin_cost_for_expense_calculation * (float(self.plc_overhead)/100)
                self.plc_e_c_cost=self.plc_margin_cost_for_expense_calculation * (float(self.plc_e_c)/100)
                self.plc_agent_commission_cost=self.plc_margin_cost_for_expense_calculation * (float(self.plc_agent_commission)/100)
                self.plc_guarantee_clause_cost=(self.plc_e_c_cost+self.plc_margin_cost_for_expense_calculation + self.plc_overhead_cost + self.plc_agent_commission_cost) * (float(self.plc_guarantee_clause_charge)/100)
                self.plc_grand_total = (self.plc_cost2+self.plc_e_c_cost + self.plc_overhead_cost + self.plc_agent_commission_cost + self.plc_guarantee_clause_cost)
                self.plc_cost = self.plc_grand_total * (float(self.plc_margin)/100)
                #plc splitup
                plcount=0
                for i in self.standard_cost:
                    if(i.system_name=="Degasser System"):
                        pass
                    else:
                        plcount=plcount+1
                for i in self.brinex_table:
                    if(i.system_name == "Chemical Treatment System"):
                        pass
                    else:
                        plcount=plcount+1
                for i in self.rewolutte_table:
                    plcount=plcount+1
                splitamount = self.plc_cost/plcount if plcount!=0 else 0
                for i in self.standard_cost:
                    if(i.system_name=="Degasser System"):
                        i.plc_split_cost = 0
                        i.total_cost = i.cost
                        i.total_price_eur = float(i.total_cost)/(self.eur-2)
                        i.total_price_usd = float(i.total_cost)/(self.usd-2)
                    else:
                        i.plc_split_cost = splitamount;
                        i.total_cost = i.plc_split_cost + i.cost
                        i.total_price_eur = float(i.total_cost)/(self.eur-2)
                        i.total_price_usd = float(i.total_cost)/(self.usd-2)
                for i in self.brinex_table:
                    if(i.system_name == "Chemical Treatment System"):
                        i.plc_split_cost = 0
                        i.total_cost = i.cost
                        i.total_price_eur = float(i.total_cost)/(self.eur-2)
                        i.total_price_usd = float(i.total_cost)/(self.usd-2)
                    else:
                        i.plc_split_cost = splitamount;
                        i.total_cost = i.plc_split_cost + i.cost
                        i.total_price_eur = float(i.total_cost)/(self.eur-2)
                        i.total_price_usd = float(i.total_cost)/(self.usd-2)
                for i in self.rewolutte_table:
                    i.plc_split_cost = splitamount;
                    i.total_cost = i.plc_split_cost + i.cost
                    i.total_price_eur = float(i.total_cost)/(self.eur-2)
                    i.total_price_usd = float(i.total_cost)/(self.usd-2)
                    
                ##margin split up in bio full system
                if(len(self.pre_treatment_full_system)>0):
                    plc=[]
                    for i in self.bio_plc_items:
                        plc.append(i.total_price)
                    total_system=[]
                    for i in self.pre_treatment_full_system:
                        total_system.append(i.item_description)
                
                    splitamount_1=splitamount/len(total_system)
                    m1=float(self.bio_tax)+float(self.bio_transport)
                    m2=float(self.bio_margin_for_expense_calculation)
                    m3=float(self.bio_e_c_)+float(self.bio_overhead_percentage)+float(self.bio_agent_commission)
                    m4=float(self.bio_guarantee_clause_charge)
                    m5=float(self.bio_margin_percentage)
                    for i in self.pre_treatment_full_system:
                        electrical_cost=[0]
                        for j in self.bio_electrical_items:
                            if(i.item_description==j.system):
                                electrical_cost.append(j.total_price)
                        base_total = i.total_price_with_erefab+sum(electrical_cost)+(sum(plc)/len(total_system))
                        cost = base_total+(base_total*m1/100)
                        cost1 = cost*m2/100
                        cost2 = cost1*m3/100
                        cost3 = (cost1+cost2)*m4/100
                        tot_cost = (cost+cost2+cost3)*m5/100
                        i.selling_price = tot_cost+splitamount_1
                    # frappe.msgprint(str(check))
                cost_ar=[]
                cost_ar2=[]
                cost_ar3=[]
                for i in self.standard_cost:
                    cost_ar.append(i.total_cost)
                for i in self.brinex_table:
                    cost_ar2.append(i.total_cost)
                for i in self.rewolutte_table:
                    cost_ar3.append(i.total_cost)
                
                self.standard__cost=sum(cost_ar)
                self.brinex_cost=sum(cost_ar2)
                self.rewolutte_cost=sum(cost_ar3)
                for i in self.standard_cost:
                    if(i.system_name=="RO" and self.is_rewolutte==1):
                        self.rewolutte_cost=sum(cost_ar3)-i.total_cost
                self.overall_cost = self.standard__cost+self.brinex_cost+self.rewolutte_cost
                ro_temp = "No RO"
                if(self.choose_ro_template!=None and self.choose_ro_template!=''):
                    ro_temp = self.choose_ro_template
                elif(self.rewolutte_ro!=None and self.rewolutte_ro!=''):
                    ro_temp = self.rewolutte_ro
                elif(self.choose_rro_template!=None and self.choose_rro_template!=''):
                    ro_temp = self.choose_rro_template
                
                if (ro_temp!="No RO"):
                    self.ssb_pressure_pump_cost = frappe.db.sql("SELECT ssb_pump_cost from `tabRO Standard Items` where name='"+str(ro_temp)+"' ",as_dict=1)[0].ssb_pump_cost
                else:
                    self.ssb_pressure_pump_cost = 0
                ##euro
                self.standard__cost2 = self.standard__cost/(self.eur-2)
                self.brinex_cost2 = self.brinex_cost/(self.eur-2)
                self.rewolutte_cost2 = self.rewolutte_cost/(self.eur-2)
                self.overall_cost2   = self.overall_cost/(self.eur-2)
                self.ssb_pressure_pump_cost2 = self.ssb_pressure_pump_cost/(self.eur-2)

                # ##usd
                self.standard__cost3 = self.standard__cost/(self.usd-2)
                self.brinex_cost3 = self.brinex_cost/(self.usd-2)
                self.rewolutte_cost3 = self.rewolutte_cost/(self.usd-2)
                self.overall_cost3   = self.overall_cost/(self.usd-2)
                self.ssb_pressure_pump_cost3 = self.ssb_pressure_pump_cost/(self.usd-2)
                for j in self.standard_cost:
                    j.usd="USD"
                    j.eur="EUR"
                for j in self.brinex_table:
                    j.usd="USD"
                    j.eur="EUR"
                for j in self.rewolutte_table:
                    j.usd="USD"
                    j.eur="EUR"
                self.scheme_splitup(selected_s,splitamount)
                self.anaero(selected_s)

        except Exception as e:
            error_message = f"An error occurred: {str(e)} (Line {traceback.extract_tb(e.__traceback__)[0].lineno})"
            frappe.throw(str(error_message))
    
    def anaero(self,selected_s):
        if "Anaerobic Screener" in selected_s:
            for i in self.anaerobic_items:
                if(i.item_description == 'SCREENER'):
                    i.flow = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow")
                    i.w_qty = 1
        if "Anaerobic Bar Screener" in selected_s:
            for i in self.anaerobic_items:
                if(i.item_description == "BAR SCREENER"):
                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='PSISOSS3161590MM796MM2MM' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                        i.w_qty = 1
                        i.unit_price = g.base_rate
                        i.total_price = g.base_rate * 1
        if "Anaerobic Lifting Pump" in selected_s:
            for i in self.anaerobic_items:
                if(i.item_description == "LIFTING PUMP"):
                    i.w_qty = 1
                    i.sb_qty = 1
                    pv_flow = (frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow")*1.5)/24
                    i.flow = int(-1 * pv_flow // 1 * -1)
                    if(("Anaerobic Ammonia Striper" in selected_s) or ("Anaerobic Cooling Tower" in selected_s)):
                        i.range =  (frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_anaerobic_feed_tank_height")/10) +0.6
                    else:
                        i.range =  (frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_anaerobic_feed_tank_height")/10) +0.1

                elif(i.item_description == "LPS LEVEL FLOAT"):
                    i.w_qty = 2
                    i.flow = 1

                elif(i.item_description == "LPS PIPES"):
                    pv_flow = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow")/24
                    pv_ceil = int(-1 * pv_flow // 1 * -1)
                    qqty=0
                    a_f = pv_ceil/24
                    m_v = 2.5
                    f0 = 3600
                    f2=(((4*a_f)/(m_v*f0*3.14))**(1/2))*1000
                    i.flow = pv_ceil
                    if(("Anaerobic Ammonia Striper" in selected_s) or ("Anaerobic Cooling Tower" in selected_s)):
                        f2=f2*1.2
                        lam_tank = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_lamella_tank_height")
                        qqty=(lam_tank+0.5+0.5)*2
                    else:
                        f2=f2*1.5
                        lam_tank = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_lamella_tank_height")
                        qqty=(lam_tank+0.5)*2
                    if(f2>0 and f2<6.99):ff="DN6"
                    elif(f2>6.99 and f2<10.42):ff="DN8"
                    elif(f2>10.42 and f2<13.85):ff="DN10"
                    elif(f2>13.85 and f2<18.04):ff="DN15"   
                    elif(f2>18.04 and f2<23.37):ff="DN20"
                    elif(f2>23.37 and f2<30.1):ff="DN25"
                    elif(f2>30.1 and f2<38.86):ff="DN32"
                    elif(f2>38.86 and f2<44.96):ff="DN40"
                    elif(f2>44.96 and f2<57.08):ff="DN50"
                    elif(f2>57.08 and f2<68.81):ff="DN65"
                    elif(f2>68.81 and f2<84.68):ff="DN80"
                    elif(f2>84.68 and f2<110.08):ff="DN100"
                    elif(f2>110.08 and f2<135.76):ff="DN125"
                    elif(f2>135.76 and f2<162.72):ff="DN150"
                    elif(f2>162.72 and f2<213.54):ff="DN200"
                    elif(f2>213.54 and f2<266.25):ff="DN250"
                    elif(f2>266.25 and f2<315.93):ff="DN300"
                    elif(f2>315.93 and f2<347.68):ff="DN350"
                    elif(f2>347.68 and f2<398.02):ff="DN400"
                    elif(f2>398.02 and f2<448.62):ff="DN450"
                    elif(f2>448.62 and f2<498.44):ff="DN500"
                    elif(f2>498.44 and f2<549.44):ff="DN550"
                    elif(f2>549.44 and f2<598.92):ff="DN600"
                    elif(f2>598.92 and f2<749.3):ff="DN750"
                    i.range=ff
                    i.w_qty=qqty
        if "Anaerobic Neutralization" in selected_s:
            if "Anaerobic Settler" in selected_s:
                for i in self.anaerobic_items:
                    if(i.item_description == "FEED PUMP"):
                        pv_flow = (frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow")*1.5)/24
                        pv_ceil = int(-1 * pv_flow // 1 * -1)
                        pv_range = ((frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_anaerobic_feed_tank_height"))/10) + 0.1
                        pv_range_ceil = int(-1 * pv_range // 1 * -1)
                        i.flow = pv_ceil
                        i.w_qty = 1
                        i.sb_qty = 1
                        i.range = pv_range_ceil
            else:
                for i in self.anaerobic_items:
                    if(i.item_description == "FEED PUMP"):
                        pv_flow = (frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow")*1.5)/24
                        pv_ceil = int(-1 * pv_flow // 1 * -1)
                        pv_range = ((frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_lamella_tank_height"))/10) + 0.1
                        pv_range_ceil = int(-1 * pv_range // 1 * -1)
                        i.flow = pv_ceil
                        i.w_qty = 1
                        i.sb_qty = 1
                        i.range = pv_range_ceil

            for i in self.anaerobic_items:
                if(i.item_description == "NT EMFM"):
                    pv_flow = (frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow"))/24
                    pv_ceil = int(-1 * pv_flow // 1 * -1)
                    i.w_qty = 1
                    i.flow = pv_ceil
                elif(i.item_description == "NT DOSING PUMP"):
                    pv_flow = ((frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow"))/1000) * 30
                    pv_ceil = int(-1 * pv_flow // 1 * -1)
                    i.w_qty = 1
                    i.sb_qty = 1
                    i.flow = pv_ceil
                elif(i.item_description == "NT. DOSING PUMP FRAME"):
                    i.w_qty = 2
                    i.flow = 1
                elif(i.item_description == "NT PH SENSOR"):
                    i.w_qty = 1
                elif(i.item_description == "NT PIPES"):
                    pv_flow = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow")/24
                    pv_ceil = int(-1 * pv_flow // 1 * -1)
                    qqty=0
                    a_f = pv_ceil/24
                    m_v = 2.5
                    f0 = 3600
                    f2=(((4*a_f)/(m_v*f0*3.14))**(1/2))*1000
                    i.flow = pv_ceil
                    if(("Anaerobic Ammonia Striper" in selected_s) or ("Anaerobic Cooling Tower" in selected_s)):
                        f2=f2*1.2
                        if("Anaerobic CTS" in selected_s):
                            lam_tank = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_lamella_tank_height")
                            qqty=(lam_tank+0.5+0.5)*2
                        elif("Anaerobic Settler" in selected_s):
                            lam_tank = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_anaerobic_feed_tank_height")
                            qqty=(lam_tank+0.5+0.5)*2
                    else:
                        f2=f2*1.5
                        if("Anaerobic CTS" in selected_s):
                            lam_tank = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_lamella_tank_height")
                            qqty=(lam_tank+0.5+0.5)*2
                        elif("Anaerobic Settler" in selected_s):
                            lam_tank = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_anaerobic_feed_tank_height")
                            qqty=(lam_tank+0.5+0.5)*2
                    if(f2>0 and f2<6.99):ff="DN6"
                    elif(f2>6.99 and f2<10.42):ff="DN8"
                    elif(f2>10.42 and f2<13.85):ff="DN10"
                    elif(f2>13.85 and f2<18.04):ff="DN15"   
                    elif(f2>18.04 and f2<23.37):ff="DN20"
                    elif(f2>23.37 and f2<30.1):ff="DN25"
                    elif(f2>30.1 and f2<38.86):ff="DN32"
                    elif(f2>38.86 and f2<44.96):ff="DN40"
                    elif(f2>44.96 and f2<57.08):ff="DN50"
                    elif(f2>57.08 and f2<68.81):ff="DN65"
                    elif(f2>68.81 and f2<84.68):ff="DN80"
                    elif(f2>84.68 and f2<110.08):ff="DN100"
                    elif(f2>110.08 and f2<135.76):ff="DN125"
                    elif(f2>135.76 and f2<162.72):ff="DN150"
                    elif(f2>162.72 and f2<213.54):ff="DN200"
                    elif(f2>213.54 and f2<266.25):ff="DN250"
                    elif(f2>266.25 and f2<315.93):ff="DN300"
                    elif(f2>315.93 and f2<347.68):ff="DN350"
                    elif(f2>347.68 and f2<398.02):ff="DN400"
                    elif(f2>398.02 and f2<448.62):ff="DN450"
                    elif(f2>448.62 and f2<498.44):ff="DN500"
                    elif(f2>498.44 and f2<549.44):ff="DN550"
                    elif(f2>549.44 and f2<598.92):ff="DN600"
                    elif(f2>598.92 and f2<749.3):ff="DN750"
                    i.range=ff
                    i.w_qty=qqty
                elif(i.item_description == "NT LEVEL TRANSMITTER"):
                    pv_range = ((frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_lamella_tank_height"))) + 1
                    pv_range_ceil = int(-1 * pv_range // 1 * -1)
                    i.w_qty = 1
                    i.range = pv_range_ceil
                elif(i.item_description == "NT LEVEL FLOAT"):
                    i.w_qty = 2

        if "Anaerobic Settler" in selected_s:
            for i in self.anaerobic_items:
                if(i.item_description == "AN. SLUDGE PUMP"):
                    pv_flow = (frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow"))/24
                    pv_ceil = int(-1 * pv_flow // 1 * -1)
                    i.flow = pv_ceil
                    i.w_qty = 1
                    i.sb_qty = 1
                    i.range = 1
                elif(i.item_description == "AN. SRS PUMP"):
                    pv_flow = (frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow"))/24
                    pv_ceil = int(-1 * pv_flow // 1 * -1)

                    pv_range = ((frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_anaerobic_feed_tank_height"))/10) + 0.5
                    pv_range_ceil = int(-1 * pv_range // 1 * -1)

                    i.flow = pv_ceil
                    i.w_qty = 1
                    i.sb_qty = 1
                    i.range = pv_range
                elif(i.item_description == "AN. SRS EMFM"):
                    pv_flow = (frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow"))/24
                    pv_ceil = int(-1 * pv_flow // 1 * -1)

                    pv_range = ((frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_anaerobic_feed_tank_height"))/10) + 0.5
                    pv_range_ceil = int(-1 * pv_range // 1 * -1)

                    i.flow = pv_ceil
                    i.w_qty = 1

                elif(i.item_description == "AN. SRS LEVEL FLOAT"):
                    w_q = ((frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_anaerobic_feed_tank_height"))/3)
                    i.flow = 1
                    i.w_qty = w_q

                elif(i.item_description == "AN. SRS LEVEL TRANSMITTER"):
                    pv_range = ((frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_anaerobic_feed_tank_height")))
                    pv_range_ceil = int(-1 * pv_range // 1 * -1)
                    i.flow = 1
                    i.w_qty = 0
                    i.range = pv_range

        if "Anaerobic Lamella Settler" in selected_s:
            for i in self.anaerobic_items:
                if(i.item_description == "LAMELLA SETTLER"):
                    tank_he = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_lamella_tank_height")
                    pv_flow = (frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow"))/24 * 4
                    lamella= (pv_flow)/(tank_he-2)
                    i.flow = round(lamella,2)
                    i.w_qty= 1
                    i.unit_price = 7600 * lamella
                    i.total_price = 7600 * lamella
                    i.pipes_per=0
                elif(i.item_description == "LAM. SLUDGE PUMP"):
                    pv_flow = (frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow"))/24
                    i.flow = int(-1 * pv_flow // 1 * -1)
                    i.range = 1.5
                    i.w_qty = 1
                    i.sb_qty = 1
                elif(i.item_description == "LAM. SLUDGE PUMP PIPES"):
                    pv_flow = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow")/24
                    pv_ceil = int(-1 * pv_flow // 1 * -1)
                    pv_tank_height = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_lamella_tank_height")
                    qqty = pv_tank_height + 20
                    a_f = pv_ceil/24
                    m_v = 2
                    f0 = 3600
                    f2=(((4*a_f)/(m_v*f0*3.14))**(1/2))*1000
                    i.flow = pv_ceil
                    if(f2>0 and f2<6.99):ff="DN6"
                    elif(f2>6.99 and f2<10.42):ff="DN8"
                    elif(f2>10.42 and f2<13.85):ff="DN10"
                    elif(f2>13.85 and f2<18.04):ff="DN15"   
                    elif(f2>18.04 and f2<23.37):ff="DN20"
                    elif(f2>23.37 and f2<30.1):ff="DN25"
                    elif(f2>30.1 and f2<38.86):ff="DN32"
                    elif(f2>38.86 and f2<44.96):ff="DN40"
                    elif(f2>44.96 and f2<57.08):ff="DN50"
                    elif(f2>57.08 and f2<68.81):ff="DN65"
                    elif(f2>68.81 and f2<84.68):ff="DN80"
                    elif(f2>84.68 and f2<110.08):ff="DN100"
                    elif(f2>110.08 and f2<135.76):ff="DN125"
                    elif(f2>135.76 and f2<162.72):ff="DN150"
                    elif(f2>162.72 and f2<213.54):ff="DN200"
                    elif(f2>213.54 and f2<266.25):ff="DN250"
                    elif(f2>266.25 and f2<315.93):ff="DN300"
                    elif(f2>315.93 and f2<347.68):ff="DN350"
                    elif(f2>347.68 and f2<398.02):ff="DN400"
                    elif(f2>398.02 and f2<448.62):ff="DN450"
                    elif(f2>448.62 and f2<498.44):ff="DN500"
                    elif(f2>498.44 and f2<549.44):ff="DN550"
                    elif(f2>549.44 and f2<598.92):ff="DN600"
                    elif(f2>598.92 and f2<749.3):ff="DN750"
                    i.range=ff
                    i.w_qty=qqty
                elif(i.item_description == "LAM. SLUDGE PUMP LEVEL FLOAT"):
                    i.w_qty = 2
                elif(i.item_description == "LAM. DOSING PUMP-1" or i.item_description == "LAM. DOSING PUMP-2" or i.item_description == "LAM. DOSING PUMP-3"):
                    pv_flow = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow")/100
                    pv_ceil = int(-1 * pv_flow // 1 * -1) * 50
                    i.flow = pv_ceil
                    i.w_qty = 1
                    i.ssb_qty = 1
                elif(i.item_description == "LAM. DOSING PUMP-1 FRAME" or i.item_description == "LAM. DOSING PUMP-2 FRAME" or i.item_description == "LAM. DOSING PUMP-3 FRAME"):
                    pv_flow = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow")/100
                    pv_ceil = int(-1 * pv_flow // 1 * -1) * 50
                    i.flow = pv_ceil
                    cipf=[]
                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='LANISOSS30440X403MM' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                        if(g.base_rate>0):
                            cipf.append(g.base_rate)
                    i.w_qty = 1
                    i.unit_price = cipf[0]
                    i.total_price = cipf[0]
        if "Anaerobic CTS" in selected_s:
            for i in self.anaerobic_items:
                if(i.item_description == "LAM. STATIC MIXER - PVDF"):
                    i.w_qty = 1
                elif(i.item_description == "LAM. STATIC MIXER - SS316"):
                    i.w_qty = 2
                elif(i.item_description == "CTS. FEED PUMP"):
                    pv_flow = (frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow"))/24
                    i.flow = int(-1 * pv_flow // 1 * -1)
                    i.range = 1.5
                    i.w_qty = 1
                    i.sb_qty = 1
                elif(i.item_description == "CTS. SLUDGE PUMP"):
                    pv_flow = ((frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow"))/24) * 0.3
                    i.flow = int(-1 * pv_flow // 1 * -1)
                    i.range = 1.5
                    i.w_qty = 1
                    i.sb_qty = 1
                elif(i.item_description == "CTS. EMFM"):
                    pv_flow = (frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow"))/24
                    i.flow = int(-1 * pv_flow // 1 * -1)
                    i.w_qty = 1
                elif(i.item_description == "CTS. AGITATOR"):
                    i.w_qty=2
                elif(i.item_description == "CTS. PH SENSOR"):
                    i.w_qty=1
                elif(i.item_description == "CTS. LEVEL FLOAT"):
                    i.w_qty=2
                elif(i.item_description == "CTS. PIPE FLOCCULATION"):
                    pv_flow = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow")
                    flow = pv_flow/1000
                    fl=0
                    fl_ce=0
                    if(flow>0 and flow<=0.1):fl=0.1
                    elif(flow>0.1 and flow<=0.25):fl=0.25
                    elif(flow>0.25 and flow<=0.5):fl=0.5
                    elif(flow>0.5 and flow<=0.75):fl=0.75
                    elif(flow>0.75 and flow<=1):fl=1
                    elif(flow>1):
                        fl_ce = int(-1 * flow // 1 * -1)
                    if(fl_ce>1):
                        i.w_qty=fl_ce
                    else:
                        i.w_qty=1
                    price_ar=[]
                    for item in frappe.db.sql("SELECT item_code,qty FROM `tabProcess BOM Template Items` where parent='FLOCCULATION"+str(fl)+"' ",as_dict=1):
                        for rate in frappe.db.sql("SELECT (`tabPurchase Order Item`.`base_rate`*"+str(item.qty)+")as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(item.item_code)+"' and `tabPurchase Order`.`naming_series`!='JOB-.YY.-' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                            price_ar.append(rate.base_rate)
                    i.unit_price=sum(price_ar)
                    i.total_price=sum(price_ar)
                elif(i.item_description == "CTS. DOSING PUMP-1" or i.item_description == "CTS. DOSING PUMP-2" or i.item_description == "CTS. DOSING PUMP-3" or i.item_description == "CTS. DOSING PUMP-4" or i.item_description == "CTS. DOSING PUMP-5"):
                    pv_flow = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow")/100
                    pv_ceil = int(-1 * pv_flow // 1 * -1) * 50
                    i.flow = pv_ceil
                    i.w_qty = 1
                    i.ssb_qty = 1
                elif(i.item_description == "CTS. DOSING PUMP-1 FRAME" or i.item_description == "CTS. DOSING PUMP-2 FRAME" or i.item_description == "CTS. DOSING PUMP-3 FRAME" or i.item_description == "CTS. DOSING PUMP-4 FRAME" or i.item_description == "CTS. DOSING PUMP-5 FRAME"):
                    pv_flow = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"pva_stream_flow")/100
                    pv_ceil = int(-1 * pv_flow // 1 * -1) * 50
                    i.flow = pv_ceil
                    cipf=[]
                    for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='LANISOSS30440X403MM' ORDER BY `tabPurchase Order`.`creation` DESC",as_dict=1):
                        if(g.base_rate>0):
                            cipf.append(g.base_rate)
                    i.w_qty = 1
                    i.unit_price = cipf[0]
                    i.total_price = cipf[0]


    def scheme_splitup(self,selected_s,splitamount):
        lamella_cost=0
        clarifier_cost=0
        main_scheme = ''
        if(frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mf")==1):
            main_scheme = 'MF'
        elif(frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbr_k")==1):
            main_scheme = "MBR (K)"
        elif(frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"mbr_o")==1):
            main_scheme = "MBR (O)"
        if(len(self.pre_treatment_special_table)>0):
            plc=[]
            for i in self.bio_plc_items:
                plc.append(i.total_price)
            total_system=[]
            for i in self.pre_treatment_full_system:
                total_system.append(i.item_description)
        
            splitamount_1=splitamount/len(total_system)
            m1=float(self.bio_tax)+float(self.bio_transport)
            m2=float(self.bio_margin_for_expense_calculation)
            m3=float(self.bio_e_c_)+float(self.bio_overhead_percentage)+float(self.bio_agent_commission)
            m4=float(self.bio_guarantee_clause_charge)
            m5=float(self.bio_margin_percentage)
            for i in self.pre_treatment_special_table:
                electrical_cost=[0]
                for j in self.bio_electrical_items:
                    if(i.item_description==j.system):
                        electrical_cost.append(j.total_price)
                base_total = i.total_price_with_erefab+sum(electrical_cost)+(sum(plc)/len(total_system))
                cost = base_total+(base_total*m1/100)
                cost1 = cost*m2/100
                cost2 = cost1*m3/100
                cost3 = (cost1+cost2)*m4/100
                tot_cost = (cost+cost2+cost3)*m5/100
                i.selling_price = tot_cost+splitamount_1
        for i in self.pre_treatment_special_table:
            if(i.item_description=="Lamella Settler"):
                lamella_cost = float(i.selling_price)
            elif(i.item_description=="Circular Clarifier System"):
                clarifier_cost = float(i.selling_price)

        if("Lamella Settler" in selected_s and "Circular Clarifier System" in selected_s):
            self.mf_scheme = (self.bio_selling_price+splitamount) - lamella_cost
            self.koch_scheme = (self.bio_selling_price+splitamount) - clarifier_cost
            self.ovivo_scheme = (self.bio_selling_price+splitamount) - clarifier_cost
        elif("Lamella Settler" in selected_s):
            self.mf_scheme = (self.bio_selling_price+splitamount) + clarifier_cost - lamella_cost
            self.koch_scheme = (self.bio_selling_price+splitamount)
            self.ovivo_scheme = (self.bio_selling_price+splitamount)
        elif("Circular Clarifier System" in selected_s):
            self.mf_scheme = (self.bio_selling_price+splitamount)
            self.koch_scheme = (self.bio_selling_price+splitamount) - clarifier_cost + lamella_cost
            self.ovivo_scheme = (self.bio_selling_price+splitamount) - clarifier_cost + lamella_cost
        else:
            self.mf_scheme = (self.bio_selling_price+splitamount) + lamella_cost
            self.koch_scheme = (self.bio_selling_price+splitamount) + clarifier_cost
            self.ovivo_scheme = (self.bio_selling_price+splitamount) + clarifier_cost
        plc_split=0
        # for jj in self.standard_cost:
        #     if(jj.system_name=="Pre Treatment"):
        #         plc_split=plc_split+jj.plc_split_cost
        # aa=(self.mf_scheme + self.bio_electrical_cost)*(1+((self.bio_tax+self.bio_transport)/100))
        # aa1=aa*(self.bio_margin_for_expense_calculation/100)
        # aa2=aa1*(self.bio_e_c_/100)
        # aa3=aa1*(self.bio_overhead_percentage/100)
        # aa4=aa1*(self.bio_agent_commission/100)
        # aa5=(aa1+aa2+aa3+aa4)*(self.bio_guarantee_clause_charge/100)
        # final_aa=aa+aa2+aa3+aa4+aa5
        # self.mf_scheme = (final_aa*(self.bio_margin_percentage/100))+plc_split

        # aa=(self.koch_scheme + self.bio_electrical_cost)*(1+((self.bio_tax+self.bio_transport)/100))
        # aa1=aa*(self.bio_margin_for_expense_calculation/100)
        # aa2=aa1*(self.bio_e_c_/100)
        # aa3=aa1*(self.bio_overhead_percentage/100)
        # aa4=aa1*(self.bio_agent_commission/100)
        # aa5=(aa1+aa2+aa3+aa4)*(self.bio_guarantee_clause_charge/100)
        # final_aa=aa+aa2+aa3+aa4+aa5
        # self.koch_scheme = (final_aa*(self.bio_margin_percentage/100))+plc_split

        # aa=(self.ovivo_scheme + self.bio_electrical_cost)*(1+((self.bio_tax+self.bio_transport)/100))
        # aa1=aa*(self.bio_margin_for_expense_calculation/100)
        # aa2=aa1*(self.bio_e_c_/100)
        # aa3=aa1*(self.bio_overhead_percentage/100)
        # aa4=aa1*(self.bio_agent_commission/100)
        # aa5=(aa1+aa2+aa3+aa4)*(self.bio_guarantee_clause_charge/100)
        # final_aa=aa+aa2+aa3+aa4+aa5
        # self.ovivo_scheme = (final_aa*(self.bio_margin_percentage/100))+plc_split
        plc_split=0
        sys=[]
        for jj in self.standard_cost:
            sys.append(jj.system_name)
            if(jj.system_name in ["MF","MBR(O)","MBR(K)"]):
                plc_split=plc_split+jj.plc_split_cost
                break
        self.reference_standard_cost=[]
        if("MF" not in sys):
            self.append("reference_standard_cost",{
                "system_name":"MF",
                "cost":self.mf_cost_with_margin,
                "plc_split_cost":plc_split,
                "eur":"EUR",
                "usd":"USD",
                "total_cost":self.mf_cost_with_margin+plc_split,
                "total_cost_usd":(self.mf_cost_with_margin+plc_split)/self.usd,
                "total_cost_eur":(self.mf_cost_with_margin+plc_split)/self.eur
            })
        if("MBR(K)" not in sys):
            self.append("reference_standard_cost",{
                "system_name":"MBR(K)",
                "cost":self.mbr_selling_price,
                "plc_split_cost":plc_split,
                "eur":"EUR",
                "usd":"USD",
                "total_cost":self.mbr_selling_price+plc_split,
                "total_cost_usd":(self.mbr_selling_price+plc_split)/self.usd,
                "total_cost_eur":(self.mbr_selling_price+plc_split)/self.eur
            })
        if("MBR(O)" not in sys):
            self.append("reference_standard_cost",{
                "system_name":"MBR(O)",
                "cost":self.ovivo_selling_price,
                "plc_split_cost":plc_split,
                "eur":"EUR",
                "usd":"USD",
                "total_cost":self.ovivo_selling_price+plc_split,
                "total_cost_usd":(self.ovivo_selling_price+plc_split)/self.usd,
                "total_cost_eur":(self.ovivo_selling_price+plc_split)/self.eur
            })

        if(main_scheme=="MF"):
            self.mf_scheme=0
        elif(main_scheme=="MBR (K)"):
            self.koch_scheme=0
        elif(main_scheme=="MBR (O)"):
            self.ovivo_scheme=0

    def on_trash(self):
        doc = frappe.get_doc("Startup Sheet", self.project_startup_sheet)
        doc.cost_working_data="Deleted"
        doc.save()
    @frappe.whitelist()
    def lamella_clarifier(self):
        try:
            ar=["Lamella Settler","Circular Clarifier System"]
            arr=[]
            for system in ar:
                if(str(system)=="Lamella Settler"):
                    tank_he = frappe.db.get_value("Startup Sheet",str(self.project_startup_sheet),"tank_height")
                    lamella= ((self.flow/24)*4)/(tank_he-2)
                    price = 7600 * lamella
                    arr.append({"system":"Lamella Settler","price":price})
                elif(str(system)=="Circular Clarifier System"):
                    dd=frappe.db.get_value("Startup Sheet",self.project_startup_sheet,'clarifier_diameter')
                    parameter="DIAMETER"
                    value=int(dd)
                    rate_from_bom=[]
                    mapping_bom=frappe.db.sql("""SELECT distinct(`tabMapping BOM`.`name`)as 'name'
                        FROM `tabMapping BOM` INNER JOIN `tabProcess System Parameter Threshold` 
                        ON `tabMapping BOM`.`name`=`tabProcess System Parameter Threshold`.`parent` 
                        WHERE `tabMapping BOM`.`process_system`='Circular Clarifier System' and 
                        `tabProcess System Parameter Threshold`.`value`='"""+str(value)+"""' """,as_dict=1)
                    if(mapping_bom):
                        for bb in frappe.db.sql("SELECT distinct(name),item_code,parent,stock_qty,stock_uom,total_weight,weight_per_unit,qty from `tabBOM Item` where parent='"+str(mapping_bom[0].name)+"' ",as_dict=1):
                            if(str(bb.item_code)[slice(3)]!="S60"):
                                for rate in frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,`tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(bb.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
                                    rate_from_bom.append(rate.base_rate*bb.stock_qty)
                            else:
                                if(bb.total_weight>0):
                                    rate_from_bom.append(480*bb.total_weight)
                                else:
                                    rate_from_bom.append(480*bb.weight_per_unit*bb.qty)
                    mar=1.05
                    price=round(sum(rate_from_bom)*mar,2)
                    arr.append({"system":"Circular Clarifier System","price":price})
            return arr
        except Exception as e:
            error_message = f"An error occurred: {str(e)} (Line {traceback.extract_tb(e.__traceback__)[0].lineno})"
            frappe.throw(str(error_message))
    

    @frappe.whitelist()
    def edit_pdf(self):
        att=self.attach
        file = frappe.get_doc("File", {'file_url':str(att)})
        file_path = file.get_full_path()
        doc = dd(file_path)
        ar=[]
        pc=0
        rc=0
        for p in doc.paragraphs:
            if 'pageno_index' in p.text:
                for i in p.runs:
                    if(i.text=='pageno_index'):
                        i.text="done"
        temp_pdf_file_path = "./erp.wttindia.com/public/files/temp.pdf"
        pdf_file_path="./erp.wttindia.com/public/files/Proposal1cb11d.pdf"
        doc.save(temp_pdf_file_path)
        subprocess.run(['unoconv', '-f', 'pdf', '-o', pdf_file_path, temp_pdf_file_path])

        self.proposal_no=pc
        self.attach2="/files/Proposal1cb11d.pdf"

@frappe.whitelist()
def get_matching_bom(arr):
    ar=[]
    data=[]
    to_python = json.loads(arr)
    for i in to_python:
        for j in frappe.db.sql("SELECT `tabMapping BOM`.`name`,`tabProcess System Parameter Threshold`.`value` as val FROM `tabMapping BOM` INNER JOIN `tabProcess System Parameter Threshold` ON `tabMapping BOM`.`name`=`tabProcess System Parameter Threshold`.`parent` WHERE `tabMapping BOM`.`process_system`='"+str(i['system_name'])+"'",as_dict=1):
            if(j.val == str(i['value'])):
                ar.append(j.name)
    final = set(ar)
    
    arr=[]
    for k in final:
        for g in frappe.db.sql("SELECT name,total_cost FROM `tabBOM` WHERE name='"+str(k)+"'",as_dict=1):
            arr.append({
                "name":g.name,
                "cost":g.total_cost
                })

    return arr
    
@frappe.whitelist()
def get_values(startup_sheet,ro=None,rro=None):
    ar=[]
    ar1=[]
    ar2=[]
    for i in frappe.db.sql("SELECT * from `tabStartup Sheet` where name='"+str(startup_sheet)+"' ",as_dict=1):
        ar.append(i)
    if(ro!=None):
        query = frappe.db.sql("""SELECT a.flow,a.ro_type,a.tds,a.theoretical_ro_recovery1,a.ro_recovery,
            a.ro_membrane_1,a.ro_membrane_2,a.ro_membrane_3,a.ro_membrane_4,a.ro_membrane_5,b.item_description,b.renamed,
            b.flow,b.range,b.model_no,b.w_qty,b.sb_qty,b.ssb_qty
             from `tabRO Standard Items` as a,`tabRO Items`as b where a.name=b.parent and a.name='"""+str(ro)+"""' """,as_dict=1)
        for i in query:
            ar1.append(i)
    if(rro!=None):
        query = frappe.db.sql("""SELECT a.flow,a.ro_type,a.tds,a.theoretical_ro_recovery1,a.ro_recovery,
            a.ro_membrane_1,a.ro_membrane_2,a.ro_membrane_3,a.ro_membrane_4,a.ro_membrane_5,b.item_description,b.renamed,
            b.flow,b.range,b.model_no,b.w_qty,b.sb_qty,b.ssb_qty
             from `tabRO Standard Items` as a,`tabRO Items`as b where a.name=b.parent and a.name='"""+str(rro)+"""' """,as_dict=1)
        for i in query:
            ar2.append(i)

    return ar,ar1,ar2
    """"""
@frappe.whitelist()
def duplicate(source_name, target_doc=None):
    def update_item(obj, target, source_parent):
        target.duplicate = 1
    doclist = get_mapped_doc(
        "Cost Working Tool",
        source_name,
        {
            "Cost Working Tool": {
                "doctype": "Cost Working Tool",
                "field_map":{
                    1:"duplicate"
                },
                "postprocess": update_item,
            }
        },
        target_doc
    )

    return doclist

@frappe.whitelist()
def generate_pdf(docname): 
    try:
        doc = frappe.get_doc('Cost Working Tool', docname)
        html = frappe.get_print(doc.doctype, doc.name,"Proposal")
        pdf = get_pdf(html)
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": str(doc.name)+".pdf",
            "file_url": "",
            "attached_to_doctype": doc.doctype,
            "attached_to_name": doc.name,
            "is_private": 0,
        })

        file_doc = save_file(file_doc.file_name, pdf, file_doc.doctype, file_doc.attached_to_name)

        frappe.db.commit()

        return file_doc.file_url

    except Exception as e:
        error_message = f"An error occurred: {str(e)} (Line {traceback.extract_tb(e.__traceback__)[0].lineno})"
        return error_message



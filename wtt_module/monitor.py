import frappe

@frappe.whitelist(allow_guest=True)
def getmonitoring(vs):
    data = frappe.parse_json(vs)
    username = data.get('username', '')
    p_hours = data.get('p_hours', 0.0)
    id_hours = data.get('id_hours', 0.0)
    total_hours = data.get('total_hours', 0.0)
    emp_code = ''
    if username == 'karthi':
        emp_code = 'WTT1401'
    elif username == 'Sathishkumar G':
        emp_code = 'WTT1194'
    elif username == 'design-1':
        emp_code = 'WTT948'
    elif username == 'proposal':
        emp_code = 'WTT947'
    elif username == 'ps':
        emp_code = 'WTT955'
    elif username == 'erp':
        emp_code = 'WTT1199'
    elif username == 'gma':
        emp_code = 'WTT1211'
    elif username == 'o&m':
        emp_code = 'WTT1278'
    elif username == 'hr-2':
        emp_code = 'WTT1301'
    elif username == 'ashok':
        emp_code = 'WTT756'
    elif username == 'design-5':
        emp_code = 'WTT1360'
    elif username == 'plc':
        emp_code = 'WTT1363'
    elif username == 'design-2':
        emp_code = 'WTT1367'
    elif username == 'process-5':
        emp_code = 'WTT1371'
    elif username == 'design-7':
        emp_code = 'WTT1379'
    elif username == 'process-6':
        emp_code = 'WTT1386'
    elif username == 'elec':
        emp_code = 'WTT1392'
    elif username == 'poa':
        emp_code = 'WTT1396'
    elif username == 'purchase-5':
        emp_code = 'WTT1398'
    elif username == 'qc':
        emp_code = 'WTT1402'
    elif username == 'design-9':
        emp_code = 'WTT1403'
    elif username == 'process-7':
        emp_code = 'WTT1404'
    elif username == 'rd':
        emp_code = 'WTT1405'
    elif username == 'Admin':
        emp_code = 'WTT1409'
    elif username == 'ps-1':
        emp_code = 'WTT1418'
    elif username == 'devaganesh':
        emp_code = 'WTT1420'
    elif username == 'arun':
        emp_code = 'WTT1421'
    elif username == 'process-8':
        emp_code = 'WTT1422'
    elif username == 'keerthana':
        emp_code = 'WTT1428'
    elif username == 'DINESH':
        emp_code = 'WTT1429'
    elif username == 'preamkumar':
        emp_code = 'WTT1432'
    elif username == 'srivatsan':
        emp_code = 'WTT1441'
    elif username == 'vinith':
        emp_code = 'WTT1447'
    elif username == 'gopika':
        emp_code = 'WTT1453'
    elif username == 'nithyanandan':
        emp_code = 'WTT1455'

    monitor_doc = frappe.new_doc("Monitoring Record")
    monitor_doc.employee = emp_code
    monitor_doc.productive_hours = p_hours
    monitor_doc.idle_hours = id_hours
    monitor_doc.total_hours = total_hours
    monitor_doc.insert(ignore_permissions=True)
    return "success"
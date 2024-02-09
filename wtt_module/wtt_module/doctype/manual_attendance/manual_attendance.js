// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Manual Attendance', {
	get_active_employees:function(frm){
		frm.clear_table("bulk_attendance_table")
		frm.refresh_field("bulk_attendance_table");
		frappe.call({
		method:"wtt_module.wtt_module.doctype.manual_attendance.manual_attendance.get_active",
		args:{
		nn:'ss'
		},
		callback(r){
			for(var i=0;i<r.message.length;i++)
			{
			var child = frm.add_child("manual_attendance_table");
			frappe.model.set_value(child.doctype, child.name, "employee", r.message[i].emp);
			frappe.model.set_value(child.doctype, child.name, "from_time", frm.doc.from_time);
			frappe.model.set_value(child.doctype, child.name, "to_time", frm.doc.to_time);
			frm.refresh_field("manual_attendance_table");
			}						
		}
	})
	},
	refresh: function(frm) {
		if (frm.doc.docstatus===1){
			frm.add_custom_button(__('Update Attendance'), () => {
			
			var arr2=[]
			$.each(frm.doc.manual_attendance_table, function (index, source_row) {
				arr2.push({
					"employee":source_row.employee,
					"from_time":source_row.from_time,
					"to_time":source_row.to_time
				})
			});


			frappe.call({
			method: 'wtt_module.wtt_module.doctype.manual_attendance.manual_attendance.update_att',
			args: { mn_detail: arr2 },
				callback(r) {
					frappe.msgprint("Attendance Updated Successfully")
				}
			});	
			});
		}
	}
});

// Copyright (c) 2021, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Task Assignment', {
	onload:function(frm,cdt,cdn){	
		var temp = frm.doc.works_table;

		for(var i=0;i<temp.length;i++){
			
			if(JSON.stringify(temp[i].no_mercy)==1){
				
				var df = frappe.meta.get_docfield("Work table","expected_date", frm.doc.name);
				df.read_only = 1;
			}
		}
		// if(frm.doc.user==frappe.session.user){
		// 	var df = frappe.meta.get_docfield("Work table","expected_date", frm.doc.name);
		// 	df.read_only = 0;
		// }
	},
	refresh: function(frm,cdt,cdn) {
		if(frm.doc.user==undefined && frm.doc.owner){
		frm.set_value("user",frm.doc.owner)
		}
		else if(frm.doc.user==undefined){
		frm.set_value("user",frappe.session.user)
		}
	}	
});
frappe.ui.form.on('Work table', {
	// onload:function(frm,cdt,cdn){
	// 	var temp = frm.doc.works_table;
	// 	for(i=0;i<temp.length;i++){
	// 		if(temp[i].no_mercy==1){
	// 			var df = frappe.meta.get_docfield("Work table","expected_date", frm.doc.name);
	// 			df.read_only = 1;
	// 		}
	// 	}

	// }
});
// 	status: function(frm,cdt,cdn) {
// 		var child = locals[cdt][cdn];
// 		if(child.status=='Completed'){
// 		frappe.call({
// 			method:"wtt_module.wtt_module.doctype.task_assignment.task_assignment.gain_points",
// 			args:{
// 				"e_date":child.expected_date,
// 				"a_date":child.assign_date,
// 				"points":child.total_points
// 			},
// 			callback:function(r){
// 				frappe.model.set_value(cdt,cdn,'gained_points',r.message);

// 			}
// 		})
// 		}
// 		else{
// 			frappe.model.set_value(cdt,cdn,'gained_points',0);	

// 		}
// 	},
// 	expected_date: function(frm,cdt,cdn){
// 		var child = locals[cdt][cdn];
// 		var cc=0
// 		if(child.assign_date>child.expected_date){
// 			frappe.model.set_value(cdt,cdn,'expected_date',"");
// 			frappe.throw("Task must need Time")
// 		}
// 	}	
// });

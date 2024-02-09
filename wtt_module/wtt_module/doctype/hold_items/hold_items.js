// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hold Items', {
	// refresh: function(frm) {

	// }
	setup: function(frm,cdt,cdn) {
		var ar=["Material Request","Purchase Order","Purchase Receipt"];
		var ar2=["1","0"]
		frm.set_query("request", function() {
		    return {
				filters: {
					'name': ['In', ar]
				}
			};
		});
		frm.set_query("number", function() {
		    return {
				filters: {
					'docstatus': ['In', ar2]
				}
			};
		});
		
	},
	number:function(frm){
		frappe.db.get_value(frm.doc.request, frm.doc.number, ['project'])
		    .then(r => {
		        let values = r.message;
		        frm.set_value("project",values.project)
		    })
	},

	get_items:function(frm){
		// if(!frm.doc.items){
			frappe.call({
			method:"wtt_module.wtt_module.doctype.hold_items.hold_items.get_items",
			args:{
				"doc":frm.doc.request,
				"num":frm.doc.number
			},
			callback(r){
				frm.set_value("items",r.message);
				frm.refresh_field("items");
			}
		})
		// }
		
	}

});

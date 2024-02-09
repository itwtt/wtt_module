// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mobile Users', {
	setup:function(frm){
		frm.set_query("employee",function(){
			return {
	            "filters": [
	                ["Employee", "status", "=", "Active"]
            	]
	        }
		})
	}
	// refresh: function(frm) {

	// }
});

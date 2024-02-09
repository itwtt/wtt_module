// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Process BOM Template', {
	// refresh: function(frm) {

	// }
	setup:function(frm){
		frm.set_query("bom",function(){
			return{
				filters:[
					['BOM','is_default','=',1],
					['BOM','is_active','=',1]
				]
			}
		})
	}
});

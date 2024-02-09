// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Site Materials', {
	// refresh: function(frm) {

	// }
	setup: function(frm){
		frm.set_query("project", function() {
			return {
				filters: [
					["Project","status", "=", "On going"],
					["Project","name", "not in", ['WTT-0408','WTT-0206','INT-HHT','HHT-INT','HO00001','HO-INT01','TTH00001','WTT-SALES','MDH00001','WTT-RD0002','SAL-0001','HOF00001','SATHY00001','OM00001']]					
				]
			};
		});

		frm.set_query("warehouse", function() {
			return {
				filters: [
					["Warehouse","company", "=", "WTT INTERNATIONAL PVT LTD"]
				]
			};
		});
	}
});

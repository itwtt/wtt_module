// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Planning', {
	// refresh: function(frm) {

	// }
	setup:function(frm){
		frm.set_query("project", function() {
			return {
				filters: [
					["Project","status", "=", "On going"],
					["Project","name","!=","HO-INT01"],
					["Project","name","!=","HO00001"],
					["Project","name","!=","HOF00001"],
					["Project","name","!=","MDH00001"],
					["Project","name","!=","SAL-0001"],
					["Project","name","!=","WTT-RD001"],
					["Project","name","!=","OM00001"],
					["Project","name","!=","SATHY00001"],
					["Project","name","!=","TTH00001"],
					["Project","name","!=","WTT-SALES"],
					["Project","name","!=","HHT-INT"],
					["Project","name","!=","INT-HHT"],
					["Project","name","!=","WTT-RD0002"]
				]
			};
		});
	}
});

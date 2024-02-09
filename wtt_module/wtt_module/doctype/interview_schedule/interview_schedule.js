// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Interview Schedule', {
	// refresh: function(frm) {

	// }
	onload:function(frm)
	{
		frm.set_query("hr_interviewer", function() {
			return {
				filters: [
					["Employee","department", "=", "Human Resources - WTT"],
					["Employee","status", "=", "Active"]
				]
			};
		});
	}
});

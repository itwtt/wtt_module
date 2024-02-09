// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('License renewal', {
	// refresh: function(frm) {

	// }
	validate:function(frm)
	{
		frappe.call({
				method:"wtt_module.wtt_module.doctype.license_renewal.license_renewal.create_license",
				args:{
					ss:'success'
				},
				callback(r){

				}
			});
	}
});

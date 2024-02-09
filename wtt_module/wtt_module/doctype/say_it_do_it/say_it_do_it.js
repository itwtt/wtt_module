// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Say It Do It', {
	refresh: function(frm) {
		frm.page.wrapper.find('.grey-link.dropdown-item:contains("Duplicate")').hide();
	}
});

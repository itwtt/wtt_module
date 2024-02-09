// Copyright (c) 2021, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tag Listing', {
	setup: function(frm){
        frm.get_docfield("items").allow_bulk_edit = 1;
    }
});

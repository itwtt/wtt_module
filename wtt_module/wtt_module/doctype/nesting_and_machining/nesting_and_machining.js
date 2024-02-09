// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Nesting and Machining', {
	setup(frm) {
		frm.set_query("parent_item", function() {
		    return {
				filters: [
					["Item","is_sub_contracted_item", "=", 1],
					["Item","is_stock_item", "=", 1],
					// ["Item","default_bom", "!=", '']

				]
			};
		});
	}
});

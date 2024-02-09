frappe.treeview_settings['Vendor Details'] = {
	get_tree_nodes: "wtt_module.wtt_module.doctype.vendor_details.vendor_details.get_children",
	add_tree_node: "wtt_module.wtt_module.doctype.vendor_details.vendor_details.add_node",
	filters: [
		{
			fieldname: "supplier",
			fieldtype:"Link",
			options: "Supplier",
			label: __("Supplier"),
		},
		{
			fieldname: "category",
			fieldtype:"Link",
			options: "Vendor Category",
			label: __("Vendor Category"),
		}
	],
	get_tree_root: false,
	root_label: "Vendor Details",
	ignore_fields: ["parent_vendor_details"],
	onload: function(me) {
		frappe.treeview_settings['Vendor Details'].page = {};
		$.extend(frappe.treeview_settings['Vendor Details'].page, me.page);
		me.make_tree();
	}
};
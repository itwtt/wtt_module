// frappe.provide("frappe.treeview_settings");
frappe.treeview_settings['Test tree'] = {
	get_tree_nodes: "wtt_module.wtt_module.doctype.test_tree.test_tree.get_children",
	add_tree_node: "wtt_module.wtt_module.doctype.test_tree.test_tree.add_node",
	filters: [
		{
			fieldname: "project",
			fieldtype:"Link",
			options: "Project",
			label: __("Project"),
		},
		{
			fieldname: "department",
			fieldtype:"Link",
			options: "Department",
			label: __("Department"),
		}
	],
	get_tree_root: false,
	root_label: "Test tree",
	ignore_fields: ["parent_test_tree"],
	onload: function(me) {
		frappe.treeview_settings['Test tree'].page = {};
		$.extend(frappe.treeview_settings['Test tree'].page, me.page);
		me.make_tree();
	}
};
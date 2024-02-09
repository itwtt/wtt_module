frappe.treeview_settings['Project Doc'] = {
	get_tree_nodes: "wtt_module.wtt_module.doctype.project_doc.project_doc.get_children",
	add_tree_node: "wtt_module.wtt_module.doctype.project_doc.project_doc.add_node",
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
	root_label: "Project Doc",
	ignore_fields: ["parent_project_doc"],
	onload: function(me) {
		frappe.treeview_settings['Project Doc'].page = {};
		$.extend(frappe.treeview_settings['Project Doc'].page, me.page);
		me.make_tree();
	}
};
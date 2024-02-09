frappe.listview_settings['Job Order Request'] = {
	get_indicator: function (doc) {
		const status_colors = {
			"Draft": "grey",
			"Pending": "orange",
			"Partially Received": "yellow",
			"Completed": "green",
			"Partially Transferred": "purple",
			"Transferred": "blue",
			"Closed": "red",
			"Cancelled": "red",
		};
		return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
	},
};
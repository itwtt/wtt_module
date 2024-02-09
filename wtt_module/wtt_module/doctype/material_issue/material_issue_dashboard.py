from frappe import _

def get_data():
	return {
		'fieldname': 'reference_material_issue',
		'internal_links': {
			
			'Material Request': ['items', 'material_request'],
			'Project': ['items', 'project'],
		},
		'transactions': [
			{
				'label': _('Reference'),
				'items': ['Material Request','Stock Entry','Project']
			},
			
		]
	}

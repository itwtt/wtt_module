from frappe import _

def get_data():
	return {
		'fieldname': 'delivery_note_request',
		'internal_links': {
			
			'Material Request': ['items', 'material_request'],
			'Project': ['items', 'project'],
		},
		'transactions': [
			{
				'label': _('Reference'),
				'items': ['Material Request','Project']
			},
			
		]
	}

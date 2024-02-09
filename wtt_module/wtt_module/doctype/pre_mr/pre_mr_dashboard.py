
from frappe import _


def get_data():
	return {
		'fieldname': 'pre_mr',
		'non_standard_fieldnames': {
			'Auto Repeat': 'reference_document'
		},
		'internal_links': {
			'Pre MR': ['items', 'pre_mr'],
			'Project': ['items', 'project'],
		},
		'transactions': [
			{			
				'label': _('Reference'),
				'items': ['Material Request']
			}
		]

	}


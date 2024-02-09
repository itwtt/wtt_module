
from frappe import _


def get_data():
	return {
		'fieldname': 'final_bank_statement',
		'non_standard_fieldnames': {
			'Auto Repeat': 'reference_document'
		},
		'transactions': [
			{			
				'label': _('Payment'),
				'items': ['Payment Entry']
			},
		]

	}

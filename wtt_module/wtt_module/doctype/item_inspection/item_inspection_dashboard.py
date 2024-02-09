
from frappe import _


def get_data():
	return {
		'fieldname': 'item_inspection',
		'non_standard_fieldnames': {
			'Auto Repeat': 'reference_document'
		},
		'internal_links': {
			'Purchase Receipt': ['items', 'purchase_receipt'],
			'Subcontracting Receipt':['items', 'subcontracting_receipt'],
			'Project': ['items', 'project'],
		},
		'transactions': [
			{			
				'label': _('Reference'),
				'items': ['Purchase Receipt','Subcontracting Receipt']
			},
			{
				'label': _('Subscription'),
				'items': ['Auto Repeat']
			},
		]

	}

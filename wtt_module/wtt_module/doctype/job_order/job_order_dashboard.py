
from frappe import _


def get_data():
	return {
		'fieldname': 'job_order_request',
		'non_standard_fieldnames': {
			'Auto Repeat': 'reference_document'
		},
		'internal_links': {
			'Material Issue': ['items', 'reference_material_issue'],
			'Stock Entry':['items','against_stock_entry'],
			'Material Request':['items','material_request']
		},
		'transactions': [
			{			
				'label': _('Reference'),
				'items': ['Material Request','Purchase Order','Material Issue','Stock Entry']
			}
		]

	}

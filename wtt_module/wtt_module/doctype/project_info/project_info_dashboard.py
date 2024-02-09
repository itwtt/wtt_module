
from frappe import _


def get_data():
	return {
		'fieldname': 'project',
		'transactions': [
			{			
				'label': _('Purchase'),
				'items': ['Material Request','Purchase Order','Purchase Receipt']
			},
			{
				'label':_('Sales'),
				'items':['Sales Invoice','Quotation']
			},
			{
				'label':_('Reference'),
				'items':['Site Info']
			}
		]

	}

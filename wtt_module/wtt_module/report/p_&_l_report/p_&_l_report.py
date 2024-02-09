
import frappe
from frappe import _
from frappe.utils import flt
import itertools

from erpnext.accounts.report.financial_statements import (
	#get_columns,
	get_data,
	get_filtered_list_for_consolidated_report,
	get_period_list,
)


def execute(filters=None):
	columns=get_columns()
	period_list = get_period_list(filters.from_fiscal_year, filters.to_fiscal_year,
		filters.period_start_date, filters.period_end_date, filters.filter_based_on, filters.periodicity,
		company=filters.company)

	income = get_data(filters.company, "Income", "Credit", period_list, filters = filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True, ignore_accumulated_values_for_fy= True)

	expense = get_data(filters.company, "Expense", "Debit", period_list, filters=filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True, ignore_accumulated_values_for_fy= True)

	
	data = []
	a1=[]
	a2=[]
	a3=[]
	a4=[]
	ar=[]
	ar1=[]
	aa=len(income)-1
	del income[aa]
	bb=len(expense)-1
	del expense[bb]
	tot1=income[len(income)-1]
	tot2=expense[len(expense)-1]
	for i in income:
		i["income_col"]=i.pop("account")
		i["total_income"]=i.pop("total")
		# i["is_group"]=i.pop("is_group")
		ar.append(i)
	
	for j in expense:
		j["expense_col"]=j.pop("account")
		j["total_expense"]=j.pop("total")
		ar1.append(j)
	
	for (i,j) in itertools.zip_longest(ar,ar1):
		if(j!=None):
			
			if(i!=None):
				j.update(i)
			else:
				j.update({"tt":"ff"})
			a1.append(j)
	data.extend(a1)

	currency = filters.presentation_currency or frappe.get_cached_value('Company', filters.company, "default_currency")

	return columns, data, None

def get_columns():
    columns=[
    {
            "label": _("Expense"),
            "fieldtype": "Link",
            "fieldname": "expense_col",
            "options":"Account",
            "width": 250
        },
        {
            "label": _("Total Expence"),
            "fieldtype": "Currency",
            "fieldname": "total_expense",
            "width": 200
        },
        {
            "label": _("Income"),
            "fieldtype": "Link",
            "fieldname": "income_col",
            "options":"Account",
            "width": 250
        },
        {
            "label": _("Total Income"),
            "fieldtype": "Currency",
            "fieldname": "total_income",
            "width": 200
        }
        
    ]
    return columns

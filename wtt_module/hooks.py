from . import __version__ as app_version

app_name = "wtt_module"
app_title = "wtt_module"
app_publisher = "wtt_module"
app_description = "wtt_module"
app_icon = "wtt_module"
app_color = "grey"
app_email = "wtt_module"
app_license = "wtt_module"

# Includes in <head>
# ------------------
web_include_css = "/assets/wtt_module/css/wtt_module.css"
web_include_js = "/assets/wtt_module/js/wtt_module.js"
# include js, css files in header of desk.html
app_include_css = "/assets/wtt_module/css/app_css.css"
# app_include_js = "/assets/wtt_module/js/wtt_module.js"

# include js, css files in header of web template
# web_include_css = "/assets/wtt_module/css/wtt_module.css"
# web_include_js = "/assets/wtt_module/js/wtt_module.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "wtt_module/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Material Request":"customization/custom/material_request.js",
	"Purchase Order":"customization/custom/purchase_order.js",
	"Item Inspection":"customization/custom/item_inspection.js",
	"Request for Quotation":"customization/custom/request_for_quotation.js",
	"Supplier Quotation":"customization/custom/supplier_quotation.js",
	"Purchase Receipt":"customization/custom/purchase_receipt.js",
	"Stock Entry":"customization/custom/stock_entry.js",
	"Delivery Note":"customization/custom/delivery_note.js",
	"Quotation":"customization/custom/quotation.js",
	"Job Applicant":"customization/custom/job_applicant.js",
	"Purchase Invoice":"customization/custom/purchase_invoice.js",
	"Bank Account":"customization/custom/bank_account.js",
	# "Subcontracting Receipt":"customization/overrides/subcontracting_receipt/subcontracting_receipt.js"
}
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "wtt_module.install.before_install"
# after_install = "wtt_module.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "wtt_module.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes
override_doctype_class = {
	"Material Request": "wtt_module.customization.overrides.custom_mr.customMR",
 	"Purchase Order": "wtt_module.customization.overrides.custom_po.customPO",
 	"Purchase Receipt": "wtt_module.customization.overrides.custom_pr.customPR",
 	"Purchase Invoice": "wtt_module.customization.overrides.custom_pi.customPI",
 	"Staffing Plan": "wtt_module.customization.overrides.custom_staffing_plan.customStaffingPlan",
 	"Quotation":  "wtt_module.customization.overrides.quotation.customQuotation",
 	"Journal Entry": "wtt_module.customization.overrides.custom_je.customJE",
 	"Supplier":"wtt_module.customization.overrides.supplier.customSupplier",
 	"Bank Account": "wtt_module.customization.overrides.custombank_account.customBankAccount",
 	"Supplier Quotation":"wtt_module.customization.overrides.supplier_quotation.CustomSupplierQuotation",
 	"Salary Slip": "wtt_module.customization.overrides.salary_slip.customSalarySlip",
 	"Landed Cost Voucher":"wtt_module.customization.overrides.lcv.custom_lcv",
 	"Subcontracting Receipt":"wtt_module.customization.overrides.subcontracting_receipt.subcontracting_receipt.customSCR",
 	"Stock Entry":"wtt_module.customization.overrides.stock_entry.customStockEntry"
 	
 	# "Employee":"wtt_module.customization.overrides.employee.customEmployee",
 	# "Request for Quotation":"wtt_module.customization.overrides.request_for_quotation.CustomRequestForQuotation",
 	#"Landed Cost Voucher":"wtt_module.customization.custom.landed_cost_voucher.LandedCostVoucher"
}
# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"cron": {
		"15 20 * * *": [
			"wtt_module.wtt_module.doctype.daily_activity.daily_activity.get_pending",
		]
	},
	"daily":[
		"wtt_module.wtt_module.doctype.task_allocation.task_allocation.sivakumar_task",
		"wtt_module.wtt_module.doctype.task_allocation.task_allocation.prabhu_task",
		"wtt_module.wtt_module.doctype.task_allocation.task_allocation.raghul_task",
		"wtt_module.wtt_module.doctype.task_allocation.task_allocation.ajith_task",
		# "wtt_module.wtt_module.doctype.task_assignment.task_assignment.make_taskpoints",
		"wtt_module.wtt_module.doctype.task_allocation.task_allocation.create_task"
	]
}
#scheduler_events = {
#	"cron":{
#		"5 13 * * *":[
#			"wtt_module.doctype.daily_sheet.daily_sheet.get_filter"
#		]
#	}
#}
#scheduler_events = {
#	"cron": {
#		"31 11 * * *": [
#			"wtt_module.wtt_module.doctype.daily_activity.daily_activity.get_pending"
#		]
#	}
#}
# 	"all": [
# 		"wtt_module.tasks.all"
# 	],
# 	"daily": [
# 		"wtt_module.tasks.daily"
# 	],
# 	"hourly": [
# 		"wtt_module.tasks.hourly"
# 	],
# 	"weekly": [
# 		"wtt_module.tasks.weekly"
# 	]
# 	"monthly": [
# 		"wtt_module.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "wtt_module.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"erpnext.stock.doctype.material_request.material_request.make_request_for_quotation": "wtt_module.customization.custom.material_request.make_request_for_quotation"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "wtt_module.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"wtt_module.auth.validate"
# ]




# old path
# "Material Request": "wtt_module.customization.custom.material_request.MaterialRequest",
#  	"Purchase Order": "wtt_module.customization.custom.purchase_order.PurchaseOrder",
#  	"Purchase Receipt": "wtt_module.customization.custom.purchase_receipt.PurchaseReceipt",
#  	"Journal Entry": "wtt_module.customization.custom.journal_entry.JournalEntry",
#  	"Staffing Plan": "wtt_module.customization.custom.staffing_plan.StaffingPlan",
#  	"Quotation":  "wtt_module.customization.custom.quotation.Quotation",
#  	"Job Applicant": "wtt_module.customization.custom.job_applicant.JobApplicant",
#  	"Supplier":"wtt_module.customization.custom.supplier.Supplier",
#  	"Supplier Quotation":"wtt_module.customization.custom.supplier_quotation.SupplierQuotation",
#  	"Salary Slip": "wtt_module.customization.custom_salary_slip.CustomSalarySlip",
#  	# "Salary Slip": "wtt_module.customization.custom.salary_slip.SalarySlip",


#  	#"Request for Quotation":"wtt_module.customization.custom.request_for_quotation.CustomRequest",
#  	"Employee":"wtt_module.customization.custom.employee.Employee",
#  	"Stock Entry": "wtt_module.customization.custom.stock_entry.StockEntry",
#  	"Bank Account": "wtt_module.customization.custom.bank_account.BankAccount",
#  	"Purchase Invoice": "wtt_module.customization.custom.purchase_invoice.PurchaseInvoice",
#  	"BOM":"wtt_module.customization.custom.custombom.custombom"
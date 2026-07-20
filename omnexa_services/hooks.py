app_name = "omnexa_services"
app_title = "ErpGenEx — Services"
app_publisher = "ErpGenEx"
app_description = "Services vertical"
app_email = "dev@erpgenex.com"
app_license = "mit"

# Apps
# ------------------

required_apps = ["omnexa_core", "omnexa_accounting", "omnexa_hr", "omnexa_customer_core", "omnexa_projects_pm"]

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
	{
		"name": "omnexa_services",
		"logo": "/assets/omnexa_services/logo.png",
		"title": "Services",
		"route": "/app/services"
	}
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/omnexa_services/css/omnexa_services.css"
# app_include_js = "/assets/omnexa_services/js/omnexa_services.js"

# include js, css files in header of web template
# web_include_css = "/assets/omnexa_services/css/omnexa_services.css"
# web_include_js = "/assets/omnexa_services/js/omnexa_services.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "omnexa_services/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "omnexa_services/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "omnexa_services.utils.jinja_methods",
# 	"filters": "omnexa_services.utils.jinja_filters"
# }

# Installation
# ------------

before_install = "omnexa_services.omnexa_services.install.enforce_supported_frappe_version"
before_migrate = "omnexa_services.omnexa_services.install.enforce_supported_frappe_version"
# after_install = "omnexa_services.omnexa_services.install.after_install"
# after_install intentionally disabled: KPI cards are synced by workspace patches/migrate.

# Uninstallation
# ------------

# before_uninstall = "omnexa_services.uninstall.before_uninstall"
# after_uninstall = "omnexa_services.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "omnexa_services.utils.before_app_install"
# after_app_install = "omnexa_services.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "omnexa_services.utils.before_app_uninstall"
# after_app_uninstall = "omnexa_services.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "omnexa_services.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Service Definition": "omnexa_services.permissions.service_definition_query_conditions",
	"Service SLA Policy": "omnexa_services.permissions.service_sla_policy_query_conditions",
	"Service Contract": "omnexa_services.permissions.service_contract_query_conditions",
	"Service Ticket": "omnexa_services.permissions.service_ticket_query_conditions",
	"Service Timesheet": "omnexa_services.permissions.service_timesheet_query_conditions"
	}
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Service Definition": {
		"before_validate": "omnexa_services.permissions.populate_company_branch_from_user_context",
		"validate": "omnexa_services.permissions.enforce_branch_access_for_doc"
	},
	"Service SLA Policy": {
		"before_validate": "omnexa_services.permissions.populate_company_branch_from_user_context",
		"validate": "omnexa_services.permissions.enforce_branch_access_for_doc"
	},
	"Service Contract": {
		"before_validate": "omnexa_services.permissions.populate_company_branch_from_user_context",
		"validate": "omnexa_services.permissions.enforce_branch_access_for_doc",
		"on_submit": "omnexa_services.revenue.ensure_revenue_schedule_for_contract"
	},
	"Service Ticket": {
		"before_validate": "omnexa_services.permissions.populate_company_branch_from_user_context",
		"validate": "omnexa_services.permissions.enforce_branch_access_for_doc"
	},
	"Service Timesheet": {
		"before_validate": "omnexa_services.permissions.populate_company_branch_from_user_context",
		"validate": "omnexa_services.permissions.enforce_branch_access_for_doc"}
	}

scheduler_events = {
	"hourly": [
		"omnexa_services.tasks.process_sla_escalations",
	]
	,
	"daily": [
		"omnexa_services.tasks.process_recurring_contract_billing",
	]
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"omnexa_services.tasks.all"
# 	],
# 	"daily": [
# 		"omnexa_services.tasks.daily"
# 	],
# 	"hourly": [
# 		"omnexa_services.tasks.hourly"
# 	],
# 	"weekly": [
# 		"omnexa_services.tasks.weekly"
# 	],
# 	"monthly": [
# 		"omnexa_services.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "omnexa_services.omnexa_services.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "omnexa_services.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "omnexa_services.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
before_request = ["omnexa_services.license_gate.before_request"]
# after_request = ["omnexa_services.utils.after_request"]

# Job Events
# ----------
# before_job = ["omnexa_services.utils.before_job"]
# after_job = ["omnexa_services.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{}",
# 		"filter_by": "{}",
# 		"redact_fields": ["{}", "{}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{}",
# 		"filter_by": "{}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"omnexa_services.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

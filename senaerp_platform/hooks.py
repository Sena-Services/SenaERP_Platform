app_name = "senaerp_platform"
app_title = "Senaerp Platform"
app_publisher = "Sena"
app_description = "Platform backend for senaerp.com"
app_email = "it@sena.services"
app_license = "unlicense"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "senaerp_platform",
# 		"logo": "/assets/senaerp_platform/logo.png",
# 		"title": "Senaerp Platform",
# 		"route": "/senaerp_platform",
# 		"has_permission": "senaerp_platform.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/senaerp_platform/css/senaerp_platform.css"
# app_include_js = "/assets/senaerp_platform/js/senaerp_platform.js"

# include js, css files in header of web template
# web_include_css = "/assets/senaerp_platform/css/senaerp_platform.css"
# web_include_js = "/assets/senaerp_platform/js/senaerp_platform.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "senaerp_platform/public/scss/website"

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
# app_include_icons = "senaerp_platform/public/icons.svg"

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
website_generators = ["Website Blog"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "senaerp_platform.utils.jinja_methods",
# 	"filters": "senaerp_platform.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "senaerp_platform.install.before_install"
# after_install = "senaerp_platform.install.after_install"

after_migrate = ["senaerp_platform.registry.seed.seed_registry"]

# Uninstallation
# ------------

# before_uninstall = "senaerp_platform.uninstall.before_uninstall"
# after_uninstall = "senaerp_platform.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "senaerp_platform.utils.before_app_install"
# after_app_install = "senaerp_platform.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "senaerp_platform.utils.before_app_uninstall"
# after_app_uninstall = "senaerp_platform.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "senaerp_platform.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"senaerp_platform.tasks.all"
# 	],
# 	"daily": [
# 		"senaerp_platform.tasks.daily"
# 	],
# 	"hourly": [
# 		"senaerp_platform.tasks.hourly"
# 	],
# 	"weekly": [
# 		"senaerp_platform.tasks.weekly"
# 	],
# 	"monthly": [
# 		"senaerp_platform.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "senaerp_platform.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "senaerp_platform.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "senaerp_platform.event.get_events"
# }

# Send emails via Microsoft Graph API instead of SMTP
override_email_send = "senaerp_platform.integrations.graph_email.send_via_graph"
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "senaerp_platform.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["senaerp_platform.utils.before_request"]
after_request = ["senaerp_platform.utils.after_request"]

# Job Events
# ----------
# before_job = ["senaerp_platform.utils.before_job"]
# after_job = ["senaerp_platform.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"senaerp_platform.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


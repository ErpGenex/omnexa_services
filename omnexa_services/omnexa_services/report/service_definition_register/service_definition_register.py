# Copyright (c) 2026, ErpGenEx
# Auto-generated Global Excellence report pack

import frappe
from frappe import _


def execute(filters=None):
	data = frappe.db.sql(
		"""
		SELECT `name`, `service_name`, `category`, `service_type`, `company`, `branch`
		FROM `tabService Definition`
		ORDER BY modified DESC
		LIMIT 500
		""",
		as_dict=True,
	)
	columns = [
		{"label": _("Name"), "fieldname": "name", "fieldtype": "Link", "width": 140},
		{"label": _("Service Name"), "fieldname": "service_name", "fieldtype": "Data", "width": 120},
		{"label": _("Category"), "fieldname": "category", "fieldtype": "Data", "width": 120},
		{"label": _("Service Type"), "fieldname": "service_type", "fieldtype": "Select", "width": 120},
		{"label": _("Company"), "fieldname": "company", "fieldtype": "Link", "width": 120},
		{"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "width": 120}
	]
	return columns, data

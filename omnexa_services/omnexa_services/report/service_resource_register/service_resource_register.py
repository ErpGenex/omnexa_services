# Copyright (c) 2026, ErpGenEx
# Auto-generated Global Excellence report pack

import frappe
from frappe import _


def execute(filters=None):
	data = frappe.db.sql(
		"""
		SELECT `name`, `resource_name`, `resource_type`, `user`, `company`, `branch`
		FROM `tabService Resource`
		ORDER BY modified DESC
		LIMIT 500
		""",
		as_dict=True,
	)
	columns = [
		{"label": _("Name"), "fieldname": "name", "fieldtype": "Link", "width": 140},
		{"label": _("Resource Name"), "fieldname": "resource_name", "fieldtype": "Data", "width": 120},
		{"label": _("Resource Type"), "fieldname": "resource_type", "fieldtype": "Select", "width": 120},
		{"label": _("User"), "fieldname": "user", "fieldtype": "Link", "width": 120},
		{"label": _("Company"), "fieldname": "company", "fieldtype": "Link", "width": 120},
		{"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "width": 120}
	]
	return columns, data

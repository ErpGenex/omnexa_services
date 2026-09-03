# Copyright (c) 2026, ErpGenEx
# Auto-generated Global Excellence report pack

import frappe
from frappe import _


def execute(filters=None):
	data = frappe.db.sql(
		"""
		SELECT `name`, `rule_name`, `is_active`, `company`, `branch`
		FROM `tabService Escalation Rule`
		ORDER BY modified DESC
		LIMIT 500
		""",
		as_dict=True,
	)
	columns = [
		{"label": _("Name"), "fieldname": "name", "fieldtype": "Link", "width": 140},
		{"label": _("Rule Name"), "fieldname": "rule_name", "fieldtype": "Data", "width": 120},
		{"label": _("Is Active"), "fieldname": "is_active", "fieldtype": "Check", "width": 120},
		{"label": _("Company"), "fieldname": "company", "fieldtype": "Link", "width": 120},
		{"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "width": 120}
	]
	return columns, data

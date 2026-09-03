# Copyright (c) 2026, ErpGenEx
# Auto-generated Global Excellence report pack

import frappe
from frappe import _


def execute(filters=None):
	data = frappe.db.sql(
		"""
		SELECT `name`, `skill_name`, `skill_category`
		FROM `tabService Skill`
		ORDER BY modified DESC
		LIMIT 500
		""",
		as_dict=True,
	)
	columns = [
		{"label": _("Name"), "fieldname": "name", "fieldtype": "Link", "width": 140},
		{"label": _("Skill Name"), "fieldname": "skill_name", "fieldtype": "Data", "width": 120},
		{"label": _("Category"), "fieldname": "skill_category", "fieldtype": "Data", "width": 120}
	]
	return columns, data

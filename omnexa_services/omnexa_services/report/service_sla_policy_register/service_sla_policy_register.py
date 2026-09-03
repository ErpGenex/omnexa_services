# Copyright (c) 2026, ErpGenEx
# Auto-generated Global Excellence report pack

import frappe
from frappe import _


def execute(filters=None):
	data = frappe.db.sql(
		"""
		SELECT `name`, `policy_name`, `priority_level`, `company`, `branch`
		FROM `tabService SLA Policy`
		ORDER BY modified DESC
		LIMIT 500
		""",
		as_dict=True,
	)
	columns = [
		{"label": _("Name"), "fieldname": "name", "fieldtype": "Link", "width": 140},
		{"label": _("Policy Name"), "fieldname": "policy_name", "fieldtype": "Data", "width": 120},
		{"label": _("Priority Level"), "fieldname": "priority_level", "fieldtype": "Select", "width": 120},
		{"label": _("Company"), "fieldname": "company", "fieldtype": "Link", "width": 120},
		{"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "width": 120}
	]
	return columns, data

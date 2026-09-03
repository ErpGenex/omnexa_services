# Copyright (c) 2026, ErpGenEx
# Auto-generated Global Excellence report pack

import frappe
from frappe import _


def execute(filters=None):
	data = frappe.db.sql(
		"""
		SELECT `name`, `contract`, `service_definition`, `recognition_method`, `schedule_start`, `schedule_end`
		FROM `tabService Revenue Schedule`
		ORDER BY modified DESC
		LIMIT 500
		""",
		as_dict=True,
	)
	columns = [
		{"label": _("Name"), "fieldname": "name", "fieldtype": "Link", "width": 140},
		{"label": _("Service Contract"), "fieldname": "contract", "fieldtype": "Link", "width": 120},
		{"label": _("Service"), "fieldname": "service_definition", "fieldtype": "Link", "width": 120},
		{"label": _("Recognition Method (IFRS 15)"), "fieldname": "recognition_method", "fieldtype": "Select", "width": 120},
		{"label": _("Schedule Start"), "fieldname": "schedule_start", "fieldtype": "Date", "width": 120},
		{"label": _("Schedule End"), "fieldname": "schedule_end", "fieldtype": "Date", "width": 120}
	]
	return columns, data

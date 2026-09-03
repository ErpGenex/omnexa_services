# Copyright (c) 2026, ErpGenEx
# Auto-generated Global Excellence report pack

import frappe
from frappe import _


def execute(filters=None):
	data = frappe.db.sql(
		"""
		SELECT `name`, `status`, `posting_date`, `customer_profile`, `contract`, `service_definition`
		FROM `tabService Invoice`
		ORDER BY modified DESC
		LIMIT 500
		""",
		as_dict=True,
	)
	columns = [
		{"label": _("Name"), "fieldname": "name", "fieldtype": "Link", "width": 140},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Select", "width": 120},
		{"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
		{"label": _("Customer Profile"), "fieldname": "customer_profile", "fieldtype": "Link", "width": 120},
		{"label": _("Service Contract"), "fieldname": "contract", "fieldtype": "Link", "width": 120},
		{"label": _("Service"), "fieldname": "service_definition", "fieldtype": "Link", "width": 120}
	]
	return columns, data

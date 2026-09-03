# Copyright (c) 2026, ErpGenEx
# Auto-generated Global Excellence report pack

import frappe
from frappe import _


def execute(filters=None):
	data = frappe.db.sql(
		"""
		SELECT `name`, `subject`, `customer_profile`, `company`, `branch`, `priority`
		FROM `tabService Ticket`
		ORDER BY modified DESC
		LIMIT 500
		""",
		as_dict=True,
	)
	columns = [
		{"label": _("Name"), "fieldname": "name", "fieldtype": "Link", "width": 140},
		{"label": _("Subject"), "fieldname": "subject", "fieldtype": "Data", "width": 120},
		{"label": _("Customer Profile"), "fieldname": "customer_profile", "fieldtype": "Link", "width": 120},
		{"label": _("Company"), "fieldname": "company", "fieldtype": "Link", "width": 120},
		{"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "width": 120},
		{"label": _("Priority"), "fieldname": "priority", "fieldtype": "Select", "width": 120}
	]
	return columns, data

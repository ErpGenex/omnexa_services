# Copyright (c) 2026, Omnexa and contributors
# License: MIT. See license.txt

import frappe
from frappe import _

from omnexa_core.omnexa_core.utils.report_charts import auto_chart_for_columns
from frappe.utils import flt
from omnexa_core.omnexa_core.branch_access import get_allowed_branches


def execute(filters=None):
	filters = frappe._dict(filters or {})
	if not filters.get("company"):
		frappe.throw(_("Company is required."), title=_("Filters"))

	# Billed service invoices — IFRS 15 revenue recognised when control transfers (billed).
	conditions = ["si.company = %(company)s", "si.status = 'Billed'"]
	if filters.get("branch"):
		conditions.append("si.branch = %(branch)s")
	if filters.get("from_date"):
		conditions.append("si.posting_date >= %(from_date)s")
	if filters.get("to_date"):
		conditions.append("si.posting_date <= %(to_date)s")

	allowed = get_allowed_branches(company=filters.company)
	if allowed is not None:
		if not allowed:
			return _columns(), []
		filters.allowed_branches = tuple(allowed)
		conditions.append("si.branch in %(allowed_branches)s")

	data = frappe.db.sql(
		f"""
		SELECT
			DATE_FORMAT(si.posting_date, '%%Y-%%m') AS period,
			COALESCE(SUM(si.amount), 0) AS revenue
		FROM `tabService Invoice` si
		WHERE {' AND '.join(conditions)}
		GROUP BY DATE_FORMAT(si.posting_date, '%%Y-%%m')
		ORDER BY period
		""",
		filters,
		as_dict=True,
	)
	for row in data:
		row["revenue"] = flt(row.revenue)
	columns = _columns()
	chart = auto_chart_for_columns(data, columns)
	return columns, data, None, chart


def _columns():
	return [
		{"label": _("Period"), "fieldname": "period", "fieldtype": "Data", "width": 130
	},
		{"label": _("Revenue"), "fieldname": "revenue", "fieldtype": "Currency", "width": 150
	},
	]

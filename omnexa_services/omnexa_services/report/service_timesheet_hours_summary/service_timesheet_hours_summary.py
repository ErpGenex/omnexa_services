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

	conditions = ["ts.company = %(company)s"]
	if filters.get("branch"):
		conditions.append("ts.branch = %(branch)s")
	if filters.get("from_date"):
		conditions.append("ts.posting_date >= %(from_date)s")
	if filters.get("to_date"):
		conditions.append("ts.posting_date <= %(to_date)s")

	allowed = get_allowed_branches(company=filters.company)
	if allowed is not None:
		if not allowed:
			return _columns(), []
		filters.allowed_branches = tuple(allowed)
		conditions.append("ts.branch in %(allowed_branches)s")

	data = frappe.db.sql(
		f"""
		SELECT
			ts.branch,
			DATE_FORMAT(ts.posting_date, '%%Y-%%m') AS period,
			COUNT(*) AS timesheet_count,
			COALESCE(SUM(ts.total_hours), 0) AS total_hours
		FROM `tabService Timesheet` ts
		WHERE {' AND '.join(conditions)}
		GROUP BY ts.branch, DATE_FORMAT(ts.posting_date, '%%Y-%%m')
		ORDER BY period DESC, ts.branch
		""",
		filters,
		as_dict=True,
	)
	for row in data:
		row["total_hours"] = flt(row.total_hours, 2)
	columns = _columns()
	chart = auto_chart_for_columns(data, columns)
	return columns, data, None, chart


def _columns():
	return [
		{"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 140},
		{"label": _("Period (YYYY-MM)"), "fieldname": "period", "fieldtype": "Data", "width": 110},
		{"label": _("Timesheets"), "fieldname": "timesheet_count", "fieldtype": "Int", "width": 100},
		{"label": _("Total hours"), "fieldname": "total_hours", "fieldtype": "Float", "width": 120},
	]

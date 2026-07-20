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

	conditions = ["t.company = %(company)s", "IFNULL(t.csat_rating, 0) > 0"]
	if filters.get("branch"):
		conditions.append("t.branch = %(branch)s")
	if filters.get("from_date"):
		conditions.append("DATE(t.creation) >= %(from_date)s")
	if filters.get("to_date"):
		conditions.append("DATE(t.creation) <= %(to_date)s")

	allowed = get_allowed_branches(company=filters.company)
	if allowed is not None:
		if not allowed:
			return _columns(), []
		filters.allowed_branches = tuple(allowed)
		conditions.append("t.branch in %(allowed_branches)s")

	data = frappe.db.sql(
		f"""
		SELECT
			t.branch,
			COUNT(*) AS rated_tickets,
			AVG(t.csat_rating) AS avg_csat
		FROM `tabService Ticket` t
		WHERE {' AND '.join(conditions)}
		GROUP BY t.branch
		ORDER BY avg_csat DESC
		""",
		filters,
		as_dict=True,
	)
	for row in data:
		row["avg_csat"] = flt(row.avg_csat, 2)
	columns = _columns()
	chart = auto_chart_for_columns(data, columns)
	return columns, data, None, chart


def _columns():
	return [
		{"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 140
	},
		{"label": _("Rated tickets"), "fieldname": "rated_tickets", "fieldtype": "Int", "width": 110
	},
		{"label": _("Avg CSAT"), "fieldname": "avg_csat", "fieldtype": "Float", "width": 100
	},
	]

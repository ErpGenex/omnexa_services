# Copyright (c) 2026, Omnexa and contributors
# License: MIT. See license.txt

import frappe
from frappe import _

from omnexa_core.omnexa_core.utils.report_charts import auto_chart_for_columns

from omnexa_core.omnexa_core.report_print.report_query_filters import (
	get_all_filters,
	policy_version_filters,
	prepare_filters,
	sql_conditions,
)



def execute(filters=None):
	columns = [
		{"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 130},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": _("Priority"), "fieldname": "priority", "fieldtype": "Data", "width": 100},
		{"label": _("Tickets"), "fieldname": "tickets", "fieldtype": "Int", "width": 90},
	]
	filters = prepare_filters(filters)
	conditions, params = sql_conditions(filters, "Service Ticket", date_field="creation", company=True, branch=True)
	rows = frappe.db.sql(
		f"""
		SELECT
			branch,
			status,
			priority,
			COUNT(name) AS tickets
		FROM `tabService Ticket`
		WHERE {' AND '.join(conditions)}
		GROUP BY branch, status, priority
		ORDER BY status ASC, priority ASC
		""",
		params,
		as_dict=True,
	)
	chart = auto_chart_for_columns(rows, columns)
	return columns, rows, None, chart
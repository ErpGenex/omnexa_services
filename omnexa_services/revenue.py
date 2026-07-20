from __future__ import annotations

import frappe
from frappe.utils import add_days, add_months, flt, get_last_day, getdate


def ensure_revenue_schedule_for_contract(contract_name: str):
	contract = frappe.get_doc("Service Contract", contract_name)
	service = frappe.get_doc("Service Definition", contract.service_definition)
	method = service.revenue_recognition or "Over Time"

	existing = frappe.db.get_value("Service Revenue Schedule", {"contract": contract.name, "status": ["!=", "Cancelled"]}, "name")
	if existing:
		return existing

	start = getdate(contract.contract_start)
	end = getdate(contract.contract_end) if contract.contract_end else get_last_day(start)
	total = flt(contract.billing_rate) if flt(contract.billing_rate) else flt(service.default_rate)

	sch = frappe.new_doc("Service Revenue Schedule")
	sch.contract = contract.name
	sch.service_definition = service.name
	sch.recognition_method = method
	sch.schedule_start = start
	sch.schedule_end = end
	sch.total_amount = total
	sch.status = "Active"
	sch.company = contract.company
	sch.branch = contract.branch

	if method == "Point in Time":
		sch.append(
			"rows",
			{
				"period_start": end,
				"period_end": end,
				"amount": total,
				"status": "Planned"
	},
		)
	else:
		# Over Time: monthly straight-line across contract duration (or at least one month)
		rows = _monthly_periods(start, end)
		per = flt(total / max(1, len(rows)), 2)
		for ps, pe in rows:
			sch.append("rows", {"period_start": ps, "period_end": pe, "amount": per, "status": "Planned"
	})

	sch.insert(ignore_permissions=True)
	return sch.name


def _monthly_periods(start, end):
	start = getdate(start)
	end = getdate(end)
	periods = []
	cur = start
	while cur <= end:
		pe = min(get_last_day(cur), end)
		periods.append((cur, pe))
		cur = add_days(pe, 1)
	return periods


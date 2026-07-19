import frappe
from frappe.utils import add_months, add_years, getdate, now_datetime, today


def process_sla_escalations():
	# Escalate tickets that breached SLA and are not closed
	now = now_datetime()
	rows = frappe.db.sql(
		"""
		SELECT name
		FROM `tabService Ticket`
		WHERE docstatus < 2
		  AND status NOT IN ('Resolved','Closed')
		  AND (
			(sla_response_due is not null AND first_response_on is null AND sla_response_due < %s)
			OR (sla_resolution_due is not null AND sla_resolution_due < %s)
		  )
		""",
		(now, now),
		as_dict=True,
	)
	for r in rows:
		doc = frappe.get_doc("Service Ticket", r.name)
		doc.is_sla_breached = 1
		if doc.status != "Escalated":
			doc.status = "Escalated"
		doc.save(ignore_permissions=True)
	apply_escalation_rules()


def apply_escalation_rules():
	# Apply configured escalation rules on breached / open tickets
	rules = frappe.get_all(
		"Service Escalation Rule",
		filters={"is_active": 1},
		fields=["name", "company", "branch", "priority", "when_sla_breached", "assign_to", "set_status"],
		order_by="modified desc",
	)
	if not rules:
		return

	candidates = frappe.get_all(
		"Service Ticket",
		filters={"docstatus": ["<", 2], "status": ["not in", ["Resolved", "Closed"]]},
		fields=["name", "company", "branch", "priority", "is_sla_breached", "assigned_to", "status"],
		limit_page_length=500,
	)
	for t in candidates:
		for r in rules:
			if r.company and t.company != r.company:
				continue
			if r.branch and t.branch != r.branch:
				continue
			if r.priority and t.priority != r.priority:
				continue
			if r.when_sla_breached and not t.is_sla_breached:
				continue

			doc = frappe.get_doc("Service Ticket", t.name)
			changed = False
			if r.assign_to and doc.assigned_to != r.assign_to:
				doc.assigned_to = r.assign_to
				changed = True
			if r.set_status and doc.status != r.set_status:
				doc.status = r.set_status
				changed = True
			if changed:
				doc.save(ignore_permissions=True)
			break


def process_recurring_contract_billing():
	current = getdate(today())
	contracts = frappe.get_all(
		"Service Contract",
		filters={"docstatus": 1, "status": "Active", "auto_bill": 1, "next_billing_date": ["<=", current]},
		pluck="name",
	)
	for name in contracts:
		contract = frappe.get_doc("Service Contract", name)
		_create_service_invoice_from_contract(contract)
		contract.last_billed_on = current
		contract.next_billing_date = _compute_next_billing_date(contract, current)
		contract.save(ignore_permissions=True)
	_process_milestones_for_contract(contract, current)


def _compute_next_billing_date(contract, base_date):
	cycle = contract.billing_cycle or "Monthly"
	if cycle == "One-time":
		return None
	if cycle == "Monthly":
		return add_months(base_date, 1)
	if cycle == "Quarterly":
		return add_months(base_date, 3)
	if cycle == "Yearly":
		return add_years(base_date, 1)
	return add_months(base_date, 1)


def _create_service_invoice_from_contract(contract):
	from omnexa_services.billing import create_service_invoice_from_contract

	create_service_invoice_from_contract(contract.name)


def _process_milestones_for_contract(contract, current):
	from omnexa_services.billing import create_sales_invoice_for_milestone

	if not getattr(contract, "milestones", None):
		return
	for row in contract.milestones:
		if row.status != "Pending":
			continue
		if row.due_date and getdate(row.due_date) <= current and row.amount:
			out = create_sales_invoice_for_milestone(contract.name, row.name)
			if out and out.get("sales_invoice"):
				row.status = "Invoiced"
				row.sales_invoice = out["sales_invoice"]
	contract.save(ignore_permissions=True)


from __future__ import annotations

import frappe
from frappe.utils import cint


@frappe.whitelist()
def kpi_open_tickets():
	value = frappe.db.count("Service Ticket", {"status": ["in", ["Open", "Assigned", "In Progress", "Escalated"]]})
	return {"value": cint(value), "fieldtype": "Int", "route": ["List", "Service Ticket"]}


@frappe.whitelist()
def kpi_sla_breached_tickets():
	value = frappe.db.count("Service Ticket", {"is_sla_breached": 1, "status": ["not in", ["Resolved", "Closed"]]})
	return {"value": cint(value), "fieldtype": "Int", "route": ["List", "Service Ticket"]}


@frappe.whitelist()
def create_ticket(
	*,
	customer_profile: str,
	subject: str,
	description: str | None = None,
	priority: str = "Medium",
	channel: str = "API",
	service_contract: str | None = None,
	service_definition: str | None = None,
):
	if not customer_profile:
		frappe.throw("customer_profile is required")
	doc = frappe.new_doc("Service Ticket")
	doc.customer_profile = customer_profile
	doc.subject = subject
	doc.description = description
	doc.priority = priority
	doc.channel = channel
	if service_contract:
		doc.service_contract = service_contract
	if service_definition:
		doc.service_definition = service_definition
	# Ensure mandatory company/branch are set for API/Portal intake
	profile = frappe.db.get_value("Customer Profile", customer_profile, ["company", "branch"], as_dict=True)
	if not profile:
		frappe.throw("Invalid customer_profile")
	doc.company = profile.company
	doc.branch = profile.branch
	if not (doc.company and doc.branch):
		frappe.throw("Customer Profile must have company and branch")
	doc.insert(ignore_permissions=True)
	return {"ticket": doc.name
	}

@frappe.whitelist()
def preview_sector_kpi(scenario: str | None = None, params: str | None = None) -> dict:
	"""SAP Wave C — sector KPI preview (omnexa_core bridge)."""
	from omnexa_core.omnexa_core.vertical_api import preview_sector_kpi as _core_preview

	return _core_preview("services", scenario=scenario, params=params)


from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt, getdate, today


def create_service_invoice_from_contract(contract_name: str):
	contract = frappe.get_doc("Service Contract", contract_name)
	if contract.docstatus != 1 or contract.status != "Active":
		return None

	service = frappe.get_doc("Service Definition", contract.service_definition)
	if not service.billing_item:
		frappe.throw(_("Set Billing Item on Service Definition before billing."), title=_("Billing"))

	linked_customer = frappe.db.get_value("Customer Profile", contract.customer_profile, "linked_customer")
	if not linked_customer:
		frappe.throw(_("Customer Profile is missing Linked Accounting Customer."), title=_("Billing"))

	posting_date = getdate(today())
	rate = flt(contract.billing_rate) if flt(contract.billing_rate) else flt(service.default_rate)

	sinv = frappe.new_doc("Service Invoice")
	sinv.company = contract.company
	sinv.branch = contract.branch
	sinv.customer_profile = contract.customer_profile
	sinv.contract = contract.name
	sinv.service_definition = contract.service_definition
	sinv.posting_date = posting_date
	sinv.amount = rate
	sinv.insert(ignore_permissions=True)

	from omnexa_core.omnexa_core.integration_bridge import create_sales_invoice, require_ok

	result = create_sales_invoice(
		{
			"company": contract.company,
			"branch": contract.branch,
			"customer": linked_customer,
			"posting_date": str(posting_date),
			"due_date": str(posting_date),
			"items": [
				{
					"item_code": service.billing_item,
					"qty": 1,
					"rate": rate,
					"description": f"Service billing for contract {contract.name}",
				}
			],
			"reference_doctype": "Service Contract",
			"reference_name": contract.name,
		},
		source_app="omnexa_services",
		idempotency_key=f"svc-contract-{contract.name}",
		submit=True,
	)
	sales_name = require_ok(result, title=_("Billing"))

	sinv.db_set("sales_invoice", sales_name, update_modified=False)
	sinv.db_set("status", "Billed", update_modified=False)
	return {"service_invoice": sinv.name, "sales_invoice": sales_name}


def create_sales_invoice_for_milestone(contract_name: str, milestone_rowname: str):
	contract = frappe.get_doc("Service Contract", contract_name)
	service = frappe.get_doc("Service Definition", contract.service_definition)
	if not service.billing_item:
		frappe.throw(_("Set Billing Item on Service Definition before billing."), title=_("Billing"))

	linked_customer = frappe.db.get_value("Customer Profile", contract.customer_profile, "linked_customer")
	if not linked_customer:
		frappe.throw(_("Customer Profile is missing Linked Accounting Customer."), title=_("Billing"))

	milestone = None
	for row in contract.milestones:
		if row.name == milestone_rowname:
			milestone = row
			break
	if not milestone or milestone.status != "Pending":
		return None

	posting_date = getdate(today())
	rate = flt(milestone.amount)

	from omnexa_core.omnexa_core.integration_bridge import create_sales_invoice, require_ok

	result = create_sales_invoice(
		{
			"company": contract.company,
			"branch": contract.branch,
			"customer": linked_customer,
			"posting_date": str(posting_date),
			"due_date": str(posting_date),
			"items": [
				{
					"item_code": service.billing_item,
					"qty": 1,
					"rate": rate,
					"description": f"Milestone: {milestone.milestone_title} (Contract {contract.name})",
				}
			],
			"reference_doctype": "Service Contract",
			"reference_name": contract.name,
		},
		source_app="omnexa_services",
		idempotency_key=f"svc-milestone-{contract.name}-{milestone_rowname}",
		submit=True,
	)
	sales_name = require_ok(result, title=_("Billing"))
	return {"sales_invoice": sales_name}


import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_months, add_years, getdate, today


class ServiceContract(Document):
	def validate(self):
		if self.contract_end and getdate(self.contract_end) < getdate(self.contract_start):
			frappe.throw(_("End Date cannot be before Start Date."), title=_("Contract"))
		if not self.contract_start:
			frappe.throw(_("Contract Start Date is mandatory."), title=_("Contract"))
		if not self.customer_profile:
			frappe.throw(_("Customer Profile is mandatory."), title=_("Contract"))
		if not self.sla_policy:
			frappe.throw(_("SLA Policy is mandatory."), title=_("Contract"))

		if not self.billing_rate:
			self.billing_rate = frappe.db.get_value("Service Definition", self.service_definition, "default_rate") or 0

	def on_submit(self):
		if self.status == "Draft":
			self.db_set("status", "Active", update_modified=False)
		if self.auto_bill and not self.next_billing_date:
			self.db_set("next_billing_date", getdate(today()), update_modified=False)

	def on_cancel(self):
		self.db_set("status", "Cancelled", update_modified=False)

	def compute_next_billing_date(self, base_date):
		cycle = self.billing_cycle or "Monthly"
		if cycle == "One-time":
			return None
		if cycle == "Monthly":
			return add_months(base_date, 1)
		if cycle == "Quarterly":
			return add_months(base_date, 3)
		if cycle == "Yearly":
			return add_years(base_date, 1)
		return add_months(base_date, 1)


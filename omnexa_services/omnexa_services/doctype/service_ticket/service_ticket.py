import frappe
from frappe.model.document import Document
from frappe.utils import add_to_date, flt, get_datetime, now_datetime


class ServiceTicket(Document):
	def before_insert(self):
		self.created_on = now_datetime()
		self._hydrate_from_contract_or_profile()

	def validate(self):
		self._hydrate_from_contract_or_profile()
		self._auto_assign()
		self._apply_sla()
		self._validate_lifecycle_controls()
		self._set_sla_breach_flags()
		self._set_sla_risk()

	def on_update(self):
		self._set_sla_breach_flags()

	def _hydrate_from_contract_or_profile(self):
		if self.service_contract:
			contract = frappe.db.get_value(
				"Service Contract", self.service_contract, ["company", "branch", "service_definition", "customer_profile"], as_dict=True
			)
			if contract:
				if not self.company:
					self.company = contract.company
				if not self.branch:
					self.branch = contract.branch
				if not self.service_definition:
					self.service_definition = contract.service_definition
				if not self.customer_profile:
					self.customer_profile = contract.customer_profile

		if self.customer_profile and (not self.company or not self.branch):
			profile = frappe.db.get_value("Customer Profile", self.customer_profile, ["company", "branch"], as_dict=True)
			if profile:
				self.company = self.company or profile.company
				self.branch = self.branch or profile.branch

		if self.service_definition and not self.required_skill:
			self.required_skill = frappe.db.get_value("Service Definition", self.service_definition, "default_skill")

	def _auto_assign(self):
		if self.assigned_to:
			return
		if not frappe.utils.cint(self.auto_assign):
			return
		from omnexa_services.assignment import pick_assignee

		assignee = pick_assignee(
			company=self.company,
			branch=self.branch,
			required_skill=self.required_skill,
		)
		if assignee:
			self.assigned_to = assignee
			if self.status == "Open":
				self.status = "Assigned"

	def _apply_sla(self):
		if not self.sla_policy:
			if self.service_contract:
				self.sla_policy = frappe.db.get_value("Service Contract", self.service_contract, "sla_policy")
		if not self.sla_policy:
			self.sla_policy = frappe.db.get_value(
				"Service SLA Policy", {"priority_level": self.priority, "is_active": 1, "company": self.company, "branch": self.branch
	}, "name"
			)

		if self.sla_policy and (not self.sla_response_due or not self.sla_resolution_due):
			policy = frappe.get_doc("Service SLA Policy", self.sla_policy)
			base = get_datetime(self.created_on) if self.created_on else now_datetime()
			self.sla_response_due = add_to_date(base, hours=policy.response_time_hours)
			self.sla_resolution_due = add_to_date(base, hours=policy.resolution_time_hours)

	def _set_sla_breach_flags(self):
		now = now_datetime()
		breached = 0
		if self.sla_response_due and not self.first_response_on and get_datetime(self.sla_response_due) < now:
			breached = 1
		if self.sla_resolution_due and self.status not in ("Resolved", "Closed") and get_datetime(self.sla_resolution_due) < now:
			breached = 1
		self.is_sla_breached = breached

	def _set_sla_risk(self):
		# Placeholder heuristic for AI-like breach prediction:
		# risk grows as we consume time budget towards resolution due.
		if not self.sla_resolution_due:
			self.sla_breach_risk = 0
			return
		start = get_datetime(self.created_on) if self.created_on else now_datetime()
		due = get_datetime(self.sla_resolution_due)
		now = now_datetime()
		total = (due - start).total_seconds()
		if total <= 0:
			self.sla_breach_risk = 100
			return
		elapsed = (now - start).total_seconds()
		ratio = max(0, min(1, elapsed / total))
		# bias upwards after 70% of budget
		risk = (ratio * 100.0) if ratio <= 0.7 else min(100.0, 70 + ((ratio - 0.7) / 0.3) * 30.0)
		if self.is_sla_breached:
			risk = 100.0
		self.sla_breach_risk = flt(risk, 2)

	def _validate_lifecycle_controls(self):
		if self.status in {"Assigned", "In Progress"} and not self.assigned_to:
			frappe.throw(_("Assigned To is mandatory when ticket is assigned or in progress."))

		if self.status in {"Resolved", "Closed"}:
			if not self.first_response_on:
				frappe.throw(_("First Response On is mandatory before resolving/closing a ticket."))
			if not self.assigned_to:
				frappe.throw(_("Assigned To is mandatory before resolving/closing a ticket."))


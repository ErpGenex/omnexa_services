import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class ServiceTimesheet(Document):
	def validate(self):
		self.total_hours = flt(sum([flt(r.hours) for r in self.entries]), 2)
		if not self.entries:
			frappe.throw(_("At least one timesheet entry is required."))
		if self.total_hours <= 0:
			frappe.throw(_("Total hours must be greater than zero."))


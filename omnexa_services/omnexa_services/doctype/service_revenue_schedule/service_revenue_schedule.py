import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate


class ServiceRevenueSchedule(Document):
	def validate(self):
		if self.schedule_end and self.schedule_start and getdate(self.schedule_end) < getdate(self.schedule_start):
			frappe.throw("Schedule end cannot be before schedule start")

		self.total_amount = flt(self.total_amount or 0)


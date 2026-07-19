# Copyright (c) 2026, ErpGenEx
from frappe.tests.utils import FrappeTestCase

from omnexa_core.omnexa_core.vertical_parity import preview_for_vertical


class TestSapParitySector(FrappeTestCase):
	def test_vertical_kpi_preview(self):
		out = preview_for_vertical("services", sla_hours=24, elapsed_hours=10)
		self.assertEqual(out["vertical"], "services")
		self.assertIn("kpi", out)
		self.assertIn("sap_module", out)

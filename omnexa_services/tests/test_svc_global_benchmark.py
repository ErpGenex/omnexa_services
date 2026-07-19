# Copyright (c) 2026, Omnexa
import json, frappe
from frappe.tests.utils import FrappeTestCase
from omnexa_services.svc_gap_register import GLOBAL_LEADER_TARGET, get_gap_status
from omnexa_services.svc_global_benchmark import get_global_svc_score
from omnexa_services.workspace.svc_workspace import sync_svc_workspace_menu

class TestSvcGlobalBenchmark(FrappeTestCase):
	def test_global_score(self):
		s = get_global_svc_score()
		self.assertGreaterEqual(s["weighted_score"], GLOBAL_LEADER_TARGET)
		self.assertTrue(s.get("global_leader_gate"))
	def test_gaps_closed(self):
		self.assertTrue(get_gap_status()["global_leader_gate"])
	def test_workspace_sync(self):
		stats = sync_svc_workspace_menu(save=True, rebuild=True)
		self.assertGreater(stats["total_links"], 10)
		ws = frappe.get_doc("Workspace", "Services")
		self.assertGreater(len(ws.shortcuts), 5)

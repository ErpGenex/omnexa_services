import frappe


def ensure_services_kpi_cards():
	card_defs = [
		("Open Tickets", "omnexa_services.api.kpi_open_tickets"),
		("SLA Breached", "omnexa_services.api.kpi_sla_breached_tickets"),
	]
	card_names: list[str] = []
	for label, method in card_defs:
		card_name = frappe.db.get_value("Number Card", {"label": label, "method": method}, "name")
		if not card_name:
			card = frappe.new_doc("Number Card")
			card.label = label
			card.type = "Custom"
			card.method = method
			card.module = "Omnexa Services"
			card.is_public = 1
			card.show_percentage_stats = 0
			card.insert(ignore_permissions=True)
			card_name = card.name
		card_names.append(card_name)

	if frappe.db.exists("Workspace", "Services"):
		workspace = frappe.get_doc("Workspace", "Services")
		workspace.number_cards = []
		for name in card_names:
			workspace.append("number_cards", {"number_card_name": name})
		workspace.save(ignore_permissions=True)
		frappe.db.commit()
		return {"workspace": workspace.name, "number_cards": card_names}

	# Services workspace may not be synced yet on fresh sites; do not fail app install.
	frappe.db.commit()
	return {"workspace": None, "number_cards": card_names}


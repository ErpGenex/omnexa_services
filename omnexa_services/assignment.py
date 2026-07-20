import frappe


def pick_assignee(*, company: str, branch: str, required_skill: str | None):
	"""
	Simple skill-based least-loaded assignment.
	- Filters active Service Resources within company/branch
	- If required_skill provided, resource must have it
	- Picks user with smallest open ticket count
	"""
	if not (company and branch):
		return None

	skill_join = ""
	skill_where = ""
	args = {"company": company, "branch": branch
	}
	if required_skill:
		skill_join = "JOIN `tabService Resource Skill` srs ON srs.parent = sr.name"
		skill_where = "AND srs.skill = %(skill)s"
		args["skill"] = required_skill

	row = frappe.db.sql(
		f"""
		SELECT
			sr.user AS user,
			(
				SELECT COUNT(st.name)
				FROM `tabService Ticket` st
				WHERE st.assigned_to = sr.user
				  AND st.company = %(company)s
				  AND st.branch = %(branch)s
				  AND st.status IN ('Open','Assigned','In Progress','Escalated')
				  AND st.docstatus < 2
			) AS open_tickets
		FROM `tabService Resource` sr
		{skill_join}
		WHERE sr.is_active = 1
		  AND sr.company = %(company)s
		  AND sr.branch = %(branch)s
		  AND sr.user IS NOT NULL
		  AND sr.user != ''
		  {skill_where}
		ORDER BY open_tickets ASC, sr.modified ASC
		LIMIT 1
		""",
		args,
		as_dict=True,
	)
	return row[0].user if row else None


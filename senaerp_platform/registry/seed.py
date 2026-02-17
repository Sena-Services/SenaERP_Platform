import frappe


# All 31 capability flag fieldnames
CAPABILITY_FLAGS = [
	"can_post_townhall",
	"can_read_townhall",
	"can_mention_individuals",
	"can_mention_all",
	"woken_by_direct_mention",
	"woken_by_all_mention",
	"woken_by_any_townhall",
	"can_send_text",
	"can_receive_text",
	"woken_by_text",
	"can_spawn",
	"can_kill_spawns",
	"spawnable",
	"can_inject",
	"injectable",
	"can_inline",
	"inlineable",
	"can_create_tasks",
	"can_read_tasks",
	"can_update_tasks",
	"can_cancel_tasks",
	"can_read_documents",
	"can_create_documents",
	"can_update_documents",
	"can_delete_documents",
	"can_mass_update",
	"can_mass_delete",
	"can_run_doc_method",
	"single_user_instance",
	"visible_in_agent_list",
	"ui_mode",
]

ROLES = [
	{
		"title": "Default",
		"description": "The default role for agents with no specific role assigned",
	},
	{
		"title": "Communicator",
		"description": "Handles external communication and user interaction",
	},
	{
		"title": "Orchestrator",
		"description": "Coordinates and manages other agents within a team",
	},
	{
		"title": "Worker",
		"description": "Executes specific tasks and operations",
	},
]

# Standard team type: nuanced permissions per role
# Format: dict of overrides from the default "deny" base
STANDARD_ROLE_CONFIGS = {
	"Default": {
		"can_post_townhall": "allow",
		"can_read_townhall": "allow",
		"can_mention_individuals": "allow",
		"woken_by_direct_mention": "allow",
		"can_send_text": "allow",
		"can_receive_text": "allow",
		"woken_by_text": "allow",
		"can_create_tasks": "allow",
		"can_read_tasks": "allow",
		"can_update_tasks": "allow",
		"can_read_documents": "allow",
		"visible_in_agent_list": "allow",
		"ui_mode": "chat",
	},
	"Communicator": {
		"can_post_townhall": "allow",
		"can_read_townhall": "allow",
		"can_mention_individuals": "allow",
		"can_mention_all": "approval_required",
		"woken_by_direct_mention": "allow",
		"woken_by_all_mention": "allow",
		"can_send_text": "allow",
		"can_receive_text": "allow",
		"woken_by_text": "allow",
		"injectable": "allow",
		"can_create_tasks": "allow",
		"can_read_tasks": "allow",
		"can_update_tasks": "allow",
		"can_read_documents": "allow",
		"visible_in_agent_list": "allow",
		"ui_mode": "chat",
	},
	"Orchestrator": {
		"can_post_townhall": "allow",
		"can_read_townhall": "allow",
		"can_mention_individuals": "allow",
		"can_mention_all": "allow",
		"woken_by_direct_mention": "allow",
		"woken_by_all_mention": "allow",
		"woken_by_any_townhall": "allow",
		"can_send_text": "allow",
		"can_receive_text": "allow",
		"woken_by_text": "allow",
		"can_spawn": "allow",
		"can_kill_spawns": "allow",
		"can_inject": "allow",
		"can_inline": "allow",
		"can_create_tasks": "allow",
		"can_read_tasks": "allow",
		"can_update_tasks": "allow",
		"can_cancel_tasks": "allow",
		"can_read_documents": "allow",
		"visible_in_agent_list": "allow",
		"ui_mode": "chat",
	},
	"Worker": {
		"can_read_townhall": "allow",
		"woken_by_direct_mention": "allow",
		"can_send_text": "allow",
		"can_receive_text": "allow",
		"woken_by_text": "allow",
		"spawnable": "allow",
		"injectable": "allow",
		"inlineable": "allow",
		"can_create_tasks": "allow",
		"can_read_tasks": "allow",
		"can_update_tasks": "allow",
		"can_read_documents": "allow",
		"can_create_documents": "allow",
		"can_update_documents": "allow",
		"can_run_doc_method": "allow",
		"visible_in_agent_list": "allow",
		"ui_mode": "chat",
	},
}


def seed_registry():
	"""Seed the registry with pre-defined roles and team types. Idempotent."""
	role_map = _seed_roles()
	_seed_team_types(role_map)
	frappe.db.commit()


def _seed_roles():
	"""Create the 4 pre-seeded agent roles. Returns {title: extension_name}."""
	role_map = {}
	for role in ROLES:
		existing = frappe.db.get_value(
			"Registry",
			{"title": role["title"], "item_type": "Agent Role"},
			"ref_name",
		)
		if existing:
			role_map[role["title"]] = existing
			continue

		reg = frappe.new_doc("Registry")
		reg.title = role["title"]
		reg.item_type = "Agent Role"
		reg.description = role["description"]
		reg.trust_status = "approved"
		reg.author = "Sena"
		reg.insert(ignore_permissions=True)
		role_map[role["title"]] = reg.ref_name

	return role_map


def _seed_team_types(role_map):
	"""Create the 2 pre-seeded team types with role configs."""
	_seed_team_type(
		title="Default",
		description="Permissive team type. All capabilities allowed for all roles. Overridable at agent level.",
		overridable=1,
		role_map=role_map,
		all_allow=True,
	)
	_seed_team_type(
		title="Standard",
		description="Balanced team type with role-appropriate permissions. Not overridable.",
		overridable=0,
		role_map=role_map,
		all_allow=False,
	)


def _seed_team_type(title, description, overridable, role_map, all_allow):
	existing = frappe.db.get_value(
		"Registry",
		{"title": title, "item_type": "Team Type"},
		"ref_name",
	)
	if existing:
		return

	reg = frappe.new_doc("Registry")
	reg.title = title
	reg.item_type = "Team Type"
	reg.description = description
	reg.trust_status = "approved"
	reg.author = "Sena"
	reg.insert(ignore_permissions=True)

	# Populate extension with role configs
	ext = frappe.get_doc("Registry Team Type", reg.ref_name)
	ext.overridable = overridable

	for role_title, role_ext_name in role_map.items():
		config = {"role": role_ext_name, "min_agents": 1, "max_agents": 1}

		if all_allow:
			for flag in CAPABILITY_FLAGS:
				if flag == "ui_mode":
					config[flag] = "chat"
				else:
					config[flag] = "allow"
		else:
			overrides = STANDARD_ROLE_CONFIGS.get(role_title, {})
			for flag in CAPABILITY_FLAGS:
				if flag == "ui_mode":
					config[flag] = overrides.get(flag, "chat")
				elif flag == "visible_in_agent_list":
					config[flag] = overrides.get(flag, "allow")
				else:
					config[flag] = overrides.get(flag, "deny")

		ext.append("role_configs", config)

	ext.save(ignore_permissions=True)

"""Registry seed data.

Seeds pre-defined Agent Roles and Team Types on every bench migrate.
Mirrors the canonical flag definitions from the Runtime's flag_resolver.
"""

from __future__ import annotations

import frappe

ALL_FLAG_NAMES = [
	# Townhall (7)
	"can_post_townhall",
	"can_read_townhall",
	"can_mention_individuals",
	"can_mention_all",
	"woken_by_direct_mention",
	"woken_by_all_mention",
	"woken_by_any_townhall",
	# Texting (3)
	"can_send_text",
	"can_receive_text",
	"woken_by_text",
	# Presets (2)
	"spawn_preset",
	"inline_preset",
	# Instances (4)
	"can_create_standard",
	"can_create_ephemeral",
	"can_kill_instance",
	"spawnable",
	# Injection (4)
	"can_inject",
	"injectable",
	"inject_scope",
	"inject_target_roles",
	# Tasks (4)
	"can_create_tasks",
	"can_read_tasks",
	"can_update_tasks",
	"can_cancel_tasks",
	# DocType access (7)
	"can_read_documents",
	"can_create_documents",
	"can_update_documents",
	"can_delete_documents",
	"can_mass_update",
	"can_mass_delete",
	"can_run_doc_method",
	# Instance (1)
	"single_user_instance",
	# Discovery (1)
	"visible_in_agent_list",
	# UI (1)
	"ui_mode",
]

ROLES = [
	{
		"title": "Default",
		"description": "General-purpose standalone agent. Used by single-agent teams.",
		"can_post_townhall": "allow",
		"can_read_townhall": "allow",
		"can_mention_individuals": "allow",
		"can_mention_all": "approval_required",
		"woken_by_direct_mention": "allow",
		"woken_by_all_mention": "allow",
		"woken_by_any_townhall": "deny",
		"can_send_text": "allow",
		"can_receive_text": "allow",
		"woken_by_text": "allow",
		"spawn_preset": "deny",
		"inline_preset": "deny",
		"can_create_standard": "deny",
		"can_create_ephemeral": "deny",
		"can_kill_instance": "deny",
		"spawnable": "deny",
		"can_inject": "allow",
		"injectable": "deny",
		"inject_scope": "spawns_only",
		"inject_target_roles": "",
		"can_create_tasks": "allow",
		"can_read_tasks": "allow",
		"can_update_tasks": "allow",
		"can_cancel_tasks": "allow",
		"can_read_documents": "allow",
		"can_create_documents": "allow",
		"can_update_documents": "allow",
		"can_delete_documents": "approval_required",
		"can_mass_update": "deny",
		"can_mass_delete": "deny",
		"can_run_doc_method": "allow",
		"single_user_instance": "deny",
		"visible_in_agent_list": "allow",
		"ui_mode": "chat",
	},
	{
		"title": "Communicator",
		"description": "User-facing agent. Handles chat, texting, townhall, task creation.",
		"can_post_townhall": "allow",
		"can_read_townhall": "allow",
		"can_mention_individuals": "allow",
		"can_mention_all": "approval_required",
		"woken_by_direct_mention": "allow",
		"woken_by_all_mention": "allow",
		"woken_by_any_townhall": "deny",
		"can_send_text": "allow",
		"can_receive_text": "allow",
		"woken_by_text": "allow",
		"spawn_preset": "deny",
		"inline_preset": "deny",
		"can_create_standard": "deny",
		"can_create_ephemeral": "deny",
		"can_kill_instance": "deny",
		"spawnable": "deny",
		"can_inject": "allow",
		"injectable": "deny",
		"inject_scope": "team_role",
		"inject_target_roles": "Orchestrator",
		"can_create_tasks": "allow",
		"can_read_tasks": "allow",
		"can_update_tasks": "deny",
		"can_cancel_tasks": "allow",
		"can_read_documents": "allow",
		"can_create_documents": "allow",
		"can_update_documents": "allow",
		"can_delete_documents": "approval_required",
		"can_mass_update": "deny",
		"can_mass_delete": "deny",
		"can_run_doc_method": "allow",
		"single_user_instance": "deny",
		"visible_in_agent_list": "allow",
		"ui_mode": "chat",
	},
	{
		"title": "Orchestrator",
		"description": "Background task manager. Spawns workers, manages the task board.",
		"can_post_townhall": "deny",
		"can_read_townhall": "deny",
		"can_mention_individuals": "deny",
		"can_mention_all": "deny",
		"woken_by_direct_mention": "deny",
		"woken_by_all_mention": "deny",
		"woken_by_any_townhall": "deny",
		"can_send_text": "deny",
		"can_receive_text": "deny",
		"woken_by_text": "deny",
		"spawn_preset": "allow",
		"inline_preset": "deny",
		"can_create_standard": "allow",
		"can_create_ephemeral": "deny",
		"can_kill_instance": "allow",
		"spawnable": "deny",
		"can_inject": "allow",
		"injectable": "allow",
		"inject_scope": "spawns_only",
		"inject_target_roles": "",
		"can_create_tasks": "allow",
		"can_read_tasks": "allow",
		"can_update_tasks": "allow",
		"can_cancel_tasks": "allow",
		"can_read_documents": "allow",
		"can_create_documents": "allow",
		"can_update_documents": "allow",
		"can_delete_documents": "deny",
		"can_mass_update": "deny",
		"can_mass_delete": "deny",
		"can_run_doc_method": "allow",
		"single_user_instance": "allow",
		"visible_in_agent_list": "deny",
		"ui_mode": "none",
	},
	{
		"title": "Worker",
		"description": "Spawnable execution unit. Does the actual work.",
		"can_post_townhall": "deny",
		"can_read_townhall": "deny",
		"can_mention_individuals": "deny",
		"can_mention_all": "deny",
		"woken_by_direct_mention": "deny",
		"woken_by_all_mention": "deny",
		"woken_by_any_townhall": "deny",
		"can_send_text": "deny",
		"can_receive_text": "deny",
		"woken_by_text": "deny",
		"spawn_preset": "deny",
		"inline_preset": "deny",
		"can_create_standard": "deny",
		"can_create_ephemeral": "deny",
		"can_kill_instance": "deny",
		"spawnable": "allow",
		"can_inject": "allow",
		"injectable": "allow",
		"inject_scope": "parent_only",
		"inject_target_roles": "",
		"can_create_tasks": "deny",
		"can_read_tasks": "allow",
		"can_update_tasks": "deny",
		"can_cancel_tasks": "deny",
		"can_read_documents": "allow",
		"can_create_documents": "allow",
		"can_update_documents": "allow",
		"can_delete_documents": "deny",
		"can_mass_update": "deny",
		"can_mass_delete": "deny",
		"can_run_doc_method": "allow",
		"single_user_instance": "deny",
		"visible_in_agent_list": "allow",
		"ui_mode": "none",
	},
]


def seed_registry() -> None:
	"""Seed the registry with pre-defined roles and team types. Idempotent."""
	role_map = _seed_roles()
	_seed_team_types(role_map)
	frappe.db.commit()


def _seed_roles() -> dict[str, str]:
	"""Create or update the 4 pre-seeded agent roles. Returns {title: extension_name}."""
	role_map: dict[str, str] = {}
	for role_def in ROLES:
		title = role_def["title"]
		ref_name = frappe.db.get_value(
			"Registry",
			{"title": title, "item_type": "Agent Role"},
			"ref_name",
		)

		if ref_name:
			ext = frappe.get_doc("Registry Agent Role", ref_name)
			for flag in ALL_FLAG_NAMES:
				setattr(ext, flag, role_def[flag])
			ext.save(ignore_permissions=True)
			role_map[title] = ref_name
			continue

		reg = frappe.new_doc("Registry")
		reg.title = title
		reg.item_type = "Agent Role"
		reg.description = role_def["description"]
		reg.trust_status = "approved"
		reg.author = "Sena"
		reg.insert(ignore_permissions=True)

		ext = frappe.get_doc("Registry Agent Role", reg.ref_name)
		for flag in ALL_FLAG_NAMES:
			setattr(ext, flag, role_def[flag])
		ext.save(ignore_permissions=True)

		role_map[title] = reg.ref_name

	return role_map


def _seed_team_types(role_map: dict[str, str]) -> None:
	"""Create the 2 pre-seeded team types with role configs."""
	_seed_team_type(
		title="Default",
		description="Permissive team type. All capabilities allowed for all roles. Overridable at agent level.",
		overridable=1,
		role_map=role_map,
	)
	_seed_team_type(
		title="Standard",
		description="Balanced team type with role-appropriate permissions. Not overridable.",
		overridable=0,
		role_map=role_map,
	)


def _seed_team_type(
	title: str,
	description: str,
	overridable: int,
	role_map: dict[str, str],
) -> None:
	existing = frappe.db.get_value(
		"Registry",
		{"title": title, "item_type": "Team Type"},
		"ref_name",
	)
	if existing:
		ext = frappe.get_doc("Registry Team Type", existing)
		ext.overridable = overridable
		ext.set("role_configs", [])
		for role_title, role_ext_name in role_map.items():
			ext.append("role_configs", {
				"role": role_ext_name,
				"min_agents": 1,
				"max_agents": 1,
			})
		ext.save(ignore_permissions=True)
		return

	reg = frappe.new_doc("Registry")
	reg.title = title
	reg.item_type = "Team Type"
	reg.description = description
	reg.trust_status = "approved"
	reg.author = "Sena"
	reg.insert(ignore_permissions=True)

	ext = frappe.get_doc("Registry Team Type", reg.ref_name)
	ext.overridable = overridable
	for role_title, role_ext_name in role_map.items():
		ext.append("role_configs", {
			"role": role_ext_name,
			"min_agents": 1,
			"max_agents": 1,
		})
	ext.save(ignore_permissions=True)

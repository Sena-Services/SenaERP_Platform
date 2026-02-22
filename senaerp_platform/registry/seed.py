"""Registry seed data.

Seeds pre-defined Agent Templates and Team Templates on every bench migrate.
Uses the new direct property/trigger/overridable Check fields.
"""

from __future__ import annotations

import frappe

PROPERTY_FIELDS = [
	"injectable",
	"can_be_killed",
	"can_be_created_standard",
	"can_be_created_ephemeral",
	"visible_in_agent_list",
	"single_user_instance",
	"is_worker_agent",
	"is_onetime_agent",
]

TRIGGER_FIELDS = [
	"trigger_user_message",
	"trigger_agent_wakeup",
	"trigger_comms_inbox",
	"trigger_comms_mention_direct",
	"trigger_comms_mention_all",
	"trigger_comms_townhall_any",
	"trigger_tasks",
]

OVERRIDABLE_FIELDS = [
	"model_overridable",
	"skills_overridable",
	"tools_overridable",
	"triggers_overridable",
	"properties_overridable",
	"ui_overridable",
	"logic_overridable",
]

ALL_TEMPLATE_FIELDS = PROPERTY_FIELDS + TRIGGER_FIELDS + OVERRIDABLE_FIELDS

TEMPLATES = [
	{
		"title": "Default",
		"description": "General-purpose standalone agent. Used by single-agent teams.",
		# Properties
		"injectable": 0,
		"can_be_killed": 0,
		"can_be_created_standard": 0,
		"can_be_created_ephemeral": 0,
		"visible_in_agent_list": 1,
		"single_user_instance": 0,
		"is_worker_agent": 0,
		"is_onetime_agent": 0,
		# Triggers
		"trigger_user_message": 1,
		"trigger_agent_wakeup": 0,
		"trigger_comms_inbox": 1,
		"trigger_comms_mention_direct": 1,
		"trigger_comms_mention_all": 1,
		"trigger_comms_townhall_any": 0,
		"trigger_tasks": 1,
		# Overridable
		"model_overridable": 1,
		"skills_overridable": 1,
		"tools_overridable": 1,
		"triggers_overridable": 1,
		"properties_overridable": 1,
		"ui_overridable": 1,
		"logic_overridable": 1,
	},
	{
		"title": "Communicator",
		"description": "User-facing agent. Handles chat, mentions, task creation.",
		"injectable": 0,
		"can_be_killed": 0,
		"can_be_created_standard": 0,
		"can_be_created_ephemeral": 0,
		"visible_in_agent_list": 1,
		"single_user_instance": 0,
		"is_worker_agent": 0,
		"is_onetime_agent": 0,
		"trigger_user_message": 1,
		"trigger_agent_wakeup": 0,
		"trigger_comms_inbox": 1,
		"trigger_comms_mention_direct": 1,
		"trigger_comms_mention_all": 1,
		"trigger_comms_townhall_any": 0,
		"trigger_tasks": 1,
		"model_overridable": 1,
		"skills_overridable": 1,
		"tools_overridable": 1,
		"triggers_overridable": 1,
		"properties_overridable": 1,
		"ui_overridable": 1,
		"logic_overridable": 1,
	},
	{
		"title": "Orchestrator",
		"description": "Background task manager. Spawns workers, manages the task board.",
		"injectable": 1,
		"can_be_killed": 0,
		"can_be_created_standard": 1,
		"can_be_created_ephemeral": 0,
		"visible_in_agent_list": 0,
		"single_user_instance": 1,
		"is_worker_agent": 1,
		"is_onetime_agent": 0,
		"trigger_user_message": 0,
		"trigger_agent_wakeup": 1,
		"trigger_comms_inbox": 0,
		"trigger_comms_mention_direct": 0,
		"trigger_comms_mention_all": 0,
		"trigger_comms_townhall_any": 0,
		"trigger_tasks": 1,
		"model_overridable": 1,
		"skills_overridable": 1,
		"tools_overridable": 1,
		"triggers_overridable": 0,
		"properties_overridable": 0,
		"ui_overridable": 0,
		"logic_overridable": 1,
	},
	{
		"title": "Worker",
		"description": "Spawnable execution unit. Does the actual work.",
		"injectable": 1,
		"can_be_killed": 1,
		"can_be_created_standard": 0,
		"can_be_created_ephemeral": 1,
		"visible_in_agent_list": 0,
		"single_user_instance": 0,
		"is_worker_agent": 1,
		"is_onetime_agent": 0,
		"trigger_user_message": 0,
		"trigger_agent_wakeup": 1,
		"trigger_comms_inbox": 0,
		"trigger_comms_mention_direct": 0,
		"trigger_comms_mention_all": 0,
		"trigger_comms_townhall_any": 0,
		"trigger_tasks": 0,
		"model_overridable": 1,
		"skills_overridable": 1,
		"tools_overridable": 0,
		"triggers_overridable": 0,
		"properties_overridable": 0,
		"ui_overridable": 0,
		"logic_overridable": 0,
	},
]


def seed_registry() -> None:
	"""Seed the registry with pre-defined templates and team templates. Idempotent."""
	template_map = _seed_templates()
	_seed_team_templates(template_map)
	frappe.db.commit()


def _seed_templates() -> dict[str, str]:
	"""Create or update the 4 pre-seeded agent templates. Returns {title: extension_name}."""
	template_map: dict[str, str] = {}
	for tmpl_def in TEMPLATES:
		title = tmpl_def["title"]
		ref_name = frappe.db.get_value(
			"Registry",
			{"title": title, "item_type": "Agent Template"},
			"ref_name",
		)

		if ref_name:
			ext = frappe.get_doc("Registry Agent Template", ref_name)
			for field in ALL_TEMPLATE_FIELDS:
				setattr(ext, field, tmpl_def[field])
			ext.save(ignore_permissions=True)
			template_map[title] = ref_name
			continue

		reg = frappe.new_doc("Registry")
		reg.title = title
		reg.item_type = "Agent Template"
		reg.description = tmpl_def["description"]
		reg.trust_status = "approved"
		reg.author = "Sena"
		reg.insert(ignore_permissions=True)

		ext = frappe.get_doc("Registry Agent Template", reg.ref_name)
		for field in ALL_TEMPLATE_FIELDS:
			setattr(ext, field, tmpl_def[field])
		ext.save(ignore_permissions=True)

		template_map[title] = reg.ref_name

	return template_map


def _seed_team_templates(template_map: dict[str, str]) -> None:
	"""Create the 2 pre-seeded team templates with role configs."""
	_seed_team_template(
		title="Default",
		description="Permissive team template. All capabilities allowed for all roles. Overridable at agent level.",
		overridable=1,
		template_map=template_map,
	)
	_seed_team_template(
		title="Standard",
		description="Balanced team template with role-appropriate permissions. Not overridable.",
		overridable=0,
		template_map=template_map,
	)


def _seed_team_template(
	title: str,
	description: str,
	overridable: int,
	template_map: dict[str, str],
) -> None:
	existing = frappe.db.get_value(
		"Registry",
		{"title": title, "item_type": "Team Template"},
		"ref_name",
	)
	if existing:
		ext = frappe.get_doc("Registry Team Template", existing)
		ext.overridable = overridable
		ext.set("role_configs", [])
		for role_title, role_ext_name in template_map.items():
			ext.append("role_configs", {
				"role": role_ext_name,
				"min_agents": 1,
				"max_agents": 1,
			})
		ext.save(ignore_permissions=True)
		return

	reg = frappe.new_doc("Registry")
	reg.title = title
	reg.item_type = "Team Template"
	reg.description = description
	reg.trust_status = "approved"
	reg.author = "Sena"
	reg.insert(ignore_permissions=True)

	ext = frappe.get_doc("Registry Team Template", reg.ref_name)
	ext.overridable = overridable
	for role_title, role_ext_name in template_map.items():
		ext.append("role_configs", {
			"role": role_ext_name,
			"min_agents": 1,
			"max_agents": 1,
		})
	ext.save(ignore_permissions=True)

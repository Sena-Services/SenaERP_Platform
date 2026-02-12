# Copyright (c) 2025, Sena and contributors
# For license information, please see license.txt

"""Seed sample registry items for development/demo."""

from __future__ import annotations

import json

import frappe


SEED_ITEMS = [
    # --- Agents ---
    {
        "item_type": "Agents",
        "title": "Customer Support Agent",
        "description": "AI agent for handling customer queries and tickets",
        "category": "Support",
        "dotmatrix_avatar": "heart",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["support", "customer", "tickets"]),
        "payload": json.dumps({
            "agent_name": "Customer Support Agent",
            "role_title": "Support Specialist",
            "department": "Support",
            "tools": ["frappe_get_list", "frappe_get_doc", "send_dm"],
        }),
    },
    {
        "item_type": "Agents",
        "title": "Data Analyst",
        "description": "Analyzes data, generates reports and insights",
        "category": "Analytics",
        "dotmatrix_avatar": "data",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["analytics", "reports", "data"]),
        "payload": json.dumps({
            "agent_name": "Data Analyst",
            "role_title": "Data Analyst",
            "department": "Data",
            "tools": ["frappe_get_list", "frappe_get_doc", "run_script"],
        }),
    },
    {
        "item_type": "Agents",
        "title": "Security Monitor",
        "description": "Monitors systems for security threats",
        "category": "Security",
        "dotmatrix_avatar": "security",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["security", "monitoring", "alerts"]),
        "payload": json.dumps({
            "agent_name": "Security Monitor",
            "role_title": "Security Analyst",
            "department": "Engineering",
            "tools": ["frappe_get_list", "web_search"],
        }),
    },
    {
        "item_type": "Agents",
        "title": "Code Reviewer",
        "description": "Reviews pull requests and suggests improvements",
        "category": "Development",
        "dotmatrix_avatar": "scholar",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["code-review", "quality", "pull-requests"]),
        "payload": json.dumps({
            "agent_name": "Code Reviewer",
            "role_title": "Senior Reviewer",
            "department": "Engineering",
            "tools": ["frappe_get_doc", "web_search", "run_script"],
        }),
    },
    # --- Teams ---
    {
        "item_type": "Teams",
        "title": "Accounts Team",
        "description": "Full accounting team with AP, AR, and reconciliation",
        "category": "Finance",
        "dotmatrix_avatar": "boss",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["finance", "accounting", "invoices"]),
        "payload": json.dumps({
            "team_name": "Accounts Team",
            "workers": ["AP Clerk", "AR Clerk", "Recon Agent"],
        }),
    },
    {
        "item_type": "Teams",
        "title": "HR Team",
        "description": "Recruitment, onboarding, and employee management",
        "category": "HR",
        "dotmatrix_avatar": "comm",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["hr", "recruitment", "onboarding"]),
        "payload": json.dumps({
            "team_name": "HR Team",
            "workers": ["Recruiter", "Onboarding Specialist"],
        }),
    },
    {
        "item_type": "Teams",
        "title": "DevOps Team",
        "description": "Infrastructure, CI/CD pipelines, and deployment automation",
        "category": "Engineering",
        "dotmatrix_avatar": "gear",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["devops", "infrastructure", "ci-cd"]),
        "payload": json.dumps({
            "team_name": "DevOps Team",
            "workers": ["Infra Manager", "CI/CD Engineer", "Monitoring Agent"],
        }),
    },
    {
        "item_type": "Teams",
        "title": "Content Team",
        "description": "Content creation, editing, and publishing workflow",
        "category": "Marketing",
        "dotmatrix_avatar": "comm",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["content", "writing", "publishing"]),
        "payload": json.dumps({
            "team_name": "Content Team",
            "workers": ["Writer", "Editor", "SEO Specialist"],
        }),
    },
    # --- Tools ---
    {
        "item_type": "Tools",
        "title": "Web Search",
        "description": "Search the web using DuckDuckGo",
        "category": "Utility",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["search", "web", "duckduckgo"]),
        "payload": json.dumps({
            "tool_name": "web_search",
            "module": "sena_agents_backend.tools.builtin.web_search",
        }),
    },
    {
        "item_type": "Tools",
        "title": "Frappe CRUD",
        "description": "Create, read, update, delete Frappe documents",
        "category": "Development",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["frappe", "crud", "documents"]),
        "payload": json.dumps({
            "tool_name": "frappe_crud",
            "module": "sena_agents_backend.tools.builtin.frappe_crud",
        }),
    },
    {
        "item_type": "Tools",
        "title": "Browser Automation",
        "description": "Control a browser with Playwright",
        "category": "Automation",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["browser", "playwright", "automation"]),
        "payload": json.dumps({
            "tool_name": "browser_automation",
            "module": "sena_agents_backend.tools.builtin.browser",
        }),
    },
    {
        "item_type": "Tools",
        "title": "Slack Notifier",
        "description": "Send messages and notifications to Slack channels",
        "category": "Communication",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["slack", "notifications", "messaging"]),
        "payload": json.dumps({
            "tool_name": "slack_notifier",
            "module": "sena_agents_backend.tools.builtin.slack",
        }),
    },
    # --- UI ---
    {
        "item_type": "UI",
        "title": "Dashboard Template",
        "description": "Pre-built analytics dashboard layout",
        "category": "Templates",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["dashboard", "analytics", "template"]),
        "payload": json.dumps({
            "template_type": "dashboard",
            "layout": "wide",
        }),
    },
    {
        "item_type": "UI",
        "title": "Form Builder",
        "description": "Drag-and-drop form creation interface",
        "category": "Templates",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["form", "builder", "drag-drop"]),
        "payload": json.dumps({
            "template_type": "form_builder",
            "layout": "default",
        }),
    },
    {
        "item_type": "UI",
        "title": "Chat Widget",
        "description": "Embeddable chat interface for agent conversations",
        "category": "Components",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["chat", "widget", "embeddable"]),
        "payload": json.dumps({
            "template_type": "chat_widget",
            "layout": "compact",
        }),
    },
    {
        "item_type": "UI",
        "title": "Data Table",
        "description": "Sortable, filterable data table with pagination",
        "category": "Components",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["table", "data", "pagination"]),
        "payload": json.dumps({
            "template_type": "data_table",
            "layout": "full-width",
        }),
    },
    # --- Models ---
    {
        "item_type": "Models",
        "title": "GPT-4o",
        "description": "OpenAI GPT-4o multimodal model",
        "category": "LLM",
        "dotmatrix_avatar": "data",
        "author": "OpenAI",
        "version": "2024-08",
        "tags": json.dumps(["openai", "gpt", "multimodal"]),
        "payload": json.dumps({
            "provider": "openai",
            "model_id": "gpt-4o",
            "capabilities": ["text", "vision", "function_calling"],
        }),
    },
    {
        "item_type": "Models",
        "title": "Claude Sonnet",
        "description": "Anthropic Claude Sonnet balanced model",
        "category": "LLM",
        "dotmatrix_avatar": "data",
        "author": "Anthropic",
        "version": "2024-10",
        "tags": json.dumps(["anthropic", "claude", "sonnet"]),
        "payload": json.dumps({
            "provider": "anthropic",
            "model_id": "claude-sonnet-4-5-20250929",
            "capabilities": ["text", "vision", "function_calling"],
        }),
    },
    {
        "item_type": "Models",
        "title": "Gemini Flash",
        "description": "Google Gemini Flash fast inference model",
        "category": "LLM",
        "dotmatrix_avatar": "data",
        "author": "Google",
        "version": "2.0",
        "tags": json.dumps(["google", "gemini", "flash"]),
        "payload": json.dumps({
            "provider": "google",
            "model_id": "gemini-2.0-flash",
            "capabilities": ["text", "vision", "function_calling"],
        }),
    },
    {
        "item_type": "Models",
        "title": "Llama 3.1 70B",
        "description": "Meta Llama 3.1 open-weight model for self-hosted deployments",
        "category": "LLM",
        "dotmatrix_avatar": "data",
        "author": "Meta",
        "version": "3.1",
        "tags": json.dumps(["meta", "llama", "open-source", "self-hosted"]),
        "payload": json.dumps({
            "provider": "ollama",
            "model_id": "llama3.1:70b",
            "capabilities": ["text", "function_calling"],
        }),
    },
    # --- Logic (formerly Code) ---
    {
        "item_type": "Logic",
        "title": "REST API Scaffold",
        "description": "Boilerplate code for REST API endpoints",
        "category": "Development",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["api", "rest", "boilerplate"]),
        "payload": json.dumps({
            "language": "python",
            "framework": "frappe",
        }),
    },
    {
        "item_type": "Logic",
        "title": "Webhook Handler",
        "description": "Template for processing incoming webhooks",
        "category": "Development",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["webhook", "handler", "template"]),
        "payload": json.dumps({
            "language": "python",
            "framework": "frappe",
        }),
    },
    {
        "item_type": "Logic",
        "title": "Auth Flow",
        "description": "OAuth2 authentication and token refresh logic",
        "category": "Security",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["auth", "oauth", "security", "tokens"]),
        "payload": json.dumps({
            "language": "python",
            "framework": "frappe",
        }),
    },
    {
        "item_type": "Logic",
        "title": "Data Pipeline",
        "description": "ETL pipeline for importing and transforming external data",
        "category": "Data",
        "author": "Sena",
        "version": "1.0",
        "tags": json.dumps(["etl", "pipeline", "import", "transform"]),
        "payload": json.dumps({
            "language": "python",
            "framework": "frappe",
        }),
    },
]


@frappe.whitelist()
def seed_registry_items() -> dict:
    """Create sample registry items if they don't already exist."""
    created = []
    skipped = []

    for item in SEED_ITEMS:
        title = item["title"]

        if frappe.db.exists("Registry Item", {"title": title}):
            skipped.append(title)
            continue

        doc = frappe.get_doc({
            "doctype": "Registry Item",
            "enabled": 1,
            "installed": 0,
            **item,
        })
        doc.insert(ignore_permissions=True)
        created.append(title)

    if created:
        frappe.db.commit()

    return {
        "created": created,
        "skipped": skipped,
        "total_created": len(created),
        "total_skipped": len(skipped),
    }

"""Generate realistic, fully interconnected registry items for Sena v0.1.

Creates a sample company deployment with ~120 registry items where clusters
contain teams, teams contain agents, and agents reference tools, skills,
UIs, logic packs, and roles — all traversable in the registry UI.
"""
import frappe


# ═══════════════════════════════════════════════════════════════════════════════
# FLAT REGISTRY ITEMS  — (item_type, title, description, category, tags)
# ═══════════════════════════════════════════════════════════════════════════════

ITEMS = []

# ── Agent Roles (10) ─────────────────────────────────────────────────────────
ITEMS += [
	("Agent Role", "Default", "General-purpose role with balanced permissions for any team configuration", "General", ["default", "general", "balanced"]),
	("Agent Role", "Communicator", "Handles external communications, announcements, and stakeholder updates", "General", ["communication", "announcements", "external"]),
	("Agent Role", "Orchestrator", "Coordinates and manages other agents within a team", "General", ["coordination", "management", "orchestration"]),
	("Agent Role", "Worker", "Executes assigned tasks within the boundaries set by the orchestrator", "General", ["execution", "tasks", "worker"]),
	("Agent Role", "Analyst", "Analyzes data, generates reports, and provides insights from structured datasets", "General", ["analytics", "data", "reports"]),
	("Agent Role", "Executor", "Performs automated actions and completes assigned tasks autonomously", "General", ["automation", "execution", "tasks"]),
	("Agent Role", "Reviewer", "Checks work output from other agents for quality and accuracy", "General", ["quality", "review", "validation"]),
	("Agent Role", "Dispatcher", "Routes incoming requests and tasks to the most appropriate agents", "General", ["routing", "dispatch", "assignment"]),
	("Agent Role", "Supervisor", "Monitors agent activities, enforces policies, and escalates issues to humans", "General", ["monitoring", "escalation", "oversight"]),
	("Agent Role", "Specialist", "Deep domain expert that handles complex, niche tasks requiring specific knowledge", "General", ["domain", "expert", "specialist"]),
]

# ── Tools (32) ───────────────────────────────────────────────────────────────
ITEMS += [
	# General
	("Tool", "Query Documents", "Query and filter ERPNext documents with natural language conditions", "General", ["documents", "query", "frappe"]),
	("Tool", "Create Document", "Create a new document in any ERPNext DocType with validation", "General", ["documents", "create", "frappe"]),
	("Tool", "Update Document", "Update fields on an existing ERPNext document", "General", ["documents", "update", "frappe"]),
	("Tool", "Run Report", "Execute a report builder query and return formatted results", "General", ["reports", "analytics", "query"]),
	("Tool", "Generate PDF", "Generate a PDF from a print format or HTML template", "General", ["pdf", "print", "documents"]),
	("Tool", "Knowledge Base Search", "Search internal knowledge base articles and documentation", "General", ["knowledge", "search", "documentation"]),
	("Tool", "Web Search", "Search the web using search APIs for external information", "General", ["search", "web", "information"]),
	# Communication
	("Tool", "Send Email", "Send formatted emails via the system email account", "General", ["email", "communication", "notification"]),
	("Tool", "Send Notification", "Create in-app notifications for specific users or roles", "General", ["notification", "alerts", "in-app"]),
	("Tool", "Schedule Reminder", "Schedule a reminder notification for a future date and time", "General", ["reminder", "scheduling", "notification"]),
	# Finance
	("Tool", "Create Invoice", "Generate a sales or purchase invoice with line items and taxes", "Finance", ["invoice", "billing", "accounts"]),
	("Tool", "Process Payment", "Process a payment entry against outstanding invoices", "Finance", ["payment", "processing", "accounts"]),
	("Tool", "Reconcile Bank", "Match bank statement entries with system payment records", "Finance", ["reconciliation", "bank", "matching"]),
	("Tool", "Calculate Tax", "Calculate tax amounts based on jurisdiction and item categories", "Finance", ["tax", "calculation", "compliance"]),
	("Tool", "Aging Analysis", "Generate accounts receivable or payable aging reports", "Finance", ["aging", "receivables", "payables"]),
	("Tool", "Budget Check", "Verify if a proposed expense falls within budget limits", "Finance", ["budget", "limits", "approval"]),
	("Tool", "Process Payroll", "Calculate and process monthly payroll for a department", "Finance", ["payroll", "salary", "processing"]),
	# HR
	("Tool", "Check Leave Balance", "Look up remaining leave balance for an employee", "HR", ["leave", "balance", "employee"]),
	("Tool", "Employee Lookup", "Search for employee records by name, department, or ID", "HR", ["employee", "search", "directory"]),
	("Tool", "Attendance Mark", "Mark attendance for employees with check-in and check-out times", "HR", ["attendance", "check-in", "tracking"]),
	("Tool", "Onboard Employee", "Execute the onboarding checklist for a new employee", "HR", ["onboarding", "new-hire", "checklist"]),
	# Sales
	("Tool", "Create Quotation", "Generate a sales quotation with items, pricing, and terms", "Sales", ["quotation", "pricing", "sales"]),
	("Tool", "Create Sales Order", "Convert a quotation to a confirmed sales order", "Sales", ["sales-order", "confirmation", "sales"]),
	("Tool", "Lead Score", "Score and prioritize sales leads based on engagement and fit", "Sales", ["lead-scoring", "prioritization", "sales"]),
	("Tool", "Pipeline Summary", "Generate a summary of the sales pipeline by stage", "Sales", ["pipeline", "summary", "forecasting"]),
	("Tool", "Customer 360", "Generate a comprehensive customer profile with history", "Sales", ["customer", "profile", "history"]),
	# Support
	("Tool", "Create Ticket", "Create a support ticket with priority classification", "Support", ["ticket", "support", "customer"]),
	("Tool", "Route Ticket", "Route support tickets to agents based on category and skills", "Support", ["routing", "assignment", "support"]),
	("Tool", "Escalate Ticket", "Escalate a ticket to the next tier with context summary", "Support", ["escalation", "support", "priority"]),
	("Tool", "SLA Check", "Check SLA compliance status and time remaining for tickets", "Support", ["sla", "compliance", "timing"]),
	("Tool", "Knowledge Suggest", "Suggest relevant KB articles for a support inquiry", "Support", ["knowledge", "suggestion", "self-service"]),
	# System
	("Tool", "Check System Health", "Run system health checks and report on service status", "System", ["health", "monitoring", "diagnostics"]),
	("Tool", "Log Analyzer", "Search and analyze system error logs for patterns", "System", ["logs", "debugging", "analysis"]),
]

# ── Skills (15) ──────────────────────────────────────────────────────────────
ITEMS += [
	# Identity
	("Skill", "Accountant Identity", "[identity] You are an accounting specialist. You understand double-entry bookkeeping, journal entries, tax compliance, and financial reporting standards.", "Finance", ["accounting", "identity", "finance"]),
	("Skill", "Sales Rep Identity", "[identity] You are a sales representative. You understand customer relationships, deal negotiation, pipeline management, and closing techniques.", "Sales", ["sales", "identity", "customer"]),
	("Skill", "HR Coordinator Identity", "[identity] You are an HR coordinator. You manage employee lifecycle, benefits administration, policy compliance, and workplace culture.", "HR", ["hr", "identity", "employee"]),
	("Skill", "Support Agent Identity", "[identity] You are a customer support agent. You resolve issues empathetically, follow escalation protocols, and maintain high satisfaction scores.", "Support", ["support", "identity", "customer"]),
	("Skill", "Ops Manager Identity", "[identity] You are an operations manager. You oversee supply chain, logistics, vendor relationships, and process efficiency.", "Operations", ["operations", "identity", "logistics"]),
	# Instructions
	("Skill", "Professional Tone", "[instructions] Always communicate in a professional, courteous tone. Avoid slang and excessive informality.", "General", ["tone", "professional", "communication"]),
	("Skill", "Concise Responses", "[instructions] Keep responses brief and actionable. Lead with the answer, then provide supporting details only if needed.", "General", ["concise", "brevity", "clarity"]),
	("Skill", "Safety First", "[instructions] Before executing any destructive action, always confirm with the user. Never delete data without explicit approval.", "General", ["safety", "confirmation", "caution"]),
	("Skill", "Data Privacy", "[instructions] Never expose personally identifiable information in responses. Mask sensitive fields like SSN, bank accounts, and passwords.", "General", ["privacy", "security", "pii"]),
	("Skill", "Human Escalation", "[instructions] Escalate to a human when confidence is below 70%, the request involves money over $10k, or the customer is upset.", "General", ["escalation", "human-in-loop", "safety"]),
	# Operating workflows
	("Skill", "Invoice Processing", "[operating_workflow] When receiving an invoice: validate vendor, match against PO, check for duplicates, verify amounts, route for approval.", "Finance", ["invoice", "processing", "workflow"]),
	("Skill", "Ticket Triage", "[operating_workflow] When a new ticket arrives: classify priority, check for duplicates, assign category, route to queue, send acknowledgment.", "Support", ["triage", "support", "workflow"]),
	("Skill", "Employee Onboarding", "[operating_workflow] New hire: create accounts day 1, schedule orientation day 2, assign buddy day 3, check-in day 5, 30-day review.", "HR", ["onboarding", "employee", "workflow"]),
	# Domain
	("Skill", "Indian GST", "[domain] Indian Goods and Services Tax: CGST, SGST, IGST, HSN codes, e-way bills, and return filing procedures.", "Finance", ["gst", "india", "tax"]),
	("Skill", "GDPR Compliance", "[domain] European data protection: consent management, data subject rights, breach notification, and processing records.", "General", ["gdpr", "privacy", "europe"]),
]

# ── UIs (6) ──────────────────────────────────────────────────────────────────
ITEMS += [
	("UI", "Chat Console", "Minimal chat interface with command palette and keyboard shortcuts for power users", "General", ["chat", "minimal", "keyboard"]),
	("UI", "Split Workspace", "Two-panel layout with chat on the left and document preview on the right", "General", ["split", "preview", "documents"]),
	("UI", "Dashboard View", "Analytics-focused interface with metric cards, charts, and compact chat input", "General", ["dashboard", "metrics", "analytics"]),
	("UI", "Form Assistant", "Embedded sidebar agent that helps users fill out complex DocType forms", "General", ["form", "assistant", "sidebar"]),
	("UI", "Customer Portal", "Self-service portal where customers interact with support agents directly", "Support", ["portal", "customer", "self-service"]),
	("UI", "Terminal Interface", "Command-line style interface for technical users with autocomplete and history", "System", ["terminal", "cli", "technical"]),
]

# ── Logic Packs (6) ─────────────────────────────────────────────────────────
ITEMS += [
	("Logic", "Accounts Logic Pack", "Business logic for chart of accounts, journal entries, trial balance, and period closing", "Finance", ["accounts", "journal", "closing"]),
	("Logic", "Payroll Logic Pack", "Salary calculation rules, tax brackets, deduction formulas, and statutory compliance", "HR", ["payroll", "tax", "deductions"]),
	("Logic", "Pricing Logic Pack", "Dynamic pricing rules, discount tiers, promotional pricing, and margin calculations", "Sales", ["pricing", "discounts", "margins"]),
	("Logic", "Approval Logic Pack", "Multi-level approval workflows with delegation, escalation timeouts, and auto-approval", "General", ["approval", "workflow", "delegation"]),
	("Logic", "Tax Calculation Logic Pack", "Multi-jurisdiction tax rules, exemptions, reverse charge, and category mapping", "Finance", ["tax", "jurisdiction", "exemptions"]),
	("Logic", "SLA Engine Logic Pack", "SLA timer management, business hours calculation, priority escalation, and breach alerting", "Support", ["sla", "timers", "escalation"]),
]

# ── Agents (35) ──────────────────────────────────────────────────────────────
ITEMS += [
	# Finance
	("Agent", "Homer", "Accounts receivable specialist that tracks outstanding invoices, sends payment reminders, and reconciles customer payments", "Finance", ["accounts", "receivable", "invoicing"]),
	("Agent", "Marge", "Accounts payable agent that processes vendor invoices, matches purchase orders, and schedules payment runs", "Finance", ["accounts", "payable", "vendors"]),
	("Agent", "Bart", "Tax compliance agent that calculates GST/VAT, prepares returns, and monitors regulatory changes", "Finance", ["tax", "compliance", "gst"]),
	("Agent", "Lisa", "Financial analyst that generates P&L reports, budget variance analysis, and cash flow forecasts", "Finance", ["analysis", "reporting", "forecasting"]),
	("Agent", "Ned", "Bank reconciliation specialist that matches transactions, identifies discrepancies, and resolves outstanding entries", "Finance", ["reconciliation", "bank", "matching"]),
	("Agent", "Krusty", "Payroll processing agent that calculates salaries, deductions, taxes, and generates pay slips", "Finance", ["payroll", "salary", "deductions"]),
	("Agent", "Lenny", "Budget planning agent that creates departmental budgets, tracks spending, and alerts on overruns", "Finance", ["budget", "planning", "tracking"]),
	("Agent", "Carl", "Internal audit agent that gathers documentation, verifies transactions, and prepares working papers", "Finance", ["audit", "preparation", "documentation"]),
	# HR
	("Agent", "Skinner", "Recruitment agent that screens resumes, schedules interviews, and coordinates the hiring pipeline", "HR", ["recruitment", "screening", "hiring"]),
	("Agent", "Otto", "Onboarding coordinator that sets up new hires with accounts, equipment, orientations, and buddies", "HR", ["onboarding", "new-hire", "setup"]),
	("Agent", "Hibbert", "Benefits administration agent that manages health insurance, retirement plans, and wellness programs", "HR", ["benefits", "insurance", "wellness"]),
	("Agent", "Milhouse", "Leave management agent that processes leave requests, checks balances, and handles approvals", "HR", ["leave", "requests", "approval"]),
	("Agent", "Nelson", "Attendance tracker that monitors check-ins, flags anomalies, calculates overtime, and generates reports", "HR", ["attendance", "overtime", "tracking"]),
	("Agent", "Lovejoy", "Performance management agent that tracks OKRs, facilitates review cycles, and identifies high performers", "HR", ["performance", "okrs", "reviews"]),
	# Sales
	("Agent", "Gil", "Cold outreach agent that generates personalized prospecting emails based on company research", "Sales", ["prospecting", "outreach", "cold-email"]),
	("Agent", "Troy McClure", "Product demo agent that prepares customized demonstrations, handles objections, and sends proposals", "Sales", ["demos", "presentations", "proposals"]),
	("Agent", "Itchy", "Lead qualification agent that scores inbound leads and routes to appropriate sales reps", "Sales", ["leads", "qualification", "scoring"]),
	("Agent", "Scratchy", "Deal tracking agent that monitors pipeline stages, calculates win probability, and alerts on stalled deals", "Sales", ["pipeline", "deals", "tracking"]),
	("Agent", "Patty", "Customer retention agent that identifies churn signals and triggers win-back campaigns", "Sales", ["retention", "churn", "loyalty"]),
	("Agent", "Selma", "Upsell recommendation agent that analyzes purchase history and suggests complementary products", "Sales", ["upsell", "cross-sell", "recommendations"]),
	# Support
	("Agent", "Barney", "First response agent that greets customers, classifies issues, and resolves common problems", "Support", ["first-response", "classification", "resolution"]),
	("Agent", "Lenny-Support", "Technical support specialist that troubleshoots product issues and escalates bugs", "Support", ["technical", "troubleshooting", "bugs"]),
	("Agent", "Carl-Support", "Billing support agent that resolves invoice disputes, processes refunds, and explains charges", "Support", ["billing", "refunds", "disputes"]),
	("Agent", "Agnes", "Customer feedback analyst that aggregates NPS scores, categorizes complaints, and finds patterns", "Support", ["feedback", "nps", "analysis"]),
	("Agent", "Cookie Kwan", "Customer onboarding specialist that guides new customers through setup and configuration", "Support", ["onboarding", "customer", "training"]),
	# Operations
	("Agent", "Kirk", "Logistics coordinator that tracks shipments, optimizes routes, and manages carriers", "Operations", ["logistics", "shipping", "carriers"]),
	("Agent", "Luann", "Procurement specialist that sources vendors, compares quotations, and manages purchase orders", "Operations", ["procurement", "sourcing", "purchasing"]),
	("Agent", "Frank Grimes", "Process auditor that evaluates operational procedures and recommends improvements", "Operations", ["audit", "process", "efficiency"]),
	# System
	("Agent", "Database Admin", "Database monitoring agent that tracks query performance, manages backups, and alerts on anomalies", "System", ["database", "performance", "monitoring"]),
	("Agent", "Security Guard", "Security monitoring agent that detects suspicious activity and enforces access policies", "System", ["security", "access", "monitoring"]),
	("Agent", "Log Watcher", "System log analyst that parses error logs, identifies recurring issues, and creates incident reports", "System", ["logs", "errors", "analysis"]),
	# General
	("Agent", "Meeting Secretary", "Meeting assistant that takes notes, extracts action items, sends summaries, and tracks follow-ups", "General", ["meetings", "notes", "action-items"]),
	("Agent", "Report Builder", "Custom report generator that queries data, creates visualizations, and distributes reports", "General", ["reports", "visualization", "analytics"]),
]

# ── Team Types (7) ───────────────────────────────────────────────────────────
ITEMS += [
	("Team Type", "Standard", "Balanced team type with role-appropriate permissions. Not overridable.", "General", ["standard", "balanced", "default"]),
	("Team Type", "Default", "Permissive team type. All capabilities allowed for all roles. Overridable at agent level.", "General", ["default", "permissive", "open"]),
	("Team Type", "Hub and Spoke", "Central orchestrator coordinates peripheral worker agents with restricted cross-talk", "General", ["centralized", "coordination"]),
	("Team Type", "Assembly Line", "Sequential pipeline where each agent handles one stage and passes to the next", "General", ["pipeline", "sequential", "processing"]),
	("Team Type", "Escalation Ladder", "Tiered team where issues escalate through progressively more capable agents", "Support", ["escalation", "tiered", "progressive"]),
	("Team Type", "Review Board", "Panel of reviewers that collectively evaluate and approve work products", "General", ["review", "approval", "consensus"]),
	("Team Type", "Autonomous Squad", "Fully autonomous team where all agents communicate, spawn, and act independently", "General", ["autonomous", "self-organizing"]),
]

# ── Teams (12) ───────────────────────────────────────────────────────────────
ITEMS += [
	("Team", "Accounts Receivable Team", "Tracks outstanding invoices, sends payment reminders, and reconciles incoming payments", "Finance", ["accounts", "receivable", "collections"]),
	("Team", "Accounts Payable Team", "Processes vendor invoices, matches purchase orders, and executes payment runs", "Finance", ["accounts", "payable", "payments"]),
	("Team", "Tax & Reporting Team", "Handles tax calculations, compliance filing, financial statements, and budget tracking", "Finance", ["tax", "reporting", "compliance"]),
	("Team", "Payroll Team", "Calculates salaries, processes deductions, and generates monthly payslips", "Finance", ["payroll", "salary", "processing"]),
	("Team", "Recruitment Team", "Sources candidates, screens applications, schedules interviews, and coordinates offers", "HR", ["recruitment", "hiring", "candidates"]),
	("Team", "People Operations Team", "Manages employee records, benefits, leave, attendance, and performance reviews", "HR", ["people-ops", "benefits", "policies"]),
	("Team", "Sales Development Team", "Generates leads through outbound outreach, qualifies inbound, and books demos", "Sales", ["sdr", "prospecting", "qualification"]),
	("Team", "Account Management Team", "Manages existing customer relationships, renewals, and expansion revenue", "Sales", ["accounts", "renewal", "expansion"]),
	("Team", "Tier 1 Support Team", "Front-line support handling initial contact, triage, and escalation", "Support", ["tier-1", "front-line", "triage"]),
	("Team", "Billing Support Team", "Resolves invoice disputes, processes refunds, and explains billing", "Support", ["billing", "refunds", "disputes"]),
	("Team", "Supply Chain Team", "Coordinates logistics, procurement, and vendor management", "Operations", ["supply-chain", "logistics", "procurement"]),
	("Team", "Platform Team", "Maintains infrastructure, monitors systems, and manages security operations", "System", ["platform", "infrastructure", "security"]),
]

# ── Clusters (5) ─────────────────────────────────────────────────────────────
ITEMS += [
	("Cluster", "Finance Department", "Complete financial operations with AR/AP, tax compliance, reporting, and payroll", "Finance", ["finance", "department", "complete"]),
	("Cluster", "HR Operations", "Full HR lifecycle covering recruitment, onboarding, benefits, attendance, and performance", "HR", ["hr", "lifecycle", "complete"]),
	("Cluster", "Sales Engine", "End-to-end sales from lead generation through deal closure and account management", "Sales", ["sales", "pipeline", "complete"]),
	("Cluster", "Customer Success Hub", "Customer-facing operations with tiered support, billing help, and feedback analysis", "Support", ["support", "customer", "complete"]),
	("Cluster", "IT & Operations", "Infrastructure, security, logistics, and supply chain management", "Operations", ["operations", "it", "infrastructure"]),
]


# ═══════════════════════════════════════════════════════════════════════════════
# EXTENSION WIRING CONFIGS
# ═══════════════════════════════════════════════════════════════════════════════

_TOOL_EXT = {
	"Query Documents": {"tool_name": "query_documents", "tool_class": "system"},
	"Create Document": {"tool_name": "create_document", "tool_class": "system"},
	"Update Document": {"tool_name": "update_document", "tool_class": "system"},
	"Run Report": {"tool_name": "run_report", "tool_class": "system"},
	"Generate PDF": {"tool_name": "generate_pdf", "tool_class": "system"},
	"Knowledge Base Search": {"tool_name": "knowledge_base_search", "tool_class": "system"},
	"Web Search": {"tool_name": "web_search", "tool_class": "external"},
	"Send Email": {"tool_name": "send_email", "tool_class": "system"},
	"Send Notification": {"tool_name": "send_notification", "tool_class": "system"},
	"Schedule Reminder": {"tool_name": "schedule_reminder", "tool_class": "system"},
	"Create Invoice": {"tool_name": "create_invoice", "tool_class": "system"},
	"Process Payment": {"tool_name": "process_payment", "tool_class": "system"},
	"Reconcile Bank": {"tool_name": "reconcile_bank", "tool_class": "system"},
	"Calculate Tax": {"tool_name": "calculate_tax", "tool_class": "system"},
	"Aging Analysis": {"tool_name": "aging_analysis", "tool_class": "system"},
	"Budget Check": {"tool_name": "budget_check", "tool_class": "system"},
	"Process Payroll": {"tool_name": "process_payroll", "tool_class": "system"},
	"Check Leave Balance": {"tool_name": "check_leave_balance", "tool_class": "system"},
	"Employee Lookup": {"tool_name": "employee_lookup", "tool_class": "system"},
	"Attendance Mark": {"tool_name": "attendance_mark", "tool_class": "system"},
	"Onboard Employee": {"tool_name": "onboard_employee", "tool_class": "system"},
	"Create Quotation": {"tool_name": "create_quotation", "tool_class": "system"},
	"Create Sales Order": {"tool_name": "create_sales_order", "tool_class": "system"},
	"Lead Score": {"tool_name": "lead_score", "tool_class": "system"},
	"Pipeline Summary": {"tool_name": "pipeline_summary", "tool_class": "system"},
	"Customer 360": {"tool_name": "customer_360", "tool_class": "system"},
	"Create Ticket": {"tool_name": "create_ticket", "tool_class": "system"},
	"Route Ticket": {"tool_name": "route_ticket", "tool_class": "system"},
	"Escalate Ticket": {"tool_name": "escalate_ticket", "tool_class": "system"},
	"SLA Check": {"tool_name": "sla_check", "tool_class": "system"},
	"Knowledge Suggest": {"tool_name": "knowledge_suggest", "tool_class": "system"},
	"Check System Health": {"tool_name": "check_system_health", "tool_class": "system"},
	"Log Analyzer": {"tool_name": "log_analyzer", "tool_class": "system"},
}

_SKILL_EXT = {
	"Accountant Identity": {"skill_type": "identity"},
	"Sales Rep Identity": {"skill_type": "identity"},
	"HR Coordinator Identity": {"skill_type": "identity"},
	"Support Agent Identity": {"skill_type": "identity"},
	"Ops Manager Identity": {"skill_type": "identity"},
	"Professional Tone": {"skill_type": "instructions"},
	"Concise Responses": {"skill_type": "instructions"},
	"Safety First": {"skill_type": "instructions"},
	"Data Privacy": {"skill_type": "instructions"},
	"Human Escalation": {"skill_type": "instructions"},
	"Invoice Processing": {"skill_type": "operating_workflow"},
	"Ticket Triage": {"skill_type": "operating_workflow"},
	"Employee Onboarding": {"skill_type": "operating_workflow"},
	"Indian GST": {"skill_type": "domain"},
	"GDPR Compliance": {"skill_type": "domain"},
}

_UI_EXT = {
	"Chat Console": {"ui_mode": "chat", "framework": "vue"},
	"Split Workspace": {"ui_mode": "chat", "framework": "vue"},
	"Dashboard View": {"ui_mode": "chat", "framework": "vue"},
	"Form Assistant": {"ui_mode": "chat", "framework": "vue"},
	"Customer Portal": {"ui_mode": "iframe", "framework": "vue"},
	"Terminal Interface": {"ui_mode": "chat", "framework": "vanilla"},
}

_LOGIC_EXT = {
	"Accounts Logic Pack": {"module_name": "accounts_logic", "tier": "sr"},
	"Payroll Logic Pack": {"module_name": "payroll_logic", "tier": "sr"},
	"Pricing Logic Pack": {"module_name": "pricing_logic", "tier": "mid"},
	"Approval Logic Pack": {"module_name": "approval_logic", "tier": "mid"},
	"Tax Calculation Logic Pack": {"module_name": "tax_logic", "tier": "sr"},
	"SLA Engine Logic Pack": {"module_name": "sla_logic", "tier": "mid"},
}

# Agent wiring: role, ui, logic, model, tools[], skills[]
_AGENT_EXT = {
	# ── Finance ──
	"Homer": {
		"role": "Executor", "ui": "Chat Console", "logic": "Accounts Logic Pack",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Create Invoice", "Process Payment", "Send Email", "Aging Analysis"],
		"skills": ["Accountant Identity", "Professional Tone", "Invoice Processing"],
	},
	"Marge": {
		"role": "Executor", "ui": "Chat Console", "logic": "Accounts Logic Pack",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Create Invoice", "Process Payment", "Send Email", "Budget Check"],
		"skills": ["Accountant Identity", "Professional Tone", "Invoice Processing"],
	},
	"Bart": {
		"role": "Specialist", "logic": "Tax Calculation Logic Pack",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Calculate Tax", "Run Report", "Generate PDF"],
		"skills": ["Accountant Identity", "Indian GST", "Concise Responses"],
	},
	"Lisa": {
		"role": "Analyst", "ui": "Dashboard View", "logic": "Accounts Logic Pack",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Run Report", "Generate PDF", "Aging Analysis", "Budget Check"],
		"skills": ["Accountant Identity", "Concise Responses"],
	},
	"Ned": {
		"role": "Analyst", "ui": "Split Workspace", "logic": "Accounts Logic Pack",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Reconcile Bank", "Run Report"],
		"skills": ["Accountant Identity", "Safety First"],
	},
	"Krusty": {
		"role": "Executor", "logic": "Payroll Logic Pack",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Process Payroll", "Generate PDF", "Send Email", "Calculate Tax"],
		"skills": ["Accountant Identity", "Data Privacy", "Safety First"],
	},
	"Lenny": {
		"role": "Analyst", "ui": "Dashboard View",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Budget Check", "Run Report", "Send Notification"],
		"skills": ["Accountant Identity", "Concise Responses"],
	},
	"Carl": {
		"role": "Reviewer", "logic": "Accounts Logic Pack",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Run Report", "Generate PDF", "Knowledge Base Search"],
		"skills": ["Accountant Identity", "Safety First", "Data Privacy"],
	},
	# ── HR ──
	"Skinner": {
		"role": "Dispatcher", "ui": "Split Workspace",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Employee Lookup", "Send Email", "Schedule Reminder"],
		"skills": ["HR Coordinator Identity", "Professional Tone"],
	},
	"Otto": {
		"role": "Executor",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Create Document", "Onboard Employee", "Send Email", "Send Notification", "Schedule Reminder"],
		"skills": ["HR Coordinator Identity", "Employee Onboarding", "Professional Tone"],
	},
	"Hibbert": {
		"role": "Specialist", "ui": "Form Assistant",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Update Document", "Employee Lookup", "Send Email"],
		"skills": ["HR Coordinator Identity", "Data Privacy"],
	},
	"Milhouse": {
		"role": "Executor",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Check Leave Balance", "Update Document", "Send Notification", "Employee Lookup"],
		"skills": ["HR Coordinator Identity", "Concise Responses"],
	},
	"Nelson": {
		"role": "Analyst",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Attendance Mark", "Query Documents", "Run Report", "Send Notification"],
		"skills": ["HR Coordinator Identity", "Concise Responses"],
	},
	"Lovejoy": {
		"role": "Reviewer",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Run Report", "Send Email", "Generate PDF"],
		"skills": ["HR Coordinator Identity", "Professional Tone"],
	},
	# ── Sales ──
	"Gil": {
		"role": "Executor", "ui": "Split Workspace",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Web Search", "Customer 360", "Send Email", "Lead Score"],
		"skills": ["Sales Rep Identity", "Professional Tone"],
	},
	"Troy McClure": {
		"role": "Specialist", "ui": "Split Workspace", "logic": "Pricing Logic Pack",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Create Quotation", "Customer 360", "Generate PDF", "Send Email"],
		"skills": ["Sales Rep Identity", "Professional Tone", "Concise Responses"],
	},
	"Itchy": {
		"role": "Dispatcher",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Lead Score", "Customer 360", "Query Documents", "Send Notification"],
		"skills": ["Sales Rep Identity", "Concise Responses"],
	},
	"Scratchy": {
		"role": "Analyst", "ui": "Dashboard View",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Pipeline Summary", "Query Documents", "Run Report", "Send Notification"],
		"skills": ["Sales Rep Identity", "Concise Responses"],
	},
	"Patty": {
		"role": "Analyst",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Customer 360", "Query Documents", "Send Email", "Run Report"],
		"skills": ["Sales Rep Identity", "Human Escalation"],
	},
	"Selma": {
		"role": "Specialist", "logic": "Pricing Logic Pack",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Customer 360", "Create Quotation", "Query Documents"],
		"skills": ["Sales Rep Identity", "Concise Responses"],
	},
	# ── Support ──
	"Barney": {
		"role": "Dispatcher", "ui": "Customer Portal", "logic": "SLA Engine Logic Pack",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Create Ticket", "Route Ticket", "Knowledge Suggest", "SLA Check"],
		"skills": ["Support Agent Identity", "Professional Tone", "Ticket Triage"],
	},
	"Lenny-Support": {
		"role": "Specialist", "ui": "Split Workspace", "logic": "SLA Engine Logic Pack",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Knowledge Base Search", "Escalate Ticket", "SLA Check", "Log Analyzer"],
		"skills": ["Support Agent Identity", "Human Escalation", "Concise Responses"],
	},
	"Carl-Support": {
		"role": "Specialist", "ui": "Customer Portal", "logic": "Accounts Logic Pack",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Create Invoice", "Process Payment", "SLA Check"],
		"skills": ["Support Agent Identity", "Accountant Identity", "Human Escalation"],
	},
	"Agnes": {
		"role": "Analyst",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Run Report", "Generate PDF"],
		"skills": ["Support Agent Identity", "Concise Responses"],
	},
	"Cookie Kwan": {
		"role": "Executor", "ui": "Customer Portal",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Create Document", "Send Email", "Knowledge Suggest", "Schedule Reminder"],
		"skills": ["Support Agent Identity", "Professional Tone"],
	},
	# ── Operations ──
	"Kirk": {
		"role": "Executor",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Update Document", "Send Notification"],
		"skills": ["Ops Manager Identity", "Concise Responses"],
	},
	"Luann": {
		"role": "Executor", "ui": "Form Assistant",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Create Document", "Send Email", "Budget Check"],
		"skills": ["Ops Manager Identity", "Professional Tone", "Safety First"],
	},
	"Frank Grimes": {
		"role": "Reviewer",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Run Report", "Generate PDF", "Knowledge Base Search"],
		"skills": ["Ops Manager Identity", "Concise Responses"],
	},
	# ── System ──
	"Database Admin": {
		"role": "Specialist", "ui": "Terminal Interface",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Check System Health", "Log Analyzer", "Send Notification"],
		"skills": ["Safety First", "Concise Responses"],
	},
	"Security Guard": {
		"role": "Supervisor", "ui": "Terminal Interface",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Check System Health", "Log Analyzer", "Send Notification", "Query Documents"],
		"skills": ["Safety First", "Data Privacy", "GDPR Compliance"],
	},
	"Log Watcher": {
		"role": "Analyst", "ui": "Terminal Interface",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Log Analyzer", "Check System Health", "Send Notification", "Create Document"],
		"skills": ["Concise Responses"],
	},
	# ── General ──
	"Meeting Secretary": {
		"role": "Executor", "ui": "Chat Console",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Create Document", "Send Email", "Schedule Reminder", "Send Notification"],
		"skills": ["Professional Tone", "Concise Responses"],
	},
	"Report Builder": {
		"role": "Analyst", "ui": "Dashboard View",
		"model": "claude-sonnet-4-5-20250929",
		"tools": ["Query Documents", "Run Report", "Generate PDF", "Send Email"],
		"skills": ["Concise Responses"],
	},
}

# ── Permission profiles for role configs ─────────────────────────────────────
_PERM = {
	"orchestrator": {
		"can_post_townhall": "allow", "can_read_townhall": "allow",
		"can_mention_individuals": "allow", "can_mention_all": "allow",
		"woken_by_direct_mention": "allow", "woken_by_all_mention": "allow",
		"woken_by_any_townhall": "allow",
		"can_send_text": "allow", "can_receive_text": "allow", "woken_by_text": "allow",
		"can_spawn": "allow", "can_kill_spawns": "allow", "spawnable": "deny",
		"can_inject": "allow", "injectable": "deny",
		"can_inline": "allow", "inlineable": "deny",
		"can_create_tasks": "allow", "can_read_tasks": "allow",
		"can_update_tasks": "allow", "can_cancel_tasks": "allow",
		"can_read_documents": "allow", "can_create_documents": "allow",
		"can_update_documents": "allow", "can_delete_documents": "approval_required",
		"can_mass_update": "approval_required", "can_mass_delete": "deny",
		"can_run_doc_method": "allow",
		"single_user_instance": "deny",
		"visible_in_agent_list": "allow", "ui_mode": "chat",
	},
	"worker": {
		"can_post_townhall": "deny", "can_read_townhall": "allow",
		"can_mention_individuals": "deny", "can_mention_all": "deny",
		"woken_by_direct_mention": "allow", "woken_by_all_mention": "allow",
		"woken_by_any_townhall": "deny",
		"can_send_text": "deny", "can_receive_text": "allow", "woken_by_text": "allow",
		"can_spawn": "deny", "can_kill_spawns": "deny", "spawnable": "allow",
		"can_inject": "deny", "injectable": "allow",
		"can_inline": "deny", "inlineable": "allow",
		"can_create_tasks": "deny", "can_read_tasks": "allow",
		"can_update_tasks": "allow", "can_cancel_tasks": "deny",
		"can_read_documents": "allow", "can_create_documents": "allow",
		"can_update_documents": "allow", "can_delete_documents": "deny",
		"can_mass_update": "deny", "can_mass_delete": "deny",
		"can_run_doc_method": "allow",
		"single_user_instance": "deny",
		"visible_in_agent_list": "allow", "ui_mode": "chat",
	},
	"specialist": {
		"can_post_townhall": "allow", "can_read_townhall": "allow",
		"can_mention_individuals": "allow", "can_mention_all": "deny",
		"woken_by_direct_mention": "allow", "woken_by_all_mention": "allow",
		"woken_by_any_townhall": "deny",
		"can_send_text": "allow", "can_receive_text": "allow", "woken_by_text": "allow",
		"can_spawn": "deny", "can_kill_spawns": "deny", "spawnable": "allow",
		"can_inject": "deny", "injectable": "allow",
		"can_inline": "allow", "inlineable": "allow",
		"can_create_tasks": "allow", "can_read_tasks": "allow",
		"can_update_tasks": "allow", "can_cancel_tasks": "deny",
		"can_read_documents": "allow", "can_create_documents": "allow",
		"can_update_documents": "allow", "can_delete_documents": "deny",
		"can_mass_update": "deny", "can_mass_delete": "deny",
		"can_run_doc_method": "allow",
		"single_user_instance": "deny",
		"visible_in_agent_list": "allow", "ui_mode": "chat",
	},
	"supervisor": {
		"can_post_townhall": "allow", "can_read_townhall": "allow",
		"can_mention_individuals": "allow", "can_mention_all": "allow",
		"woken_by_direct_mention": "allow", "woken_by_all_mention": "allow",
		"woken_by_any_townhall": "allow",
		"can_send_text": "allow", "can_receive_text": "allow", "woken_by_text": "allow",
		"can_spawn": "allow", "can_kill_spawns": "allow", "spawnable": "deny",
		"can_inject": "allow", "injectable": "deny",
		"can_inline": "allow", "inlineable": "deny",
		"can_create_tasks": "allow", "can_read_tasks": "allow",
		"can_update_tasks": "allow", "can_cancel_tasks": "allow",
		"can_read_documents": "allow", "can_create_documents": "allow",
		"can_update_documents": "allow", "can_delete_documents": "allow",
		"can_mass_update": "approval_required", "can_mass_delete": "approval_required",
		"can_run_doc_method": "allow",
		"single_user_instance": "deny",
		"visible_in_agent_list": "allow", "ui_mode": "chat",
	},
	"reviewer": {
		"can_post_townhall": "allow", "can_read_townhall": "allow",
		"can_mention_individuals": "allow", "can_mention_all": "deny",
		"woken_by_direct_mention": "allow", "woken_by_all_mention": "allow",
		"woken_by_any_townhall": "allow",
		"can_send_text": "allow", "can_receive_text": "allow", "woken_by_text": "allow",
		"can_spawn": "deny", "can_kill_spawns": "deny", "spawnable": "deny",
		"can_inject": "deny", "injectable": "deny",
		"can_inline": "deny", "inlineable": "deny",
		"can_create_tasks": "allow", "can_read_tasks": "allow",
		"can_update_tasks": "allow", "can_cancel_tasks": "deny",
		"can_read_documents": "allow", "can_create_documents": "deny",
		"can_update_documents": "deny", "can_delete_documents": "deny",
		"can_mass_update": "deny", "can_mass_delete": "deny",
		"can_run_doc_method": "deny",
		"single_user_instance": "deny",
		"visible_in_agent_list": "allow", "ui_mode": "chat",
	},
	"autonomous": {
		"can_post_townhall": "allow", "can_read_townhall": "allow",
		"can_mention_individuals": "allow", "can_mention_all": "allow",
		"woken_by_direct_mention": "allow", "woken_by_all_mention": "allow",
		"woken_by_any_townhall": "allow",
		"can_send_text": "allow", "can_receive_text": "allow", "woken_by_text": "allow",
		"can_spawn": "allow", "can_kill_spawns": "allow", "spawnable": "allow",
		"can_inject": "allow", "injectable": "allow",
		"can_inline": "allow", "inlineable": "allow",
		"can_create_tasks": "allow", "can_read_tasks": "allow",
		"can_update_tasks": "allow", "can_cancel_tasks": "allow",
		"can_read_documents": "allow", "can_create_documents": "allow",
		"can_update_documents": "allow", "can_delete_documents": "allow",
		"can_mass_update": "allow", "can_mass_delete": "approval_required",
		"can_run_doc_method": "allow",
		"single_user_instance": "deny",
		"visible_in_agent_list": "allow", "ui_mode": "chat",
	},
}

# Team Type wiring: roles with permission profiles
_TEAM_TYPE_EXT = {
	"Standard": {
		"overridable": 0,
		"roles": [
			{"role": "Orchestrator", "min": 1, "max": 1, "perms": "orchestrator"},
			{"role": "Communicator", "min": 0, "max": 2, "perms": "specialist"},
			{"role": "Worker", "min": 1, "max": 8, "perms": "worker"},
			{"role": "Default", "min": 0, "max": 5, "perms": "worker"},
		],
	},
	"Default": {
		"overridable": 1,
		"roles": [
			{"role": "Default", "min": 1, "max": 10, "perms": "autonomous"},
		],
	},
	"Hub and Spoke": {
		"overridable": 0,
		"roles": [
			{"role": "Orchestrator", "min": 1, "max": 1, "perms": "orchestrator"},
			{"role": "Worker", "min": 1, "max": 8, "perms": "worker"},
		],
	},
	"Assembly Line": {
		"overridable": 0,
		"roles": [
			{"role": "Orchestrator", "min": 1, "max": 1, "perms": "orchestrator"},
			{"role": "Executor", "min": 2, "max": 10, "perms": "worker"},
		],
	},
	"Escalation Ladder": {
		"overridable": 0,
		"roles": [
			{"role": "Dispatcher", "min": 1, "max": 1, "perms": "orchestrator"},
			{"role": "Executor", "min": 1, "max": 5, "perms": "worker"},
			{"role": "Specialist", "min": 1, "max": 3, "perms": "specialist"},
			{"role": "Supervisor", "min": 1, "max": 1, "perms": "supervisor"},
		],
	},
	"Review Board": {
		"overridable": 0,
		"roles": [
			{"role": "Orchestrator", "min": 1, "max": 1, "perms": "orchestrator"},
			{"role": "Reviewer", "min": 2, "max": 5, "perms": "reviewer"},
		],
	},
	"Autonomous Squad": {
		"overridable": 1,
		"roles": [
			{"role": "Default", "min": 2, "max": 10, "perms": "autonomous"},
		],
	},
}

# Team wiring: team_type + members (agent_title, role_title)
_TEAM_EXT = {
	"Accounts Receivable Team": {
		"team_type": "Hub and Spoke",
		"members": [("Lisa", "Orchestrator"), ("Homer", "Worker"), ("Ned", "Worker")],
	},
	"Accounts Payable Team": {
		"team_type": "Assembly Line",
		"members": [("Lisa", "Orchestrator"), ("Marge", "Executor"), ("Carl", "Executor")],
	},
	"Tax & Reporting Team": {
		"team_type": "Review Board",
		"members": [("Lenny", "Orchestrator"), ("Bart", "Reviewer"), ("Lisa", "Reviewer"), ("Carl", "Reviewer")],
	},
	"Payroll Team": {
		"team_type": "Hub and Spoke",
		"members": [("Lisa", "Orchestrator"), ("Krusty", "Worker")],
	},
	"Recruitment Team": {
		"team_type": "Hub and Spoke",
		"members": [("Skinner", "Orchestrator"), ("Otto", "Worker")],
	},
	"People Operations Team": {
		"team_type": "Hub and Spoke",
		"members": [("Lovejoy", "Orchestrator"), ("Hibbert", "Worker"), ("Milhouse", "Worker"), ("Nelson", "Worker")],
	},
	"Sales Development Team": {
		"team_type": "Hub and Spoke",
		"members": [("Itchy", "Orchestrator"), ("Gil", "Worker"), ("Troy McClure", "Worker")],
	},
	"Account Management Team": {
		"team_type": "Autonomous Squad",
		"members": [("Scratchy", "Default"), ("Patty", "Default"), ("Selma", "Default")],
	},
	"Tier 1 Support Team": {
		"team_type": "Escalation Ladder",
		"members": [("Barney", "Dispatcher"), ("Cookie Kwan", "Executor"), ("Lenny-Support", "Specialist"), ("Agnes", "Supervisor")],
	},
	"Billing Support Team": {
		"team_type": "Hub and Spoke",
		"members": [("Carl-Support", "Orchestrator"), ("Barney", "Worker")],
	},
	"Supply Chain Team": {
		"team_type": "Hub and Spoke",
		"members": [("Frank Grimes", "Orchestrator"), ("Kirk", "Worker"), ("Luann", "Worker")],
	},
	"Platform Team": {
		"team_type": "Autonomous Squad",
		"members": [("Database Admin", "Default"), ("Security Guard", "Default"), ("Log Watcher", "Default")],
	},
}

# Cluster wiring: team titles
_CLUSTER_EXT = {
	"Finance Department": ["Accounts Receivable Team", "Accounts Payable Team", "Tax & Reporting Team", "Payroll Team"],
	"HR Operations": ["Recruitment Team", "People Operations Team"],
	"Sales Engine": ["Sales Development Team", "Account Management Team"],
	"Customer Success Hub": ["Tier 1 Support Team", "Billing Support Team"],
	"IT & Operations": ["Platform Team", "Supply Chain Team"],
}


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATION LOGIC
# ═══════════════════════════════════════════════════════════════════════════════

def _cleanup_all():
	"""Remove all registry items and extensions."""
	# Child tables first
	for dt in [
		"Registry Tag", "Registry Agent Tool", "Registry Agent Skill",
		"Registry Team Member", "Registry Cluster Team", "Registry Team Type Role Config",
	]:
		frappe.db.sql(f"DELETE FROM `tab{dt}`")

	# Extension tables
	for dt in [
		"Registry Agent", "Registry Team", "Registry Cluster",
		"Registry Team Type", "Registry Agent Role", "Registry UI",
		"Registry Logic", "Registry Skill", "Registry Tool",
	]:
		frappe.db.sql(f"DELETE FROM `tab{dt}`")

	# Registry items
	frappe.db.sql("DELETE FROM `tabRegistry`")
	frappe.db.commit()
	print("Cleaned up all registry data")


def _build_ref_map():
	"""Build (item_type, title) -> ref_name lookup."""
	return {
		(r.item_type, r.title): r.ref_name
		for r in frappe.get_all("Registry", fields=["title", "item_type", "ref_name"])
		if r.ref_name
	}


def _wire_tools(ref_map):
	for title, cfg in _TOOL_EXT.items():
		ext_name = ref_map.get(("Tool", title))
		if not ext_name:
			continue
		frappe.db.set_value("Registry Tool", ext_name, {
			"tool_name": cfg["tool_name"],
			"tool_class": cfg.get("tool_class", "system"),
			"access_default": cfg.get("access_default", "allow"),
		}, update_modified=False)


def _wire_skills(ref_map):
	for title, cfg in _SKILL_EXT.items():
		ext_name = ref_map.get(("Skill", title))
		if not ext_name:
			continue
		# Extract content from the Registry description (strip the [type] prefix)
		reg_name = frappe.db.get_value("Registry Skill", ext_name, "registry")
		desc = frappe.db.get_value("Registry", reg_name, "description") or ""
		content = desc
		bracket_end = desc.find("] ")
		if bracket_end > 0:
			content = desc[bracket_end + 2:]
		frappe.db.set_value("Registry Skill", ext_name, {
			"skill_type": cfg["skill_type"],
			"skill_content": content,
		}, update_modified=False)


def _wire_uis(ref_map):
	for title, cfg in _UI_EXT.items():
		ext_name = ref_map.get(("UI", title))
		if not ext_name:
			continue
		frappe.db.set_value("Registry UI", ext_name, {
			"ui_mode": cfg.get("ui_mode", "chat"),
			"framework": cfg.get("framework", "vue"),
		}, update_modified=False)


def _wire_logic(ref_map):
	for title, cfg in _LOGIC_EXT.items():
		ext_name = ref_map.get(("Logic", title))
		if not ext_name:
			continue
		frappe.db.set_value("Registry Logic", ext_name, {
			"module_name": cfg.get("module_name", ""),
			"tier": cfg.get("tier", "jr"),
		}, update_modified=False)


def _wire_agents(ref_map):
	for title, cfg in _AGENT_EXT.items():
		ext_name = ref_map.get(("Agent", title))
		if not ext_name:
			continue

		doc = frappe.get_doc("Registry Agent", ext_name)

		# Direct links
		if cfg.get("role"):
			role_ext = ref_map.get(("Agent Role", cfg["role"]))
			if role_ext:
				doc.agent_role = role_ext
		if cfg.get("ui"):
			ui_ext = ref_map.get(("UI", cfg["ui"]))
			if ui_ext:
				doc.ui = ui_ext
		if cfg.get("logic"):
			logic_ext = ref_map.get(("Logic", cfg["logic"]))
			if logic_ext:
				doc.logic = logic_ext
		if cfg.get("model"):
			doc.model = cfg["model"]

		# Tools child table
		doc.agent_tools = []
		for tool_title in cfg.get("tools", []):
			tool_ext = ref_map.get(("Tool", tool_title))
			if tool_ext:
				doc.append("agent_tools", {"tool": tool_ext, "enabled": 1})

		# Skills child table
		doc.agent_skills = []
		for skill_title in cfg.get("skills", []):
			skill_ext = ref_map.get(("Skill", skill_title))
			if skill_ext:
				skill_type = _SKILL_EXT.get(skill_title, {}).get("skill_type", "")
				activation = "on-demand" if skill_type in ("domain", "operating_workflow") else "core"
				doc.append("agent_skills", {"skill": skill_ext, "activation": activation, "enabled": 1})

		doc.save(ignore_permissions=True)


def _wire_team_types(ref_map):
	for title, cfg in _TEAM_TYPE_EXT.items():
		ext_name = ref_map.get(("Team Type", title))
		if not ext_name:
			continue

		doc = frappe.get_doc("Registry Team Type", ext_name)
		doc.overridable = cfg.get("overridable", 0)

		doc.role_configs = []
		for role_cfg in cfg.get("roles", []):
			role_ext = ref_map.get(("Agent Role", role_cfg["role"]))
			if not role_ext:
				continue
			row = {
				"role": role_ext,
				"min_agents": role_cfg.get("min", 1),
				"max_agents": role_cfg.get("max", 1),
			}
			row.update(_PERM.get(role_cfg.get("perms", "worker"), {}))
			doc.append("role_configs", row)

		doc.save(ignore_permissions=True)


def _wire_teams(ref_map):
	for title, cfg in _TEAM_EXT.items():
		ext_name = ref_map.get(("Team", title))
		if not ext_name:
			continue

		doc = frappe.get_doc("Registry Team", ext_name)

		# Team type link
		if cfg.get("team_type"):
			tt_ext = ref_map.get(("Team Type", cfg["team_type"]))
			if tt_ext:
				doc.team_type = tt_ext

		# Members
		doc.members = []
		for agent_title, role_title in cfg.get("members", []):
			agent_ext = ref_map.get(("Agent", agent_title))
			role_ext = ref_map.get(("Agent Role", role_title))
			if agent_ext and role_ext:
				doc.append("members", {"agent": agent_ext, "role": role_ext})

		doc.save(ignore_permissions=True)


def _wire_clusters(ref_map):
	for title, team_titles in _CLUSTER_EXT.items():
		ext_name = ref_map.get(("Cluster", title))
		if not ext_name:
			continue

		doc = frappe.get_doc("Registry Cluster", ext_name)
		doc.cluster_teams = []
		for team_title in team_titles:
			team_ext = ref_map.get(("Team", team_title))
			if team_ext:
				doc.append("cluster_teams", {"team": team_ext})

		doc.save(ignore_permissions=True)


def generate_dummy_data(clean=False):
	"""Generate realistic, interconnected registry items.

	Args:
		clean: If True, wipe all existing registry data first.
	"""
	if clean:
		_cleanup_all()

	# ── Phase 1: Create Registry items (auto-creates empty extensions) ──
	existing = {
		(r.title, r.item_type)
		for r in frappe.get_all("Registry", fields=["title", "item_type"])
	}

	created = 0
	for item_type, title, description, category, tags in ITEMS:
		if (title, item_type) in existing:
			continue

		reg = frappe.new_doc("Registry")
		reg.title = title
		reg.item_type = item_type
		reg.description = description
		reg.category = category
		reg.trust_status = "approved"
		reg.author = "Sena"
		for tag in tags:
			reg.append("tags", {"tag": tag})
		reg.insert(ignore_permissions=True)
		created += 1

	frappe.db.commit()
	print(f"Phase 1: {created} registry items created")

	# ── Phase 2: Wire extensions with links and child tables ──
	ref_map = _build_ref_map()

	_wire_tools(ref_map)
	_wire_skills(ref_map)
	_wire_uis(ref_map)
	_wire_logic(ref_map)
	print("  Leaf extensions wired (tools, skills, UIs, logic)")

	_wire_agents(ref_map)
	print("  Agents wired (roles, UIs, logic, tools, skills)")

	_wire_team_types(ref_map)
	print("  Team types wired (role configs with permissions)")

	_wire_teams(ref_map)
	print("  Teams wired (team types + members)")

	_wire_clusters(ref_map)
	print("  Clusters wired (teams)")

	frappe.db.commit()
	print(f"Done: {created} items created, all extensions wired")
	return {"created": created}

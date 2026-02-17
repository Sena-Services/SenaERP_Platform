import frappe

from senaerp_platform.registry.embedding import (
	fulltext_search,
	semantic_search,
)


SEARCH_FIELDS = [
	"name",
	"slug",
	"title",
	"item_type",
	"category",
	"description",
	"trust_status",
	"featured",
	"author",
	"install_count",
]

_ORDER_FIELDS = {
	"featured": "featured DESC, modified DESC",
	"newest": "creation DESC",
	"updated": "modified DESC",
	"popular": "install_count DESC",
	"alpha": "title ASC",
}

EXTENSION_MAP = {
	"Cluster": "Registry Cluster",
	"Team": "Registry Team",
	"Agent": "Registry Agent",
	"Tool": "Registry Tool",
	"Skill": "Registry Skill",
	"UI": "Registry UI",
	"Logic": "Registry Logic",
	"Agent Role": "Registry Agent Role",
	"Team Type": "Registry Team Type",
}

EXTENSION_CHILDREN = {
	"Registry Cluster": ["cluster_teams"],
	"Registry Team": ["members"],
	"Registry Agent": ["agent_tools", "agent_skills"],
	"Registry Team Type": ["role_configs"],
}

# Direct link fields on extension DocTypes that point to other extensions
_EXT_LINK_FIELDS = {
	"Registry Agent": {
		"agent_role": "Registry Agent Role",
		"ui": "Registry UI",
		"logic": "Registry Logic",
	},
	"Registry Team": {
		"team_type": "Registry Team Type",
	},
}

# Link fields on child table rows that point to extension DocTypes
_CHILD_LINK_FIELDS = {
	"Registry Cluster Team": {"team": "Registry Team"},
	"Registry Team Member": {"role": "Registry Agent Role", "agent": "Registry Agent"},
	"Registry Agent Tool": {"tool": "Registry Tool"},
	"Registry Agent Skill": {"skill": "Registry Skill"},
	"Registry Team Type Role Config": {"role": "Registry Agent Role"},
}

# Map child table fieldname -> child DocType
_CHILD_TABLE_DOCTYPES = {
	"cluster_teams": "Registry Cluster Team",
	"members": "Registry Team Member",
	"agent_tools": "Registry Agent Tool",
	"agent_skills": "Registry Agent Skill",
	"role_configs": "Registry Team Type Role Config",
}


@frappe.whitelist(allow_guest=True)
def search(
	q=None,
	item_type=None,
	category=None,
	tags=None,
	trust_status="approved",
	featured_only=False,
	sort_by="featured",
	limit=20,
	offset=0,
):
	limit = min(int(limit), 100)
	offset = int(offset)
	featured_only = frappe.utils.sbool(featured_only)

	filters = {}
	if trust_status:
		filters["trust_status"] = trust_status
	if item_type:
		filters["item_type"] = item_type
	if category:
		filters["category"] = category
	if featured_only:
		filters["featured"] = 1

	order_fields = _ORDER_FIELDS.get(sort_by, _ORDER_FIELDS["featured"])

	if q:
		# Try semantic search first (embedding cosine similarity)
		semantic_results = semantic_search(q, filters=filters, limit=limit)
		if semantic_results is not None:
			items = semantic_results
			total = len(items)
			# Apply tag filter post-search if needed
			if tags:
				items = _filter_by_tags(items, tags)
				total = len(items)
			items = _attach_tags(items)
			return {"items": items, "total": total, "limit": limit, "offset": offset}

		# Fall back to FULLTEXT MATCH AGAINST
		try:
			sql_order = ", ".join(f"r.{p.strip()}" for p in order_fields.split(","))
			items, total = fulltext_search(q, filters=filters, order_by=sql_order, limit=limit, offset=offset)
			if tags:
				items = _filter_by_tags(items, tags)
				total = len(items)
			items = _attach_tags(items)
			return {"items": items, "total": total, "limit": limit, "offset": offset}
		except Exception:
			pass

		# Final fallback: LIKE search
		items, total = _like_search(q, tags, filters, order_fields, limit, offset)
	elif tags:
		items, total = _like_search(None, tags, filters, order_fields, limit, offset)
	else:
		items = frappe.get_list(
			"Registry",
			filters=filters,
			fields=SEARCH_FIELDS,
			order_by=order_fields,
			limit_page_length=limit,
			start=offset,
		)
		total = frappe.db.count("Registry", filters=filters)

	items = _attach_tags(items)
	return {"items": items, "total": total, "limit": limit, "offset": offset}


def _attach_tags(items):
	for item in items:
		if "name" in item:
			item["tags"] = [
				t.tag
				for t in frappe.get_all(
					"Registry Tag", filters={"parent": item["name"]}, fields=["tag"]
				)
			]
			del item["name"]
		elif "tags" not in item:
			item["tags"] = []
	return items


def _filter_by_tags(items, tags_str):
	tag_list = [t.strip().lower() for t in tags_str.split(",") if t.strip()]
	if not tag_list:
		return items
	filtered = []
	for item in items:
		item_name = item.get("name")
		if not item_name:
			continue
		item_tags = {
			t.tag.lower()
			for t in frappe.get_all("Registry Tag", filters={"parent": item_name}, fields=["tag"])
		}
		if all(t in item_tags for t in tag_list):
			filtered.append(item)
	return filtered


def _like_search(q, tags, filters, order_by, limit, offset):
	"""LIKE-based text search (last resort fallback)."""
	conditions = []
	values = {}

	for field, value in filters.items():
		conditions.append(f"r.`{field}` = %({field})s")
		values[field] = value

	if q:
		conditions.append(
			"(r.title LIKE %(q_like)s OR r.description LIKE %(q_like)s OR rt_search.tag LIKE %(q_like)s)"
		)
		values["q_like"] = f"%{q}%"

	if tags:
		tag_list = [t.strip().lower() for t in tags.split(",") if t.strip()]
		for i, tag in enumerate(tag_list):
			key = f"tag_{i}"
			conditions.append(
				f"EXISTS (SELECT 1 FROM `tabRegistry Tag` rt{i} WHERE rt{i}.parent = r.name AND rt{i}.tag = %({key})s)"
			)
			values[key] = tag

	where = " AND ".join(conditions) if conditions else "1=1"
	sql_order = ", ".join(f"r.{p.strip()}" for p in order_by.split(","))

	count_sql = f"""
		SELECT COUNT(DISTINCT r.name)
		FROM `tabRegistry` r
		LEFT JOIN `tabRegistry Tag` rt_search ON rt_search.parent = r.name
		WHERE {where}
	"""
	total = frappe.db.sql(count_sql, values)[0][0]

	sql = f"""
		SELECT DISTINCT r.name, r.slug, r.title, r.item_type, r.category,
			r.description, r.trust_status, r.featured, r.author, r.install_count
		FROM `tabRegistry` r
		LEFT JOIN `tabRegistry Tag` rt_search ON rt_search.parent = r.name
		WHERE {where}
		ORDER BY {sql_order}
		LIMIT %(limit)s OFFSET %(offset)s
	"""
	values["limit"] = limit
	values["offset"] = offset

	items = frappe.db.sql(sql, values, as_dict=True)
	return items, total


@frappe.whitelist(allow_guest=True)
def get_item(slug=None):
	if not slug:
		frappe.throw("slug is required", frappe.MandatoryError)

	reg = frappe.db.get_value(
		"Registry",
		{"slug": slug},
		["name", "slug", "title", "item_type", "category", "description",
		 "trust_status", "featured", "visibility", "ref_name", "install_count",
		 "author", "version", "source_url", "readme", "dotmatrix_avatar"],
		as_dict=True,
	)

	if not reg:
		frappe.throw(f"Registry item with slug '{slug}' not found", frappe.DoesNotExistError)

	reg["tags"] = [
		t.tag
		for t in frappe.get_all(
			"Registry Tag", filters={"parent": reg["name"]}, fields=["tag"]
		)
	]

	extension = None
	if reg.get("ref_name"):
		ext_doctype = EXTENSION_MAP.get(reg["item_type"])
		if ext_doctype:
			extension = _get_extension(ext_doctype, reg["ref_name"])

	del reg["name"]
	del reg["ref_name"]

	return {"registry": reg, "extension": extension}


def _get_extension(ext_doctype, ext_name):
	ext = frappe.get_doc(ext_doctype, ext_name)
	data = ext.as_dict()

	for key in ["doctype", "name", "owner", "creation", "modified", "modified_by",
				"docstatus", "idx", "registry"]:
		data.pop(key, None)

	# Resolve direct link fields to Registry items
	for field, target_dt in _EXT_LINK_FIELDS.get(ext_doctype, {}).items():
		if data.get(field):
			ref = _resolve_to_registry(target_dt, data[field])
			if ref:
				data[f"{field}_ref"] = ref

	# Clean and resolve child table rows
	child_fields = EXTENSION_CHILDREN.get(ext_doctype, [])
	for field in child_fields:
		if field in data and isinstance(data[field], list):
			child_dt = _CHILD_TABLE_DOCTYPES.get(field)
			data[field] = [_clean_child_row(row, child_dt) for row in data[field]]

	return data


def _clean_child_row(row, child_doctype=None):
	if not isinstance(row, dict):
		row = row.as_dict()
	else:
		row = dict(row)
	for key in ["doctype", "name", "owner", "creation", "modified", "modified_by",
				"docstatus", "parent", "parentfield", "parenttype", "idx"]:
		row.pop(key, None)

	# Resolve link fields to Registry items
	if child_doctype:
		for field, target_dt in _CHILD_LINK_FIELDS.get(child_doctype, {}).items():
			if row.get(field):
				ref = _resolve_to_registry(target_dt, row[field])
				if ref:
					row[f"{field}_ref"] = ref

	return row


def _resolve_to_registry(ext_doctype, ext_name):
	"""Resolve an extension DocType name back to its parent Registry item."""
	registry_name = frappe.db.get_value(ext_doctype, ext_name, "registry")
	if not registry_name:
		return None
	return frappe.db.get_value(
		"Registry", registry_name,
		["slug", "title", "item_type"], as_dict=True,
	)

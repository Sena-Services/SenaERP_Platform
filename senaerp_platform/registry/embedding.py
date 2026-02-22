import json
import math
import os
import urllib.request
import urllib.error

import frappe


SEARCH_FIELDS = [
	"name", "slug", "title", "item_type", "category",
	"description", "trust_status", "featured", "author",
	"install_count",
]


def build_search_text(doc):
	"""Build a concatenated text blob for embedding and fulltext search."""
	parts = [f"{doc.item_type}: {doc.title}"]
	if doc.description:
		parts.append(doc.description)
	if doc.category:
		parts.append(f"Category: {doc.category}")
	tags = []
	if hasattr(doc, "tags") and doc.tags:
		tags = [t.tag for t in doc.tags if hasattr(t, "tag")]
	if tags:
		parts.append(f"Tags: {', '.join(tags)}")
	return ". ".join(parts)


def get_embedding(text):
	"""Generate embedding vector using OpenAI-compatible API.

	Checks in order:
	  1. OPENAI_API_KEY env var
	  2. site_config embedding_api_key
	Returns None if no API key is configured.
	"""
	api_key = os.environ.get("OPENAI_API_KEY") or frappe.conf.get("embedding_api_key")
	if not api_key:
		return None

	base_url = (
		os.environ.get("OPENAI_BASE_URL")
		or frappe.conf.get("embedding_base_url")
		or "https://api.openai.com/v1"
	)
	model = (
		os.environ.get("EMBEDDING_MODEL")
		or frappe.conf.get("embedding_model")
		or "text-embedding-3-small"
	)

	url = f"{base_url.rstrip('/')}/embeddings"
	payload = json.dumps({"input": text, "model": model}).encode()
	req = urllib.request.Request(
		url,
		data=payload,
		headers={
			"Authorization": f"Bearer {api_key}",
			"Content-Type": "application/json",
		},
	)

	try:
		with urllib.request.urlopen(req, timeout=30) as resp:
			data = json.loads(resp.read())
			return data["data"][0]["embedding"]
	except (urllib.error.URLError, KeyError, IndexError) as e:
		frappe.log_error(f"Embedding API error: {e}", "Registry Embedding")
		return None


def cosine_similarity(a, b):
	dot = sum(x * y for x, y in zip(a, b))
	norm_a = math.sqrt(sum(x * x for x in a))
	norm_b = math.sqrt(sum(x * x for x in b))
	if norm_a == 0 or norm_b == 0:
		return 0.0
	return dot / (norm_a * norm_b)


_SIMILARITY_THRESHOLD = 0.30


def semantic_search(query, filters=None, limit=20):
	"""Search registry items by embedding similarity.

	Returns list of items sorted by relevance, or None if embeddings
	are unavailable or no items exceed the similarity threshold.
	"""
	query_embedding = get_embedding(query)
	if query_embedding is None:
		return None  # Caller should fall back to fulltext

	# Load items with embeddings
	db_filters = dict(filters or {})
	db_filters["_embedding"] = ("is", "set")

	items = frappe.get_all(
		"Registry",
		filters=db_filters,
		fields=SEARCH_FIELDS + ["_embedding"],
		limit_page_length=0,
	)

	scored = []
	for item in items:
		if not item.get("_embedding"):
			continue
		try:
			emb = json.loads(item["_embedding"])
		except (json.JSONDecodeError, TypeError):
			continue
		score = cosine_similarity(query_embedding, emb)
		if score >= _SIMILARITY_THRESHOLD:
			item["_score"] = score
			del item["_embedding"]
			scored.append(item)

	if not scored:
		return None  # Fall through to fulltext

	scored.sort(key=lambda x: x["_score"], reverse=True)
	result = scored[:limit]
	for item in result:
		item.pop("_score", None)
	return result


def fulltext_search(query, filters=None, order_by="", limit=20, offset=0):
	"""Fallback search using MariaDB FULLTEXT MATCH AGAINST."""
	conditions = []
	values = {"query": query}

	if filters:
		for field, value in filters.items():
			conditions.append(f"r.`{field}` = %({field})s")
			values[field] = value

	conditions.append("MATCH(r._search_text) AGAINST (%(query)s IN NATURAL LANGUAGE MODE)")
	where = " AND ".join(conditions)

	# Count
	count_sql = f"SELECT COUNT(*) FROM `tabRegistry` r WHERE {where}"
	total = frappe.db.sql(count_sql, values)[0][0]

	# Relevance-ranked results
	if not order_by:
		order_by = "relevance DESC"

	sql = f"""
		SELECT r.name, r.slug, r.title, r.item_type, r.category,
			r.description, r.trust_status, r.featured, r.author, r.install_count,
			MATCH(r._search_text) AGAINST (%(query)s IN NATURAL LANGUAGE MODE) AS relevance
		FROM `tabRegistry` r
		WHERE {where}
		ORDER BY {order_by}
		LIMIT %(limit)s OFFSET %(offset)s
	"""
	values["limit"] = limit
	values["offset"] = offset

	items = frappe.db.sql(sql, values, as_dict=True)
	for item in items:
		item.pop("relevance", None)
	return items, total


def update_embedding(registry_name):
	"""Generate and store embedding for a single registry item."""
	doc = frappe.get_doc("Registry", registry_name)
	search_text = build_search_text(doc)
	doc.db_set("_search_text", search_text, update_modified=False)

	embedding = get_embedding(search_text)
	if embedding:
		doc.db_set("_embedding", json.dumps(embedding), update_modified=False)
	return bool(embedding)


@frappe.whitelist()
def rebuild_search_index():
	"""Rebuild search text and embeddings for all registry items."""
	items = frappe.get_all("Registry", pluck="name")
	success = 0
	for name in items:
		if update_embedding(name):
			success += 1
	frappe.db.commit()
	return {"total": len(items), "embedded": success}

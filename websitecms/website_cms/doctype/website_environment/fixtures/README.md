# Website Environment Fixtures

This directory contains sample Website Environment documents that can be loaded into your Frappe site.

## Structure

Each JSON file represents a Website Environment document with the following structure:

```json
{
  "doctype": "Website Environment",
  "environment_id": "unique-id",           // URL-friendly ID
  "label": "Display Name",                 // Human-readable name
  "category": "Industry|Feature|Role",     // Type of environment
  "published": 1,                          // 1 = published, 0 = draft
  "display_order": 10,                     // Sort order
  "persona": "Short tagline",              // Brief description
  "summary": "Detailed description...",    // Full description
  "interface_count": 12,                   // Count of interfaces/UI
  "data_count": 6,                         // Count of data models
  "workflows_count": 8,                    // Count of workflows/automations
  "agents_count": 3,                       // Count of AI agents
  "bullet_1": "First feature point",       // Key feature 1
  "bullet_2": "Second feature point",      // Key feature 2
  "bullet_3": "Third feature point"        // Key feature 3
}
```

## Categories

### Industry
Environments designed for specific industry verticals:
- `travel-agencies.json` - Travel booking and package management
- `hotels.json` - Hotel property management

### Feature
Environments focused on specific business features:
- `sales-module.json` - Sales pipeline and CRM functionality

### Role
Environments designed for specific job roles:
- `receptionists.json` - Front desk and guest management

## Loading Fixtures

### Method 1: Using Bench Execute (Recommended)

From your bench directory, run:

```bash
bench --site <sitename> execute websitecms.website_cms.doctype.website_environment.fixtures.load_fixtures.load_all_fixtures
```

Example:
```bash
bench --site senamarketing.senaerp.com execute websitecms.website_cms.doctype.website_environment.fixtures.load_fixtures.load_all_fixtures
```

### Method 2: Using Frappe Console

```bash
bench --site <sitename> console
```

Then in the console:
```python
from websitecms.website_cms.doctype.website_environment.fixtures.load_fixtures import load_all_fixtures
load_all_fixtures()
```

### Method 3: Manual Import

1. Go to Website Environment list in Frappe desk
2. Click "Menu" → "Import"
3. Upload the JSON files one by one

## Creating New Fixtures

To create a new fixture:

1. Copy an existing JSON file
2. Update the values:
   - Change `environment_id` to a unique URL-friendly ID (lowercase, hyphens)
   - Set `label` to the display name
   - Choose appropriate `category`: Industry, Feature, or Role
   - Update `persona` and `summary`
   - Adjust metrics (ui_components, automations, etc.)
   - Update the 3 bullet points
3. Add the filename to `load_fixtures.py` in the `fixture_files` list
4. Load using one of the methods above

## API Usage

After loading, these environments are available via the API:

```bash
# Get all published environments
curl https://senamarketing.senaerp.com/api/method/websitecms.api.website_environment.get_published_environments

# Get specific environment
curl https://senamarketing.senaerp.com/api/method/websitecms.api.website_environment.get_environment_by_id?environment_id=travel-agencies

# Get count
curl https://senamarketing.senaerp.com/api/method/websitecms.api.website_environment.get_environment_count
```

## Notes

- The `environment_id` field is used for URL routing and must be unique
- The `display_order` field determines the sort order in listings (lower numbers appear first)
- Set `published: 0` for draft environments that shouldn't appear in the public API
- The loader script will update existing documents if they already exist (based on `environment_id`)

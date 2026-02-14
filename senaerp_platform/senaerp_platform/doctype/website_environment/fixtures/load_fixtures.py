#!/usr/bin/env python3
"""
Load Website Environment fixtures

This script loads sample Website Environment documents from JSON files.
Run this from the Frappe bench directory:

    bench --site <sitename> execute senaerp_platform.senaerp_platform.doctype.website_environment.fixtures.load_fixtures.load_all_fixtures
"""

import frappe
import json
import os


def load_fixture(fixture_file):
    """Load a single fixture file"""
    try:
        with open(fixture_file, 'r') as f:
            data = json.load(f)

        environment_id = data.get('environment_id')

        # Check if document already exists
        if frappe.db.exists('Website Environment', environment_id):
            print(f"✓ Environment '{environment_id}' already exists, updating...")
            doc = frappe.get_doc('Website Environment', environment_id)
            doc.update(data)
        else:
            print(f"+ Creating new environment '{environment_id}'...")
            doc = frappe.get_doc(data)

        doc.save()
        frappe.db.commit()
        print(f"  Successfully loaded: {data.get('label')} ({data.get('category')})")
        return True

    except Exception as e:
        print(f"✗ Error loading {fixture_file}: {str(e)}")
        return False


def load_all_fixtures():
    """Load all fixture files from the fixtures directory"""
    fixtures_dir = os.path.dirname(os.path.abspath(__file__))

    print("\n" + "="*60)
    print("Loading Website Environment Fixtures")
    print("="*60 + "\n")

    fixture_files = [
        'travel-agencies.json',
        'dmc.json',
        'hotels.json',
        'restaurants.json',
        'receptionists.json',
        'sales-module.json'
    ]

    loaded = 0
    failed = 0

    for fixture_file in fixture_files:
        file_path = os.path.join(fixtures_dir, fixture_file)
        if os.path.exists(file_path):
            if load_fixture(file_path):
                loaded += 1
            else:
                failed += 1
        else:
            print(f"⚠ Warning: Fixture file not found: {fixture_file}")

    print("\n" + "="*60)
    print(f"Summary: {loaded} loaded, {failed} failed")
    print("="*60 + "\n")

    return loaded, failed


if __name__ == "__main__":
    load_all_fixtures()

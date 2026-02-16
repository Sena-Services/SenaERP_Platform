from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from senaerp_platform.api.waitlist import _normalize_access_type


class TestWaitlistAccessType(unittest.TestCase):
    def test_normalize_access_type(self):
        self.assertEqual(_normalize_access_type(None), "Product")
        self.assertEqual(_normalize_access_type("product"), "Product")
        self.assertEqual(_normalize_access_type("pitchdeck"), "Pitch Deck")
        self.assertEqual(_normalize_access_type("Pitch Deck"), "Pitch Deck")
        self.assertEqual(_normalize_access_type("pitch-deck"), "Pitch Deck")
        self.assertEqual(_normalize_access_type("unknown"), "")


class TestProvisioningFailure(unittest.TestCase):
    @patch("senaerp_platform.api.accept.subprocess.run")
    @patch("senaerp_platform.api.accept.frappe")
    def test_failure_marks_waitlist_failed(self, mock_frappe, mock_run):
        from senaerp_platform.api.accept import run_provisioning

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "boom"
        mock_run.return_value = mock_result

        ps_doc = MagicMock()
        wl_doc = MagicMock()

        def get_doc_side_effect(doctype, name):
            if doctype == "Provisioned Site":
                return ps_doc
            if doctype == "Waitlist":
                return wl_doc
            raise AssertionError(f"unexpected doctype {doctype}")

        mock_frappe.get_doc.side_effect = get_doc_side_effect
        mock_frappe.conf.get.return_value = "/tmp"

        run_provisioning(
            subdomain="acme",
            email="owner@acme.com",
            company_name="Acme",
            waitlist_name="WL-001",
            provisioned_site_name="PS-001",
        )

        self.assertEqual(ps_doc.status, "Failed")
        self.assertEqual(wl_doc.status, "Failed")
        ps_doc.save.assert_called()
        wl_doc.save.assert_called()


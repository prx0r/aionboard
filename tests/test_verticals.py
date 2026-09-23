"""Tests for repeatable vertical packs."""

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VERTICALS_ROOT = REPO_ROOT / "verticals"
REQUIRED_FILES = (
    "manifest.json",
    "README.md",
    "PAINS.md",
    "STACK.md",
    "CAMPAIGN.md",
    "DISCOVERY.md",
    "INSTALL.md",
)
FORBIDDEN_CLAIMS = (
    "appear in ChatGPT",
    "guaranteed placement",
    "live voice service is included",
    "Meta production integration is included",
)


def vertical_directories():
    return sorted(
        path
        for path in VERTICALS_ROOT.iterdir()
        if path.is_dir() and not path.name.startswith((".", "_"))
    )


class VerticalPackTests(unittest.TestCase):
    def test_expected_pilot_verticals_exist(self):
        names = {path.name for path in vertical_directories()}
        self.assertIn("electrician", names)
        self.assertIn("beauty", names)

    def test_manifests_are_valid_and_use_subdomains(self):
        for vertical in vertical_directories():
            with self.subTest(vertical=vertical.name):
                manifest_path = vertical / "manifest.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                self.assertEqual(manifest["vertical"], vertical.name)
                self.assertEqual(manifest["pilot_package"], "standard-ai-setup")
                self.assertEqual(manifest["public_offer"], "../../OFFER.md")
                self.assertTrue(
                    manifest["proposed_subdomain"].endswith(".aionboard.co.uk"),
                    msg=f"{vertical.name} must use an aionboard.co.uk subdomain",
                )
                self.assertEqual(manifest["subdomain_status"], "proposed")

    def test_required_pack_files_exist(self):
        for vertical in vertical_directories():
            with self.subTest(vertical=vertical.name):
                for filename in REQUIRED_FILES:
                    self.assertTrue(
                        (vertical / filename).is_file(),
                        msg=f"{vertical.name} is missing {filename}",
                    )

    def test_vertical_docs_make_no_guarantees(self):
        for vertical in vertical_directories():
            for filename in REQUIRED_FILES:
                if not filename.endswith(".md"):
                    continue
                with self.subTest(vertical=vertical.name, file=filename):
                    text = (vertical / filename).read_text(encoding="utf-8")
                    for forbidden in FORBIDDEN_CLAIMS:
                        self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)

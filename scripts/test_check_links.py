"""Regression checks for failures that can hide on a Windows working copy."""
from pathlib import Path
import tempfile
import unittest

from check_links import audit


class LinkAuditTests(unittest.TestCase):
    def test_reader_routes_and_github_anchors(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Guide (1).md").write_text(
                '# Guide\n## What next?\n## What next?\n## Use `Focus 10` carefully\n<a id="term-obe"></a>\n', encoding="utf-8")
            (root / "README.md").write_text(
                '# Home\n[Read](<Guide (1).md#what-next-1>)\n'
                '[Term](Guide%20%281%29.md#term-obe)\n'
                '[Code heading](Guide%20%281%29.md#use-focus-10-carefully)\n'
                '[Reference][guide]\n[guide]: <Guide (1).md#guide>\n'
                '```md\n[Example only](absent.md)\n```\n', encoding="utf-8")
            self.assertEqual(audit(root)["errors"], [])

    def test_missing_paths_fragments_and_case_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Guide.md").write_text('# Guide\n', encoding="utf-8")
            (root / "README.md").write_text(
                '[Wrong case](guide.md)\n[Old heading](Guide.md#removed)\n'
                '![Missing exhibit](figure.png)\n[Missing reference][unknown]\n', encoding="utf-8")
            self.assertEqual(len(audit(root)["errors"]), 4)

    def test_linked_image_checks_both_destinations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "figure.svg").write_text('<svg/>', encoding="utf-8")
            (root / "README.md").write_text('[![Figure](figure.svg)](missing.md)\n', encoding="utf-8")
            self.assertEqual(len(audit(root)["errors"]), 1)

    def test_unfinished_citations_and_invalid_inventory_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text('Claim.[[FN01]]\n', encoding="utf-8")
            (root / "research").mkdir()
            (root / "research/05_Research_Source_Inventory.json").write_text('{broken', encoding="utf-8")
            self.assertEqual(len(audit(root)["errors"]), 2)


if __name__ == "__main__":
    unittest.main()

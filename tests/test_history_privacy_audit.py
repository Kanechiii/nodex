"""Regression tests for historical privacy auditing."""

import unittest
from unittest.mock import patch

from scripts import history_privacy_audit as audit


class HistoryAuditTests(unittest.TestCase):
    def test_old_bytecode_path_is_not_lost_after_rename(self):
        blob = "a" * 40
        entries = (
            b"100644 blob " + blob.encode() + b"\told/app.pyc\x00"
            + b"100644 blob " + blob.encode() + b"\tapp.bin\x00"
        )

        def fake_git(*args):
            if args == ("log", "--all", "--format=%T"):
                return b"b" * 40 + b"\nc" * 40 + b"\n"
            if args[:3] == ("ls-tree", "-r", "-z"):
                return entries
            raise AssertionError(args)

        with patch.object(audit, "git", side_effect=fake_git):
            found = audit.get_blobs()
        self.assertEqual(found, [(blob, "old/app.pyc")])

    def test_scans_historical_binary_without_decoding_it(self):
        indicators = audit.scan_blob(
            b"\x00data person@example.invalid "
            b"C:\\Users\\Example\\project\\module.pyc "
            b"-----BEGIN PRIVATE KEY-----\x00"
        )
        self.assertGreaterEqual(indicators["emails"], 1)
        self.assertGreaterEqual(indicators["paths"], 1)
        self.assertGreaterEqual(indicators["secrets"], 1)

    def test_no_reply_classification(self):
        self.assertEqual(audit.classify("123+user@users.noreply.github.com"), "GitHub no-reply")
        self.assertEqual(audit.classify("contact@example.invalid"), "other email")


if __name__ == "__main__":
    unittest.main()

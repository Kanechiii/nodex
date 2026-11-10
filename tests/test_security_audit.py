"""Check that the source audit distinguishes PEM keys from test fixtures."""

import unittest

from scripts import security_audit as audit


class SecurityAuditTests(unittest.TestCase):
    def setUp(self):
        audit.issues.clear()

    def tearDown(self):
        audit.issues.clear()

    def test_header_alone_is_not_a_private_key(self):
        sample = b"-----BEGIN " + b"PRIVATE KEY-----"
        audit.check_data(sample, "fixture")
        self.assertEqual(audit.issues, [])

    def test_complete_synthetic_pem_is_detected(self):
        header = b"-----BEGIN " + b"PRIVATE KEY-----"
        footer = b"-----END " + b"PRIVATE KEY-----"
        sample = header + b"\n" + b"A" * 64 + b"\n" + footer
        audit.check_data(sample, "fixture")
        self.assertEqual(len(audit.issues), 1)
        self.assertIn("possible private key", audit.issues[0])
        self.assertIn("value redacted", audit.issues[0])

    def test_mismatched_pem_labels_are_not_accepted(self):
        header = b"-----BEGIN " + b"RSA PRIVATE KEY-----"
        footer = b"-----END " + b"EC PRIVATE KEY-----"
        sample = header + b"\n" + b"A" * 64 + b"\n" + footer
        audit.check_data(sample, "fixture")
        self.assertEqual(audit.issues, [])


if __name__ == "__main__":
    unittest.main()

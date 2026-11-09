import unittest
from contextlib import redirect_stdout
from io import StringIO

from models.device import Device


class DeviceTests(unittest.TestCase):
    def test_attributes_and_display(self):
        d = Device(7, "Switch-7", "Switch", 8)
        self.assertEqual((d.device_id, d.hostname, d.device_type, d.port_capacity),
                         (7, "Switch-7", "Switch", 8))
        output = StringIO()
        with redirect_stdout(output):
            d.display_info()
        self.assertIn("Device ID: 7", output.getvalue())
        self.assertIn("Port Capacity: 8", output.getvalue())


if __name__ == "__main__":
    unittest.main()

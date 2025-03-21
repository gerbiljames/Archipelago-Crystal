from test.bases import TestBase
from ..phone_data import phone_scripts


class PhoneCallsTest(TestBase):
    max_phone_trap_bytes = 1024

    def test_phone_calls(self):
        for script in phone_scripts:
            assert len(script.get_script_bytes()) < self.max_phone_trap_bytes

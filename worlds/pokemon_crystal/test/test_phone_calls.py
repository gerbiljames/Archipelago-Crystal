from test.bases import TestBase
from ..phone_data import phone_scripts, poke_cmd


class PhoneCallsTest(TestBase):
    max_phone_trap_bytes = 1024
    max_line_length = 18

    def test_phone_calls(self):
        for script in phone_scripts:

            assert len(script.get_script_bytes()) < self.max_phone_trap_bytes

            for line in script.lines:
                assert sum(
                    [len(item) if isinstance(item, str) else 4 if item == poke_cmd else 7 for item in
                     line.contents[1:]]) <= self.max_line_length, f"{line.contents[1:]} is too long."

import unittest
from helpers import time_in_minutes, minutes_to_time, format_available_minutes


# Simple unit tests (in unittest).


class TestHelpers(unittest.TestCase):

    def test_time_in_minutes(self):
        self.assertEqual(time_in_minutes('00:00'), 0)
        self.assertEqual(time_in_minutes('00:01'), 1)
        self.assertEqual(time_in_minutes('01:00'), 60)
        self.assertEqual(time_in_minutes('23:59'), 1439)

    def test_minutes_to_time(self):
        self.assertEqual(minutes_to_time(0), '00:00')
        self.assertEqual(minutes_to_time(1), '00:01')
        self.assertEqual(minutes_to_time(60), '01:00')
        self.assertEqual(minutes_to_time(1439), '23:59')

    def test_format_available_minutes(self):
        self.assertEqual(format_available_minutes([0, 1, 2, 60, 61, 120]), ['00:00 - 00:02', '01:00 - 01:01',
                                                                            '02:00 - 02:00'])
        self.assertEqual(format_available_minutes([0]), ['00:00 - 00:00'])


if __name__ == '__main__':
    unittest.main()

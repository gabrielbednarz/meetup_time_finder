import unittest
from main import Time, Colleague, valid_time_format


# Simple unit tests (in unittest).


class TestMain(unittest.TestCase):

    def test_valid_time_format(self):
        self.assertTrue(valid_time_format('00:00'))
        self.assertTrue(valid_time_format('23:59'))
        self.assertFalse(valid_time_format('24:00'))
        self.assertFalse(valid_time_format('23:60'))
        self.assertFalse(valid_time_format('00:60'))
        self.assertFalse(valid_time_format('0000'))

    def test_time_class(self):
        time_obj = Time('00:00', '01:00')
        self.assertEqual(time_obj.from_in_minutes, 0)
        self.assertEqual(time_obj.to_in_minutes, 60)
        self.assertEqual(time_obj.time_in_minutes, [range(0, 61)])

        time_obj_2 = Time('23:00', '01:00')
        self.assertEqual(time_obj_2.from_in_minutes, 1380)
        self.assertEqual(time_obj_2.to_in_minutes, 60)
        self.assertEqual(time_obj_2.time_in_minutes, [range(1380, 1440), range(0, 61)])

    def test_colleague_class(self):
        Colleague.busy_range_list = []
        colleague = Colleague("John")
        colleague_2 = Colleague("Jack")
        time_obj = Time('00:30', '01:00')
        time_obj_2 = Time('20:00', '21:00')
        colleague.append_to_busy_range_list(time_obj)
        colleague_2.append_to_busy_range_list(time_obj_2)
        self.assertEqual(colleague.name, "John")
        self.assertEqual(colleague_2.name, "Jack")
        self.assertEqual(Colleague.busy_range_list, [range(30, 61), range(1200, 1261)])


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch
from main import get_valid_number_of_colleagues, add_colleague, Colleague
import io
# import sys
import main


class TestGetValidNumberOfColleagues(unittest.TestCase):
    def test_valid_input(self):
        with patch("builtins.input", return_value="5"):
            result = get_valid_number_of_colleagues("Enter the number of colleagues: ")
            self.assertEqual(result, 5)

    @patch("builtins.input", side_effect=["not_an_integer", "True", "10"])
    def test_invalid_input(self, magic_mock):  # MagicMock as magic_mock is necessary.
        result = get_valid_number_of_colleagues("Enter the number of colleagues: ")
        self.assertEqual(result, 10)


class TestAddColleague(unittest.TestCase):

    def test_add_colleagues_valid(self):
        with patch("builtins.input", side_effect=["James", "08:00", "15:00", "n"]):
            Colleague.busy_range_list = []
            colleague1 = add_colleague()
            self.assertEqual(colleague1.name, "James")
            self.assertEqual(len(Colleague.busy_range_list), 1)

        with patch("builtins.input", side_effect=["Alice", "10:00", "12:00", "n"]):
            colleague2 = add_colleague()
            self.assertEqual(colleague2.name, "Alice")
            self.assertEqual(len(Colleague.busy_range_list), 2)

    def test_add_colleague_invalid(self):
        with patch("builtins.input", side_effect=["Bob", "invalid_time", "10:00", "12:00", "n"]):
            # Colleague.busy_range_list = []
            colleague = add_colleague()
            self.assertEqual(colleague.name, "Bob")
            self.assertEqual(len(Colleague.busy_range_list), 1)

    def test_add_colleague_valid_patch(self):
        with patch('builtins.input') as mock_input, \
             patch('main.get_valid_time') as mock_get_valid_time, \
             patch('main.get_yes_no') as mock_get_yes_no:

            # Note. The mock_input, mock_get_yes_no, and mock_get_valid_time objects are instances of MagicMock.

            mock_input.return_value = 'John Doe'
            mock_get_valid_time.side_effect = ['08:00', '09:00']
            mock_get_yes_no.return_value = 'n'

            colleague = add_colleague()
            self.assertEqual(colleague.name, 'John Doe')
            self.assertEqual(len(colleague.busy), 0)  # The busy attribute of Colleague remains empty.


class TestMainFunction(unittest.TestCase):

    def test_main_simpler(self):
        Colleague.busy_range_list = []

        input_values = ["2", "Alice", "08:00", "10:00", "N", "Bob", "14:00", "16:00", "n"]
        output_mock = io.StringIO()

        with patch("builtins.input", side_effect=input_values):
            with patch("sys.stdout", new_callable=lambda: output_mock):
                main.main()
                # main() outputs data using print statements, which write to sys.stdout by default. But now main()
                # writes into output_mock.getvalue() via patch("sys.stdout", new_callable=lambda: output_mock).

        captured_output = output_mock.getvalue()

        assert 'Possible meeting' in captured_output
        assert '00:00 - 07:59' in captured_output
        assert '10:01 - 13:59' in captured_output
        assert '16:01 - 23:59' in captured_output


if __name__ == '__main__':
    unittest.main()

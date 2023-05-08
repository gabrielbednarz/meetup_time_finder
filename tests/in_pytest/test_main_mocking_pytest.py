import main
from main import get_valid_number_of_colleagues, add_colleague, Colleague
from unittest.mock import patch
import pytest
# import sys
import io


# For demonstration purposes, I will use mocker.patch as well as unittest.mock.patch.

# Testing get_valid_number_of_colleagues:

def test_valid_input():
    with patch("builtins.input", return_value="5"):
        result = get_valid_number_of_colleagues("Enter the number of colleagues: ")
        assert result == 5


@patch("builtins.input", side_effect=["not_an_integer", "10"])
def test_invalid_input(magic_mock):  # magic_mock represents MagicMock from unittest.
    result = get_valid_number_of_colleagues("Enter the number of colleagues: ")
    assert result == 10


# Essentially the same two tests - as the one before - but with mocker.patch context manager.


def test_invalid_input_mocker(mocker):
    mocker.patch("builtins.input", side_effect=["not_an_integer", "10"])
    result = get_valid_number_of_colleagues("Enter the number of colleagues: ")
    assert result == 10


def test_invalid_input_mocker_with(mocker):
    with mocker.patch("builtins.input", side_effect=["not_an_integer", "10"]):
        result = get_valid_number_of_colleagues("Enter the number of colleagues: ")
        assert result == 10


# We will now test add_colleague.


def test_add_colleague_mocker(mocker):
    with mocker.patch("builtins.input", side_effect=["James", "08:00", "15:00", "n"]):
        Colleague.busy_range_list = []
        colleague = add_colleague()  # In main.py you can see that this function returns a Colleague object.
        assert colleague.name == "James"
        assert len(Colleague.busy_range_list) == 1


def test_add_colleague_valid(mocker):
    with mocker.patch("builtins.input", side_effect=["Alice", "10:00", "12:00", "n"]):
        Colleague.busy_range_list = []
        colleague = add_colleague()
        assert colleague.name == "Alice"


def test_add_colleague_invalid(mocker):
    with mocker.patch("builtins.input", side_effect=["Bob", "invalid_time", "10:00", "12:00", "n"]):
        Colleague.busy_range_list = []
        colleague = add_colleague()
        assert colleague.name == "Bob"


# Test and mock main() function with two colleagues.


def test_main(mocker):
    Colleague.busy_range_list = []

    # with statement automatically handles MagicMock. No variable representing it will be used.

    with mocker.patch("builtins.input", side_effect=["2", "Alice", "08:00", "10:00",
                                                     "N", "Bob", "14:00", "16:00", "n"]):
        # Mocking output:
        output_mock = io.StringIO()

        # new_callable has a callable used to create an object. Here lambda function creates the replacement
        # (output_mock) for standard output (sys.stdout) every time this function is called.

        with mocker.patch("sys.stdout", new_callable=lambda: output_mock):
            # We could also write:
            # with mocker.patch("sys.stdout", new_callable=lambda: io.StringIO()) as output_mock:

            main.main()

            # main() outputs data using print statements, these write to sys.stdout by default.
            # But sys.stdout is being mocked, so they write into output_mock.get_value().

            output = output_mock.getvalue()

    assert 'Possible meeting' in output
    assert '00:00 - 07:59' in output
    assert '10:01 - 13:59' in output
    assert '16:01 - 23:59' in output


# A simpler version. As opposed to unittest.mock.patch, mocker from pytest automatically handles setting up and tearing
# down the mocks. No need to write start() and stop() in lines like these:

#     input_mock.start()
#     output_mock = io.StringIO()
#     sys_stdout_mock = patch("sys.stdout", new_callable=lambda: output_mock)
#     sys_stdout_mock.start()
#     main.main()
#     input_mock.stop()
#     sys_stdout_mock.stop()


# Since the mocker fixture automatically undoes mocking at the end of a test you do not need to use as context managers:

def test_main_simpler(mocker):
    Colleague.busy_range_list = []

    # Mock input:
    mocker.patch("builtins.input", side_effect=["2", "Alice", "08:00", "10:00", "N", "Bob", "14:00", "16:00", "n"])

    output_mock = io.StringIO()

    # We set up one mock output of print statements from main() function. Once main() is called, it will write
    # into output_mock.get_value() empty string initiated by output_mock = io.StringIO().
    # Mock output:
    mocker.patch("sys.stdout", new_callable=lambda: output_mock)

    main.main()  # main() outputs data using print statements, which write to sys.stdout by default.

    captured_output = output_mock.getvalue()

    assert 'Possible meeting' in captured_output
    assert '00:00 - 07:59' in captured_output
    assert '10:01 - 13:59' in captured_output
    assert '16:01 - 23:59' in captured_output


def test_main_simpler_2(mocker):
    Colleague.busy_range_list = []

    mocker.patch("builtins.input", side_effect=["2", "Alice", "20:00", "10:00", "N", "Bob", "01:00", "15:55", "n"])

    output_mock = io.StringIO()
    mocker.patch("sys.stdout", new_callable=lambda: output_mock)

    main.main()

    captured_output = output_mock.getvalue()

    assert 'Possible meeting' in captured_output
    assert '15:56 - 19:59' in captured_output

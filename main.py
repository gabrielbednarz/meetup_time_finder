from dataclasses import dataclass, field
from typing import ClassVar  # To set a class variable showing a busy time ranges, for every Colleague.
import helpers
import re


# Data classes

# We'll convert a start or end time to the number of minutes since 00:00.
# Keep in mind that the first minute is of number 0. The last is 1439.


@dataclass
class Time:

    busy_from: str
    busy_to: str  # Example of Time object: Time('00:00', '01:00').

    from_in_minutes: int = field(init=False, repr=False)
    to_in_minutes: int = field(init=False, repr=False)

    time_in_minutes: list[range] = field(init=False, repr=False)

    def __post_init__(self):
        self.from_in_minutes = helpers.time_in_minutes(self.busy_from)
        self.to_in_minutes = helpers.time_in_minutes(self.busy_to)

        if self.to_in_minutes >= self.from_in_minutes:
            self.time_in_minutes = [range(self.from_in_minutes, self.to_in_minutes + 1)]

        else:
            self.time_in_minutes = [
                range(self.from_in_minutes, 1440),
                range(0, self.to_in_minutes + 1)
            ]


@dataclass
class Colleague:

    busy_range_list: ClassVar[list] = []

    name: str

    # Creates a personal list of busy times. This step is not necessary.

    busy: list[Time] = field(default_factory=list, repr=False)  # Sets the default [] if the value is not provided.

    @staticmethod
    def append_to_busy_range_list(time: Time):
        # self.busy.append(time)  # Here we can additionally append a Time object to the personal list of busy times.

        # Making use of the ClassVar, we append to its list every busy time of every person:

        for time_range in time.time_in_minutes:
            Colleague.busy_range_list.append(time_range)


# Functions
# Four helper functions to handle the input:

def get_valid_number_of_colleagues(prompt):
    while True:
        try:
            number = int(input(prompt))
            return number
        except ValueError:
            print("Type an integer.")


def valid_time_format(time_str):
    pattern = r'^(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$'
    return bool(re.match(pattern, time_str))


def get_valid_time(prompt):
    while True:
        time_str = input(prompt)
        if valid_time_format(time_str):
            return time_str
        else:
            print("Invalid time format. Please use the format HH:MM.")


def get_yes_no(prompt):
    while True:
        answer = input(prompt).lower()
        if answer in ('y', 'n'):
            return answer
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")


# The last function creates a person and assigns busy times.

def add_colleague():
    name = input("Enter colleague's name: ")
    colleague = Colleague(name)

    while True:
        try:
            start_time = get_valid_time("Enter start time of busy period (HH:MM): ")
            end_time = get_valid_time("Enter end time of busy period (HH:MM): ")
            colleague.append_to_busy_range_list(Time(start_time, end_time))

            more_busy_times = get_yes_no("Add more busy times? (Y/N): ")
            if more_busy_times == 'n':
                break
        except ValueError:
            print("Invalid time format. Please use the format HH:MM.")

    return colleague


def main():
    all_day_minutes = set(range(1440))
    busy_minutes = set()

    num_colleagues = get_valid_number_of_colleagues("Enter the number of colleagues: ")

    for _ in range(num_colleagues):
        add_colleague()

    for r in Colleague.busy_range_list:
        busy_minutes.update(r)  # We can sum sets (busy_minutes) with other data types such as range (r).

    free_minutes = all_day_minutes - busy_minutes

    print(helpers.format_available_minutes(list(free_minutes)))

    for i in helpers.format_available_minutes(list(free_minutes)):
        print(f'Possible meeting at {i}.')


if __name__ == '__main__':
    main()

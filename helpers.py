from typing import List


# Takes time string (e.g. '07:45') and converts it into the number of minutes (integer), e.g. 465.

def time_in_minutes(time):
    h, m = time.split(':')
    return int(h) * 60 + int(m)


def minutes_to_time(minutes):  # The reverse. It transforms minutes into time string, e.g. 465 into '07:45'.
    h, m = divmod(minutes, 60)
    return f"{h:02d}:{m:02d}"  # Pad zeros to hours and minutes to return strings of the format 05:09.


# The next function takes the list of available minutes (from 0 to 1439), and transforms it into a nested list.
# The nested lists are then transformed into a list of formatted available time periods.

def format_available_minutes(array: List[int]):  # Takes the list of minutes as integers from 0 to 1439.
    nested_list = []  # Start a nested list.
    current_list = []

    for idx, element in enumerate(array):

        # Add the first element to the current group:

        if not current_list:
            current_list.append(element)

        # Check if the current element is a consecutive one:

        elif element == current_list[-1] + 1:
            current_list.append(element)

        else:

            # If the current element is not consecutive, add the current group to the nested_list:

            nested_list.append(current_list)
            current_list = [element]

    # Add the last group to the nested_list:

    nested_list.append(current_list)

    # Sort and merge overlapping time ranges.
    # Sort according to the first element of every sublist. This can be done because we know that every sublist has
    # consecutive integers. Although with or without key=lambda x: x[0] this is O(nlog(n)). However, no need for
    # lexicographic order, i.e. sorted(nested_list).

    nested_list = sorted(nested_list, key=lambda x: x[0])
    merged_ranges = []

    for current_range in nested_list:
        if not merged_ranges or current_range[0] > merged_ranges[-1][-1] + 1:  # Without + 1, it's always larger.
            merged_ranges.append(current_range)
            # The line above is valid since by sorted(nested_list, key=lambda x: x[0]) we made sure that the nested
            # list, when summed up by some set theory operation, is ordered from smallest to biggest numbers.
        else:
            merged_ranges[-1][-1] = current_range[-1]

    # Transform the nested list into a list of formatted available time periods. For now, the nested list contains
    # the list of consecutive minutes. The transformation looks like this: from [[0, 1, 2, 3], [120, 121, 122]]
    # into ['00:00 - 00:03', '02:00 - 02:03'].

    available_time_periods = []

    for nested in merged_ranges:
        start_in_minutes = minutes_to_time(nested[0])
        end_in_minutes = minutes_to_time(nested[-1])
        time_range_str = f'{start_in_minutes} - {end_in_minutes}'
        available_time_periods.append(time_range_str)

    return available_time_periods

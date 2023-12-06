def radix_sort_for_numbers_lsd(to_be_sorted):
    if not isinstance(to_be_sorted, list) or len(to_be_sorted) == 0:
        return []
    element_type = type(to_be_sorted[0])
    if not all(isinstance(element, element_type) for element in to_be_sorted):
        return []

    maximum_value = max(to_be_sorted)
    max_exponent = len(str(maximum_value))
    # [:] is used to create a new list object of the input list.
    # a simply assignement would not work since it will still reference the same object in memory
    being_sorted = to_be_sorted[:]

    for exponent in range(max_exponent):
        position = exponent + 1
        index = -position

        digits = [[] for i in range(10)]

        for number in being_sorted:
            number_as_a_string = str(number)
            try:
                digit = number_as_a_string[index]
            except IndexError:
                digit = 0
            digit = int(digit)

            digits[digit].append(number)

        being_sorted = []
        for numeral in digits:
            being_sorted.extend(numeral)

    return being_sorted


def radix_sort_for_strings(to_be_sorted):

    if not isinstance(to_be_sorted, list) or len(to_be_sorted) == 0:
        return []

    element_type = type(to_be_sorted[0])
    if not all(isinstance(element, element_type) for element in to_be_sorted):
        return []

    # Find the maximum length of a string in the list
    max_length = max(len(string) for string in to_be_sorted)

    # [:] is used to create a new list object of the input list.
    # a simple assignment would not work since it will still reference the same object in memory
    being_sorted = to_be_sorted[:]

    # Iterate over each character in each string from right to left
    for index in range(max_length - 1, -1, -1):
        # Create a list of empty lists, one for each possible value of a character
        buckets = [[] for value in range(256)]

        # Assign each string to the appropriate bucket based on the character at the current position
        for string in being_sorted:
            if len(string) > index:
                # get each unicode point for each character
                char_value = ord(string[index])
            else:
                # If the string is too short, assign it to the first bucket
                char_value = 0
            buckets[char_value].append(string)

        # Concatenate the buckets back into a single list, in the order of the character values
        being_sorted = [string for bucket in buckets for string in bucket]

    return being_sorted


def radix_sort(to_be_sorted, msd=False):
    if not to_be_sorted:
        return to_be_sorted

    max_number = max(to_be_sorted)
    max_length = len(str(max_number))

    if msd:
        to_be_sorted = [str(number).zfill(max_length)
                        for number in to_be_sorted]
        for index in range(max_length-1, -1, -1):
            buckets = [[] for _ in range(10)]
            for number in to_be_sorted:
                digit = int(number[index])
                buckets[digit].append(number)
            # create new list for every number in bucket of buckets
            to_be_sorted = [number for bucket in buckets for number in bucket]
        to_be_sorted = [int(number.lstrip('0')) for number in to_be_sorted]
    else:
        for index in range(max_length):
            buckets = [[] for _ in range(10)]
            for number in to_be_sorted:
                digit = number % 10**(index+1) // 10**index
                buckets[digit].append(number)
            to_be_sorted = [number for bucket in buckets for number in bucket]

    return to_be_sorted


liste = [12, 4, 68, 23, 891]

sorted_lst = radix_sort(liste, msd=True)
print(sorted_lst)  # sollte [4, 12, 23, 68, 891] ergeben

sorted_lst = radix_sort(liste, msd=False)
print(sorted_lst)  # sollte [4, 12, 23, 68, 891] ergeben

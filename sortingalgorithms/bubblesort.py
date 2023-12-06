def swap(array, first_index, second_index):
    temporary_value = array[first_index]
    array[first_index] = array[second_index]
    array[second_index] = temporary_value


def bubble_sort_unoptimized(array, descending=False):
    if not isinstance(array, list) or len(array) <= 0:
        return []
    element_type = type(array[0])
    if not all(isinstance(element, element_type) for element in array):
        return []
    for element in array:
        for index in range(len(array) - 1):
            if array[index] > array[index + 1]:
                swap(array, index, index + 1)

    if descending:
        return list(reversed(array))
    return array


def bubble_sort(array, descending=False):
    if not isinstance(array, list) or len(array) == 0:
        return []
    element_type = type(array[0])
    if not all(isinstance(element, element_type) for element in array):
        return []
    for i in range(len(array)):
        # iterate through unplaced elements
        for index in range(len(array) - i - 1):
            if array[index] > array[index + 1]:
                # replacement for swap function
                array[index], array[index +
                                    1] = array[index + 1], array[index]

    if descending:
        return list(reversed(array))
    return array


liste = [4, 12, 23, 68, 891]

print(bubble_sort_unoptimized(liste, True))

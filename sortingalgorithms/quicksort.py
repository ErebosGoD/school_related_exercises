from random import randrange


def quicksort(input_list, start, end):
    if not isinstance(input_list, list) or not isinstance(start, int) or not isinstance(end, int) or len(input_list) == 0:
        return []
    element_type = type(input_list[0])
    if not all(isinstance(element, element_type) for element in input_list):
        return []
    # this portion of list has been sorted
    if start >= end:
        return input_list[start:end+1]

    # select random element to be pivot
    pivot_index = randrange(start, end + 1)
    pivot_element = input_list[pivot_index]
    # swap random element with last element in sub-lists
    input_list[end], input_list[pivot_index] = input_list[pivot_index], input_list[end]

    # tracks all elements which should be to left (lesser than) pivot
    less_than_pointer = start

    for i in range(start, end):
        # we found an element out of place
        if input_list[i] < pivot_element:
            # swap element to the right-most portion of lesser elements
            input_list[i], input_list[less_than_pointer] = input_list[less_than_pointer], input_list[i]
            # tally that we have one more lesser element
            less_than_pointer += 1
    # move pivot element to the right-most portion of lesser elements
    input_list[end], input_list[less_than_pointer] = input_list[less_than_pointer], input_list[end]
    # recursively sort left and right sub-lists and combine them with pivot element
    left_sorted = quicksort(input_list, start, less_than_pointer - 1)
    right_sorted = quicksort(input_list, less_than_pointer + 1, end)
    return left_sorted + [pivot_element] + right_sorted

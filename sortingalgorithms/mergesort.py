def merge_sort(array):
    if not isinstance(array, list) or len(array) == 0:
        return []
    element_type = type(array[0])
    if not all(isinstance(element, element_type) for element in array):
        return []

    if len(array) <= 1:
        return array

    middle_index = len(array) // 2
    left_split = array[:middle_index]
    right_split = array[middle_index:]

    left_sorted = merge_sort(left_split)
    right_sorted = merge_sort(right_split)
    return merge(left_sorted, right_sorted)


def merge(left_part_of_list, right_part_of_list):
    result = []
    if isinstance(left_part_of_list, list) and isinstance(right_part_of_list, list):
        while (left_part_of_list and right_part_of_list):
            if left_part_of_list[0] < right_part_of_list[0]:
                result.append(left_part_of_list[0])
                left_part_of_list.pop(0)
            else:
                result.append(right_part_of_list[0])
                right_part_of_list.pop(0)

        if left_part_of_list:
            result += left_part_of_list
        if right_part_of_list:
            result += right_part_of_list

    return result

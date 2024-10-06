lst = [1, 2, 3, 4, 5, 6, 3, 4, 5, 7, 6, 5, 4, 3, 4, 5, 4, 3, 'Привіт', 'Анаконда']


def double(lst):
    duplicatee = set()
    result = []
    for item in lst:
        if item not in duplicatee:
            duplicatee.add(item)
            result.append(item)
    return result


def sort_custom(input_list):
    numbers = [item for item in input_list if isinstance(item, (int, float))]
    strings = [item for item in input_list if isinstance(item, str)]
    numbers.sort()
    strings.sort()
    return numbers + strings


first_list = double(lst)
sorted_list = sort_custom(first_list)
print(sorted_list)
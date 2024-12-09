import time
import matplotlib.pyplot as plt
import random


# Сортування вставкою
def insertion_sort(array):
    comparisons = swaps = 0
    for i in range(1, len(array)):
        key, j = array[i], i - 1
        while j >= 0 and array[j] > key:
            comparisons += 1
            array[j + 1] = array[j]
            swaps += 1
            j -= 1
        array[j + 1] = key
        if j >= 0: comparisons += 1
    return comparisons, swaps


# Швидке сортування
def quick_sort(array):
    comparisons = swaps = 0

    def partition(low, high):
        nonlocal comparisons, swaps
        pivot, i = array[high], low - 1
        for j in range(low, high):
            comparisons += 1
            if array[j] <= pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
                swaps += 1
        array[i + 1], array[high] = array[high], array[i + 1]
        swaps += 1
        return i + 1

    def quick_sort_rec(low, high):
        if low < high:
            pi = partition(low, high)
            quick_sort_rec(low, pi - 1)
            quick_sort_rec(pi + 1, high)

    quick_sort_rec(0, len(array) - 1)
    return comparisons, swaps


# Вимірювання часу та побудова графіка
def measure_time_and_plot():
    sizes = [100, 200, 300, 400, 500]
    insertion_times = []
    quick_times = []

    for size in sizes:
        array = list(range(size, 0, -1))  # зворотно відсортований масив

        # Сортування вставкою
        start = time.time()
        insertion_sort(array.copy())
        insertion_times.append(time.time() - start)

        # Швидке сортування
        start = time.time()
        quick_sort(array.copy())
        quick_times.append(time.time() - start)

    # Побудова графіка
    plt.plot(sizes, insertion_times, label="Insertion Sort", marker='o')
    plt.plot(sizes, quick_times, label="Quick Sort", marker='x')
    plt.xlabel('Array size')
    plt.ylabel('Time (seconds)')
    plt.title('Comparison of Insertion Sort and Quick Sort')
    plt.legend()
    plt.show()


# Викликаємо функцію для вимірювання часу та побудови графіка
measure_time_and_plot()

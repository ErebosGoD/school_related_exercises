import time
import random
from memory_profiler import profile


class SortingAlgorithms:
    @staticmethod
    def bubble_sort(arr):
        n = len(arr)
        for pass_num in range(n):
            for i in range(0, n - pass_num - 1):
                current_value = arr[i]
                next_value = arr[i + 1]
                if current_value > next_value:
                    # Tausche Elemente, falls sie in falscher Reihenfolge sind
                    arr[i], arr[i + 1] = next_value, current_value

    @staticmethod
    def quick_sort(arr):
        if len(arr) <= 1:
            return arr

        pivot_index = len(arr) // 2
        pivot = arr[pivot_index]
        left, middle, right = [], [], []

        for value in arr:
            if value < pivot:
                left.append(value)
            elif value == pivot:
                middle.append(value)
            else:
                right.append(value)

        return SortingAlgorithms.quick_sort(left) + middle + SortingAlgorithms.quick_sort(right)

    # @staticmethod
    # def bucket_sort(arr):
    #     if len(arr) == 0:
    #         return arr

    #     # Erstelle 10 Eimer für die Ziffern 0 bis 9
    #     buckets = []
    #     for _ in range(10):
    #         buckets.append([])

    #     # Platziere Werte in den entsprechenden Eimern
    #     for value in arr:
    #         buckets[value].append(value)

    #     # Verbinde die sortierten Eimer zu einer sortierten Liste
    #     sorted_arr = []
    #     for bucket in buckets:
    #         sorted_arr.extend(bucket)

    #     return sorted_arr

    @staticmethod
    @profile
    def measure_time_and_memory(algorithm, data):
        start_time = time.time()
        algorithm(data)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution Time: {execution_time} seconds")


if __name__ == "__main__":
    # Beispiel-Nutzung
    data = [random.randint(1, 1000) for _ in range(10000)]

    # Zeit und Speicher für Bubblesort messen
    SortingAlgorithms.measure_time_and_memory(
        SortingAlgorithms.bubble_sort, data.copy())

    # Zeit und Speicher für Quicksort messen
    SortingAlgorithms.measure_time_and_memory(
        SortingAlgorithms.quick_sort, data.copy())

    # Zeit und Speicher für Bucket Sort messen
    # SortingAlgorithms.measure_time_and_memory(
    #     SortingAlgorithms.bucket_sort, data.copy())

"""
Multiple sorting algorithms implemented in Python.
"""

import random
import time
from typing import Callable


def bubble_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr: list[int]) -> list[int]:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)


def heap_sort(arr: list[int]) -> list[int]:
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0)

    return arr


def _heapify(arr: list[int], n: int, root: int) -> None:
    largest = root
    left = 2 * root + 1
    right = 2 * root + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != root:
        arr[root], arr[largest] = arr[largest], arr[root]
        _heapify(arr, n, largest)


ALGORITHMS: dict[str, Callable[[list[int]], list[int]]] = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
}


def _is_sorted(arr: list[int]) -> bool:
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def run_tests() -> None:
    print("=== Running correctness tests ===\n")

    test_cases = [
        [],
        [1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],
        [-3, 10, -1, 0, 7, -5],
    ]

    for name, algo in ALGORITHMS.items():
        all_pass = True
        for case in test_cases:
            original = case.copy()
            result = algo(case.copy())
            expected = sorted(original)
            if result != expected:
                print(f"  FAIL {name}: {original} -> {result} (expected {expected})")
                all_pass = False
        if all_pass:
            print(f"  PASS {name}")


def run_benchmark() -> None:
    print("\n=== Running benchmark (n=5000) ===\n")

    size = 5000
    data = [random.randint(0, 10000) for _ in range(size)]

    for name, algo in ALGORITHMS.items():
        arr = data.copy()
        start = time.perf_counter()
        result = algo(arr)
        elapsed = time.perf_counter() - start
        assert _is_sorted(result), f"{name} failed to sort"
        print(f"  {name:.<20s} {elapsed:.4f}s")


def main() -> None:
    run_tests()
    run_benchmark()


if __name__ == "__main__":
    main()

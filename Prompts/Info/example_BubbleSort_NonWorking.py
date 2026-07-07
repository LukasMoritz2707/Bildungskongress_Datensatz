def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = True
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = False
        if not swapped:
            break
    return arr


def run_tests():
    test_cases = [
        ([1], [1]),
        ([1, 2, 3, 4], [1, 2, 3, 4]),
        ([5, -1, 0, 5, 2], [-1, 0, 2, 5, 5]),
    ]

    for i, (input_data, expected) in enumerate(test_cases, start=1):
        data = input_data.copy()
        result = bubble_sort(data)
        assert result == expected, f"Test {i} failed: {result} != {expected}"
        print(f"Test {i} passed: {input_data} -> {result}")

    print("Alle Tests bestanden.")

if __name__ == "__main__":
    run_tests()

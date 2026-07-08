def insertion_sort(a):
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key


def is_sorted(a):
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))


# Tests
cases = [
    [1, 2, 3, 4, 5],          # already sorted
    [5, 4, 3, 2, 1],          # reverse sorted
    [3, 1, 2, 3, 1],          # mixed with duplicates
    [],                       # empty
    [7],                      # single element
]

for case in cases:
    original = case.copy()
    insertion_sort(case)
    assert is_sorted(case), f"Failed for {original} -> {case}"
    print(original, "=>", case)

print("All tests passed.")

def partition(array, low, high):
    pivot = array[high]
    i = low - 1

    for j in range(low, high):
        if array[j] <= pivot:
            i += 1
            array[i], array[j] = array[j], array[i]

    array[i+1], array[high] = array[high], array[i+1]
    return i+1

def quicksort(array, low=0, high=None):
    if high is None:
        high = len(array) - 1

    if low < high:
        pivot_index = partition(array, low, high)
        quicksort(array, low, pivot_index-1)
        quicksort(array, pivot_index+1, high)

array = [64, 34, 25, 12, 22, 11, 90, 5]
quicksort(array)
print("Sorted array:", array)
targetValue = 34

def binarySearch(array, targetValue):
    leftIndex = 0
    rightIndex = len(array) - 1

    while leftIndex <= rightIndex:
        currentIndex = (leftIndex + rightIndex) // 2
        if array[currentIndex] == targetValue:
            return currentIndex
        
        if array[currentIndex] < targetValue:
            leftIndex = currentIndex + 1
        else:
            rightIndex = currentIndex - 1

    return -1

result = binarySearch(array, targetValue)

if result != -1:
    print("Value",targetValue,"found at index", result)
else:
    print("Target not found in array.")
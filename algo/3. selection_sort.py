array = [5,32,0,8,6,1]

n = len(array)
for i in range(n-1):
    min_index = i
    for j in range(i+1, n):
        if array[j] < array[min_index]:
            min_index = j
    min_value = array.pop(min_index)
    array.insert(i, min_value)

print(array)

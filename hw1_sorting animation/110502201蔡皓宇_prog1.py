'''
演算法 Programming Assignment 1 
110502201 資工三A 蔡皓宇
'''
import random
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# bubble sort main function
def bubble_sort_animation(data):
    n = len(data)
    global bubble_time
    bubble_time = 0
    for i in range(n-1):
        bubble_start = time.time()
        for j in range(0, n-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
            yield data
        bubble_end = time.time()
        bubble_time += (bubble_end - bubble_start)

# insertion sort main function
def insertion_sort_animation(data):
    n = len(data)
    global insertion_time
    insertion_time = 0
    for i in range(1, n):
        insertion_start = time.time()
        key = data[i]
        j = i-1
        while j >= 0 and data[j] > key:
            data[j+1] = data[j]
            j -= 1
            yield data
        data[j+1] = key
        yield data
        insertion_end = time.time()
        insertion_time += (insertion_end - insertion_start)

# partition function
def partition(data, low, high):
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        if data[j] <= pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
    data[i + 1], data[high] = data[high], data[i + 1]
    return i + 1

# quick sort main function
quick_time = 0
def quick_sort_animation(data, low, high):
    global quick_time
    if low < high:
        quick_start = time.time()
        pivot_index = partition(data, low, high)
        yield data
        yield from quick_sort_animation(data, low, pivot_index - 1)
        yield from quick_sort_animation(data, pivot_index + 1, high)
        quick_end = time.time()
        quick_time += (quick_end - quick_start)

# for building max-heap
def heap_insert(A, data_idx):
    cur_idx = data_idx
    temp = A[data_idx]
    while cur_idx > 1 and temp > A[cur_idx // 2]:
        A[cur_idx] = A[cur_idx // 2]
        cur_idx = cur_idx // 2
    A[cur_idx] = temp

# heap sort main function
def heap_sort_animation(A):
    global heap_time
    heap_time = 0
    # loop : exexcuting heap delete 
    for j in range(len(A) - 1, 0, -1):
        heap_start = time.time()
        max_val = A[1]
        heap_size = j
        A[1], A[heap_size] = A[heap_size], A[1]
        heap_size -= 1
        node_idx = 1;
        child_idx = node_idx * 2
        while child_idx <= heap_size:
            if child_idx + 1 <= heap_size:
                if A[child_idx+1] > A[child_idx]:
                    child_idx += 1;
            if A[node_idx] < A[child_idx]:
                A[node_idx], A[child_idx] = A[child_idx], A[node_idx]
                yield A
                node_idx = child_idx;
                child_idx *= 2;
            else: 
                break
        heap_end = time.time()
        heap_time += (heap_end - heap_start)
        yield A

# merge function
def merge(data, left, mid, right):
    len_left = mid - left + 1
    len_right = right - mid
    L = data[left:mid+1]
    R = data[mid+1:right+1]
    i, j, k = 0, 0, left
    while i < len_left and j < len_right:
        if L[i] <= R[j]:
            data[k] = L[i]
            i += 1
        else: 
            data[k] = R[j]
            j += 1
        k += 1
    while i < len_left:
        data[k] = L[i]
        i += 1
        k += 1
    while j < len_right:
        data[k] = R[j]
        j += 1
        k += 1

# merge sort main function
merge_time = 0
def merge_sort_animation(data, left, right):
    global merge_time
    if left < right:
        merge_start = time.time()
        mid = (left + right) // 2
        yield from merge_sort_animation(data, left, mid)
        yield from merge_sort_animation(data, mid+1, right)
        merge(data, left, mid, right)
        merge_end = time.time()
        merge_time += (merge_end - merge_start)
        yield data

# 1~50 random permutation
data = random.sample(range(1, 51), 50)
# data for heap
heap_data = [0] + data
# set up the figure(2 rows, 3 columns) and the size
fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(15, 6))

# set up the bars for each sorting algorithm
bars_bubble = ax1.bar(range(len(data)), data, color='skyblue')
bars_quick = ax2.bar(range(len(data)), data, color='lightgreen')
bars_insertion = ax3.bar(range(len(data)), data, color='salmon')
bars_merge = ax4.bar(range(len(data)), data, color='lightgrey')
bars_heap = ax5.bar(range(len(heap_data)), heap_data, color='wheat')

### function for updating frames
def update_bubble(data):
    for bar, val in zip(bars_bubble, data):
        bar.set_height(val)
    # update the total sorting time on x-axis
    ax1.set_xlabel(f'Elapsed Time (Bubble Sort): {round(bubble_time, 3)} seconds', fontsize=9)

def update_quick(data):
    for bar, val in zip(bars_quick, data):
        bar.set_height(val)
    # update the total sorting time on x-axis
    ax2.set_xlabel(f'Elapsed Time (Quick Sort): {round(quick_time, 3)} seconds', fontsize=9)

def update_insertion(data):
    for bar, val in zip(bars_insertion, data):
        bar.set_height(val)
    # update the total sorting time on x-axis
    ax3.set_xlabel(f'Elapsed Time (Insertion Sort): {round(insertion_time, 3)} seconds', fontsize=9)

def update_merge(data):
    for bar, val in zip(bars_merge, data):
        bar.set_height(val)
    # update the total sorting time on x-axis
    ax4.set_xlabel(f'Elapsed Time (Merge Sort): {round(merge_time, 3)} seconds', fontsize=9)

def update_heap(data):
    for bar, val in zip(bars_heap, data):
        bar.set_height(val)
    # update the total sorting time on x-axis
    ax5.set_xlabel(f'Elapsed Time (Heap Sort): {round(heap_time, 3)} seconds', fontsize=9)

ax6.set_xlabel(f'Elapsed Time (Empty): {0} seconds', fontsize=9)
### function for updating frames

### animation for respective sorting algorithm
ani_bubble = FuncAnimation(fig, update_bubble, frames=bubble_sort_animation(data.copy()), interval=5, repeat=False)
ani_quick = FuncAnimation(fig, update_quick, frames=quick_sort_animation(data.copy(), 0, len(data) - 1), interval=5, repeat=False)
ani_insertion = FuncAnimation(fig, update_insertion, frames=insertion_sort_animation(data.copy()), interval=5, repeat=False)
ani_merge = FuncAnimation(fig, update_merge, frames=merge_sort_animation(data.copy(), 0, len(data) - 1), interval=5, repeat=False)

# convert heap_data to max-heap
for i in range(1, len(heap_data)):
    heap_insert(heap_data, i)
ani_heap = FuncAnimation(fig, update_heap, frames=heap_sort_animation(heap_data), interval=5, repeat=False)
### animation for respective sorting algorithm

ax1.set_title('Bubble Sort Animation', fontweight='bold')
ax2.set_title('Quick Sort Animation', fontweight='bold')
ax3.set_title('Insertion Sort Animation', fontweight='bold')
ax4.set_title('Merge Sort Animation', fontweight='bold')
ax5.set_title('Heap Sort Animation', fontweight='bold')
ax6.set_title('Empty', fontweight='bold')

# automatically adjust the spaces between bounding boxes
plt.tight_layout()
plt.show()

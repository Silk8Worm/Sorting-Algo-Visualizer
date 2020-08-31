from tkinter import *
import random, time
from win32api import GetSystemMetrics

bars = []
rectangles = []

screen_size = GetSystemMetrics(0), GetSystemMetrics(1)

NUM_BARS = 5
NUM_SORTS = 6
WIDTH = screen_size[0]*.85
HEIGHT = screen_size[1]*.9
BORDER = 30
UNIT_DIM = (min(WIDTH, HEIGHT)-BORDER*6)/NUM_BARS*2

if NUM_BARS >= 300:
    SLEEP_TIME = 0
else:
    SLEEP_TIME = (1/(NUM_BARS+5)-.003)

def draw():
    for i in range(NUM_BARS):
        bars.append(i+1)
        # bars.append(random.randint(1,NUM_BARS))

    for i in range(NUM_BARS):
        rectangles.append(canvas.create_rectangle(BORDER+UNIT_DIM*i, HEIGHT-BORDER, BORDER+UNIT_DIM*i+UNIT_DIM, HEIGHT-BORDER-UNIT_DIM/2*(bars[i]), fill="orange"))

def draw_buttons():
    f1 = Frame(tk, height=HEIGHT/20, width=WIDTH/(NUM_SORTS+1), bg='blue')
    f1.pack_propagate(0)
    f1.pack(side='left')

    f7 = Frame(tk, height=HEIGHT/20, width=WIDTH/(NUM_SORTS+1.5), bg='SeaGreen2')
    f7.pack_propagate(0)
    f7.pack(side='right')

    f6 = Frame(tk, height=HEIGHT/20, width=WIDTH/(NUM_SORTS+1.5), bg='salmon3')
    f6.pack_propagate(0)
    f6.pack(side='right')

    f5 = Frame(tk, height=HEIGHT/20, width=WIDTH/(NUM_SORTS+1.5), bg='SeaGreen2')
    f5.pack_propagate(0)
    f5.pack(side='right')

    f4 = Frame(tk, height=HEIGHT/20, width=WIDTH/(NUM_SORTS+1.5), bg='salmon3')
    f4.pack_propagate(0)
    f4.pack(side='right')

    f3 = Frame(tk, height=HEIGHT/20, width=WIDTH/(NUM_SORTS+1.5), bg='SeaGreen2')
    f3.pack_propagate(0)
    f3.pack(side='right')

    f2 = Frame(tk, height=HEIGHT/20, width=WIDTH/(NUM_SORTS+1.5), bg='salmon3')
    f2.pack_propagate(0)
    f2.pack(side='right')

    randomize_button = Button(f1, text='Randomize', command=lambda: shuffle_one_by_one())
    randomize_button.pack(fill=BOTH, padx=20, pady=10)

    quick_sort_button = Button(f2, text='Quick Sort', command=lambda: quick_sort(0, NUM_BARS-1))
    quick_sort_button.pack(fill=BOTH, padx=20, pady=10)

    heap_sort_button = Button(f3, text='Heap Sort', command=lambda: heap_sort())
    heap_sort_button.pack(fill=BOTH, padx=20, pady=10)

    bubble_sort_button = Button(f4, text='Bubble Sort', command=lambda: bubble_sort())
    bubble_sort_button.pack(fill=BOTH, padx=20, pady=10)

    insertion_sort_button = Button(f5, text='Insertion Sort', command=lambda: insertion_sort())
    insertion_sort_button.pack(fill=BOTH, padx=20, pady=10)

    selection_sort_button = Button(f6, text='Selection Sort', command=lambda: selection_sort())
    selection_sort_button.pack(fill=BOTH, padx=20, pady=10)

    bogo_bogo_sort_button = Button(f7, text='Bogo-Bogo Sort', command=lambda: bogo_bogo_sort())
    bogo_bogo_sort_button.pack(fill=BOTH, padx=20, pady=10)

def switch_rectangles(index1, index2):
    canvas.itemconfig(rectangles[index1], fill='blue2')
    canvas.itemconfig(rectangles[index2], fill='purple2')
    tk.update()
    canvas.move(rectangles[index1], (index2-index1)*UNIT_DIM, 0)
    canvas.move(rectangles[index2], (index1-index2)*UNIT_DIM, 0)
    rectangles[index1], rectangles[index2] = rectangles[index2], rectangles[index1]
    time.sleep(SLEEP_TIME)
    canvas.itemconfig(rectangles[index1], fill='orange')
    canvas.itemconfig(rectangles[index2], fill='orange')
    tk.update()


def shuffle_one_by_one():
    for i in range(NUM_BARS):
        rand_index = random.randint(0,NUM_BARS-1)
        bars[i], bars[rand_index] = bars[rand_index], bars[i]
        switch_rectangles(i, rand_index)

def partition(start, end):
    pivot = bars[start]
    low = start+1
    high = end

    while True:
        while low <= high and bars[high] >= pivot:
            high = high - 1

        while low <= high and bars[low] <= pivot:
            low = low + 1

        if low <= high:
            bars[low], bars[high] = bars[high], bars[low]
            switch_rectangles(low, high)
        else:
            break
    bars[start], bars[high] = bars[high], bars[start]
    switch_rectangles(start, high)

    return high

def quick_sort(start, end):
    if start >= end:
        return

    p = partition(start, end)
    quick_sort(start, p-1)
    quick_sort(p+1, end)

def insertion_sort():
    for i in range(1, NUM_BARS):
        curr = bars[i]
        j = i-1
        while j >= 0 and curr < bars[j]:
            bars[j+1] = bars[j]
            switch_rectangles(j+1, j)
            j -= 1
        bars[j+1] = curr

def selection_sort():
    for i in range(NUM_BARS):
        min_index = i
        for j in range(i+1, NUM_BARS):
            if bars[min_index] > bars[j]:
                min_index = j
        bars[i], bars[min_index] = bars[min_index], bars[i]
        switch_rectangles(i, min_index)

def bubble_sort():
    for curr in range(NUM_BARS-1, 0, -1):
        for i in range(curr):
            if bars[i] > bars[i+1]:
                bars[i], bars[i+1] = bars[i+1], bars[i]
                switch_rectangles(i, i+1)

def heap(n, i):
    largest = i
    l = 2*i+1
    r = 2*i+2

    if l < n and bars[i] < bars[l]:
        largest = l

    if r < n and bars[largest] < bars[r]:
        largest = r

    if largest != i:
        bars[i], bars[largest] = bars[largest], bars[i]
        switch_rectangles(i, largest)
        heap(n, largest)

def heap_sort():
    for i in range(NUM_BARS//2-1, -1, -1):
        heap(NUM_BARS, i)

    for i in range(NUM_BARS-1, 0, -1):
        bars[i], bars[0] = bars[0], bars[i]
        switch_rectangles(0, i)
        heap(i, 0)

def bogo_bogo_sort():
    for i in range(1, NUM_BARS):
        bogo_sort(i)

def bogo_sort(index_plus_one):
    for i in range(0, index_plus_one):
        rand_ind = random.randint(0, index_plus_one)
        bars[i], bars[rand_ind] = bars[rand_ind], bars[i]
        switch_rectangles(i, rand_ind)

    if bars[0:index_plus_one] != sorted(bars[0:index_plus_one]):
        bogo_sort(index_plus_one)


if __name__ == '__main__':

    num_swaps = 0

    tk = Tk()
    canvas = Canvas(tk, width=WIDTH, height=HEIGHT)
    tk.title("Sorting Visualizer")
    canvas.pack()

    draw()
    draw_buttons()

    tk.mainloop()

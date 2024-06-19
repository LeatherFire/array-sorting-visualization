import time
import tkinter as tk
import random
import pygame
from tkinter import simpledialog

# Pencere oluşturma
window = tk.Tk()
window.title("Array Sorting Visualization")
window.configure(bg='black')

# Pygame'i başlat ve ses modülünü başlat
pygame.init()
pygame.mixer.init()
sound = pygame.mixer.Sound('beep.wav')


canvas_width = 800
canvas_height = 600
columns = []
equal_heights_var = None
num_columns_var = None

# Ekran boyutları
canvas_width = 800
canvas_height = 600
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='black')
canvas.pack()

# Sıralama zamanını göstermek için bir etiket
time_label = tk.Label(window, text="", bg='black', fg='white')
time_label.pack()

def show_time_taken(start_time):
    end_time = time.time()
    time_taken = end_time - start_time
    time_label.config(text=f"Time: {time_taken:.4f} seconds")


# Yükseklik etiketi
height_label = tk.Label(window, text="", bg='black', fg='white')
height_label.pack()

# Varsayılan sütun sayısı
num_columns = 267

# Başlangıç ayarları penceresi
def open_settings_window():
    settings_window = tk.Toplevel(window)
    settings_window.title("Settings")
    settings_window.geometry("300x200")
    settings_window.configure(bg='black')
    
    global equal_heights_var, num_columns_var
    
    equal_heights_var = tk.BooleanVar(value=True)
    num_columns_var = tk.IntVar(value=num_columns)
    
    tk.Label(settings_window, text="Column Has Equal Heights ?", bg='black', fg='white').pack(pady=5)
    tk.Checkbutton(settings_window, variable=equal_heights_var, bg='black', fg='white').pack()
    
    tk.Label(settings_window, text="Column Count", bg='black', fg='white').pack(pady=5)
    tk.Spinbox(settings_window, from_=20, to=267, textvariable=num_columns_var, bg='white').pack(pady=5)
    
    tk.Button(settings_window, text="Set", command=apply_settings).pack(pady=10)
    
def apply_settings():
    global num_columns, columns
    num_columns = num_columns_var.get()
    reset_columns()


# Fare hareketi olayı
def on_mouse_move(event):
    x, y = event.x, event.y
    highlighted = False
    for rect, height in columns:
        coords = canvas.coords(rect)
        if coords[0] <= x <= coords[2] and not highlighted:
            canvas.itemconfig(rect, fill='green')
            height_label.config(text=f"Height: {height}")
            highlighted = True
        else:
            canvas.itemconfig(rect, fill='white')

    if not highlighted:
        height_label.config(text="")

canvas.bind('<Motion>', on_mouse_move)

# Insertion Sort
def sort_columns():
    start_time = time.time()  # Zaman ölçümünü başlat
    for i in range(1, len(columns)):
        rect, height = columns[i]
        j = i - 1
        while j >= 0 and columns[j][1] > height:
            canvas.itemconfig(columns[j][0], fill='green')
            canvas.update_idletasks()  # Güncelleme işlemi
            canvas.itemconfig(columns[j][0], fill='white')
            sound.play()
            columns[j + 1] = columns[j]
            j -= 1
        columns[j + 1] = (rect, height)
        # Yeniden çizim
        for k in range(i + 1):
            r, h = columns[k]
            x = k * (column_width + column_spacing)
            canvas.coords(r, x, canvas_height - h, x + column_width, canvas_height)
        time.sleep(0.05)
        canvas.update_idletasks()  # Güncelleme işlemi
    show_time_taken(start_time)  # Zaman ölçümünü göster
# Bubble Sort
def bubble_sort():
    start_time = time.time()  # Zaman ölçümünü başlat
    n = len(columns)
    for i in range(n):
        for j in range(0, n-i-1):
            if columns[j][1] > columns[j+1][1]:
                canvas.itemconfig(columns[j][0], fill='green')
                canvas.itemconfig(columns[j+1][0], fill='green')
                columns[j], columns[j+1] = columns[j+1], columns[j]
                canvas.update_idletasks()
                sound.play()
                canvas.itemconfig(columns[j][0], fill='white')
                canvas.itemconfig(columns[j+1][0], fill='white')
        # Yeniden çizim
        for k in range(n):
            r, h = columns[k]
            x = k * (column_width + column_spacing)
            canvas.coords(r, x, canvas_height - h, x + column_width, canvas_height)
        canvas.update_idletasks()
        time.sleep(0.05)
    show_time_taken(start_time)  # Zaman ölçümünü göster
# Selection Sort
def selection_sort():
    start_time = time.time()  # Zaman ölçümünü başlat
    n = len(columns)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if columns[j][1] < columns[min_idx][1]:
                min_idx = j
        canvas.itemconfig(columns[min_idx][0], fill='green')
        canvas.itemconfig(columns[i][0], fill='green')
        columns[i], columns[min_idx] = columns[min_idx], columns[i]
        canvas.update_idletasks()
        sound.play()
        canvas.itemconfig(columns[min_idx][0], fill='white')
        canvas.itemconfig(columns[i][0], fill='white')
        # Yeniden çizim
        for k in range(n):
            r, h = columns[k]
            x = k * (column_width + column_spacing)
            canvas.coords(r, x, canvas_height - h, x + column_width, canvas_height)
        canvas.update_idletasks()
        time.sleep(0.05)
    show_time_taken(start_time)  # Zaman ölçümünü göster
# Merge Sort
def merge_sort(columns, l, r):
    start_time = time.time()  # Zaman ölçümünü başlat
    _merge_sort(columns, l, r)
    show_time_taken(start_time)  # Zaman ölçümünü göster
def _merge_sort(columns, l, r):
    if l < r:
        m = (l + r) // 2
        _merge_sort(columns, l, m)
        _merge_sort(columns, m+1, r)
        merge(columns, l, m, r)
        # Yeniden çizim
        for k in range(len(columns)):
            r, h = columns[k]
            x = k * (column_width + column_spacing)
            canvas.coords(r, x, canvas_height - h, x + column_width, canvas_height)
        canvas.update_idletasks()
        time.sleep(0.05)
def merge(columns, l, m, r):
    n1 = m - l + 1
    n2 = r - m
    L = columns[l:m+1]
    R = columns[m+1:r+1]
    i, j, k = 0, 0, l
    while i < n1 and j < n2:
        if L[i][1] <= R[j][1]:
            columns[k] = L[i]
            i += 1
        else:
            columns[k] = R[j]
            j += 1
        k += 1
        sound.play()  # Ses çalma işlemi
    while i < n1:
        columns[k] = L[i]
        i += 1
        k += 1
        sound.play()  # Ses çalma işlemi
    while j < n2:
        columns[k] = R[j]
        j += 1
        k += 1
        sound.play()  # Ses çalma işlemi
# Quick Sort
def quick_sort(columns, low, high):
    start_time = time.time()  # Zaman ölçümünü başlat
    _quick_sort(columns, low, high)
    show_time_taken(start_time)  # Zaman ölçümünü göster
def _quick_sort(columns, low, high):
    if low < high:
        pi = partition(columns, low, high)
        _quick_sort(columns, low, pi-1)
        _quick_sort(columns, pi+1, high)
        # Yeniden çizim
        for k in range(len(columns)):
            r, h = columns[k]
            x = k * (column_width + column_spacing)
            canvas.coords(r, x, canvas_height - h, x + column_width, canvas_height)
        canvas.update_idletasks()
        time.sleep(0.05)
def partition(columns, low, high):
    pivot = columns[high]
    i = low - 1
    for j in range(low, high):
        if columns[j][1] <= pivot[1]:
            i += 1
            columns[i], columns[j] = columns[j], columns[i]
            sound.play()  # Ses çalma işlemi
    columns[i+1], columns[high] = columns[high], columns[i+1]
    sound.play()  # Ses çalma işlemi
    return i + 1
def reset_columns():
    global columns, column_width, column_spacing
    canvas.delete("all")
    columns = []
    heights = set()
    
    # Sütun genişliği ve aralık ayarları
    total_width = canvas_width - (num_columns - 1)  # Toplam genişlik
    column_width = total_width // num_columns
    column_spacing = 1
    
    for i in range(num_columns):
        x = i * (column_width + column_spacing)
        if not equal_heights_var.get():
            height = random.randint(10, canvas_height)
            while height in heights:
                height = random.randint(10, canvas_height)
            heights.add(height)
        else:
            height = random.randint(10, canvas_height)
        
        rect = canvas.create_rectangle(x, canvas_height - height, x + column_width, canvas_height, fill='white')
        columns.append((rect, height))
    canvas.update_idletasks()


# Buton çerçevesi
button_frame = tk.Frame(window, bg='black')
button_frame.pack()

# Sıralama butonları
sort_button = tk.Button(button_frame, text="Insertion Sort", command=sort_columns)
sort_button.pack(side=tk.LEFT, padx=5)

bubble_sort_button = tk.Button(button_frame, text="Bubble Sort", command=bubble_sort)
bubble_sort_button.pack(side=tk.LEFT, padx=5)

selection_sort_button = tk.Button(button_frame, text="Selection Sort", command=selection_sort)
selection_sort_button.pack(side=tk.LEFT, padx=5)

merge_sort_button = tk.Button(button_frame, text="Merge Sort", command=lambda: merge_sort(columns, 0, len(columns)-1))
merge_sort_button.pack(side=tk.LEFT, padx=5)

quick_sort_button = tk.Button(button_frame, text="Quick Sort", command=lambda: quick_sort(columns, 0, len(columns)-1))
quick_sort_button.pack(side=tk.LEFT, padx=5)

reset_button = tk.Button(button_frame, text="Reset", command=reset_columns)
reset_button.pack(side=tk.LEFT, padx=5)

# Başlangıçta ayar penceresini aç
window.after(100, open_settings_window)

# Pencereyi çalıştır
window.mainloop()

pygame.quit()

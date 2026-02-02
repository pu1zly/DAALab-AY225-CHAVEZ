import csv
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

file_path = ""
cancel_sort = False
sort_thread = None

# ---------- SORTING ALGORITHMS ----------
def bubble_sort(arr, key):
    n = len(arr)
    for i in range(n):
        if cancel_sort:
            return
        for j in range(0, n - i - 1):
            if cancel_sort:
                return
            if arr[j][key] > arr[j + 1][key]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
        progress_var.set((i + 1) / n * 100)
        root.update_idletasks()

def insertion_sort(arr, key):
    n = len(arr)
    for i in range(1, n):
        if cancel_sort:
            return
        current = arr[i]
        j = i - 1
        while j >= 0 and arr[j][key] > current[key]:
            if cancel_sort:
                return
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
        progress_var.set((i + 1) / n * 100)
        root.update_idletasks()

def merge_sort(arr, key):
    if cancel_sort or len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    merged = merge(left, right, key)
    progress_var.set(min(progress_var.get() + (100 / total_rows), 100))
    root.update_idletasks()
    return merged

def merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if cancel_sort:
            return []
        if left[i][key] <= right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    if cancel_sort:
        return []
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# ---------- LOAD CSV ----------
def load_csv(file_path, n):
    data = []
    with open(file_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= n:
                break
            row["ID"] = int(row["ID"])
            data.append(row)
    return data

# ---------- GUI FUNCTIONS ----------
def choose_file():
    global file_path
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv")]
    )
    file_label.config(text=file_path if file_path else "No file selected")

def cancel_operation():
    global cancel_sort
    cancel_sort = True
    status_label.config(text="Status: Cancelled!", fg="#d32f2f")
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "CANCELLED!\n")
    output_text.config(state=tk.DISABLED)

def run_sort_threaded():
    global sort_thread
    if sort_thread and sort_thread.is_alive():
        return  # already sorting
    sort_thread = threading.Thread(target=run_sort)
    sort_thread.start()

def run_sort():
    global cancel_sort, total_rows
    cancel_sort = False
    status_label.config(fg="#000000")

    if not file_path:
        messagebox.showerror("Error", "Please select a CSV file.")
        return

    try:
        total_rows = int(n_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number for N.")
        return

    key = column_var.get()
    algo = algo_var.get()

    if algo in ["Bubble Sort", "Insertion Sort"] and total_rows > 10000:
        messagebox.showwarning("Warning", "O(n²) algorithm selected. This may take a long time.")

    progress_var.set(0)
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    status_label.config(text="Status: Loading data...")
    performance_label.config(text="")

    start_load = time.time()
    data = load_csv(file_path, total_rows)
    end_load = time.time()

    if cancel_sort:
        cancel_operation()
        return

    status_label.config(text="Status: Sorting...")
    start_sort = time.time()

    if algo == "Bubble Sort":
        bubble_sort(data, key)
    elif algo == "Insertion Sort":
        insertion_sort(data, key)
    elif algo == "Merge Sort":
        data = merge_sort(data, key)

    end_sort = time.time()

    if cancel_sort:
        cancel_operation()
        return

    progress_var.set(100)
    status_label.config(text="Status: Done", fg="#388e3c")

    performance_label.config(text=
        f"Load Time: {end_load - start_load:.4f}s | "
        f"Sort Time: {end_sort - start_sort:.4f}s | "
        f"Total: {(end_sort - start_load):.4f}s"
    )

    # Output first 10 rows
    output_text.insert(tk.END, f"First 10 sorted values ({key}):\n\n")
    for row in data[:10]:
        output_text.insert(tk.END, f"{row[key]}\n")
    output_text.config(state=tk.DISABLED)

# ---------- GUI SETUP ----------
root = tk.Tk()
root.title("Sorting Algorithm Stress Test")
root.geometry("950x650")
root.resizable(False, False)
root.config(bg="#f5f5f5")  # Light gray background

# ---------- Frames ----------
top_frame = tk.Frame(root, bg="#f5f5f5", pady=10)
top_frame.pack(fill=tk.X)

# File selection frame
file_frame = tk.Frame(top_frame, bg="#f5f5f5")
file_frame.pack(fill=tk.X, pady=5)
tk.Button(file_frame, text="Select CSV File", bg="#1976d2", fg="white", command=choose_file, width=16).pack(side=tk.LEFT, padx=10)
file_label = tk.Label(file_frame, text="No file selected", anchor="w", bg="#f5f5f5")
file_label.pack(side=tk.LEFT, padx=10)

# Options frame
options_frame = tk.Frame(top_frame, bg="#f5f5f5")
options_frame.pack(fill=tk.X, pady=5)
tk.Label(options_frame, text="Column:", bg="#f5f5f5").pack(side=tk.LEFT, padx=(10,5))
column_var = tk.StringVar(value="ID")
tk.OptionMenu(options_frame, column_var, "ID", "FirstName", "LastName").pack(side=tk.LEFT, padx=5)
tk.Label(options_frame, text="Algorithm:", bg="#f5f5f5").pack(side=tk.LEFT, padx=(20,5))
algo_var = tk.StringVar(value="Merge Sort")
tk.OptionMenu(options_frame, algo_var, "Bubble Sort", "Insertion Sort", "Merge Sort").pack(side=tk.LEFT, padx=5)
tk.Label(options_frame, text="Rows (N):", bg="#f5f5f5").pack(side=tk.LEFT, padx=(20,5))
n_entry = tk.Entry(options_frame, width=8)
n_entry.pack(side=tk.LEFT, padx=5)

# Buttons frame
buttons_frame = tk.Frame(top_frame, bg="#f5f5f5")
buttons_frame.pack(fill=tk.X, pady=5)
tk.Button(buttons_frame, text="Run Sort", bg="#388e3c", fg="white", command=run_sort_threaded, width=16).pack(side=tk.LEFT, padx=10)
tk.Button(buttons_frame, text="Cancel", bg="#d32f2f", fg="white", command=cancel_operation, width=16).pack(side=tk.LEFT, padx=10)

# Progress frame
progress_frame = tk.Frame(root, bg="#f5f5f5", pady=10)
progress_frame.pack(fill=tk.X)
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100, length=650)
progress_bar.pack(side=tk.LEFT, padx=10)
progress_percent = tk.Label(progress_frame, text="0%", bg="#f5f5f5")
progress_percent.pack(side=tk.LEFT)
def update_percent(*args):
    progress_percent.config(text=f"{int(progress_var.get())}%")
progress_var.trace_add("write", update_percent)

# Status & Performance
status_frame = tk.Frame(root, bg="#f5f5f5", pady=5)
status_frame.pack(fill=tk.X)
status_label = tk.Label(status_frame, text="Status: Idle", font=("Arial", 11, "bold"), bg="#f5f5f5")
status_label.pack(anchor="w", padx=10)
performance_label = tk.Label(status_frame, text="", font=("Arial", 10), bg="#f5f5f5")
performance_label.pack(anchor="w", padx=10)

# Output frame with scrollbar
output_frame = tk.Frame(root, bg="#f5f5f5", pady=10, padx=10)
output_frame.pack(fill=tk.BOTH, expand=True)
output_text = tk.Text(output_frame, height=20, width=100, wrap=tk.NONE)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
output_text.config(state=tk.DISABLED)

total_rows = 0
root.mainloop()

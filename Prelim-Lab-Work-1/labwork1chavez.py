import time
import os
import sys

# Make stdout unbuffered (forces printing)
sys.stdout.reconfigure(line_buffering=True)

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "dataset.txt")

# Read dataset
with open(file_path, "r") as file:
    data = [int(line.strip()) for line in file]

n = len(data)

start_time = time.time()

# Bubble Sort (Descending)
for i in range(n):
    swapped = False
    for j in range(0, n - i - 1):
        if data[j] < data[j + 1]:
            data[j], data[j + 1] = data[j + 1], data[j]
            swapped = True
    if not swapped:
        break

end_time = time.time()
time_spent = end_time - start_time

# Display summary
print(f"Total elements sorted: {n}")
print(f"Time spent: {time_spent:.4f} seconds")
print("\nSorted data (Descending Order, showing up to 1000 elements):")

# Print up to 1000 elements
max_display = 1000
for value in data[:max_display]:
    print(value, flush=True)

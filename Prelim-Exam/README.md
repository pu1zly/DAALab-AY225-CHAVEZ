# Sorting Algorithm Stress Test GUI

## Overview

This is a **Sorting Algorithm Stress Test GUI** built in **Python**. It benchmarks three sorting algorithms on structured CSV datasets with columns: `ID`, `FirstName`, `LastName`.  

It demonstrates the performance difference between **O(n²)** algorithms (Bubble Sort, Insertion Sort) and **O(n log n)** Merge Sort, while providing a clean, dark-themed interface.

---

## Features

- **Column Selection**: `ID`, `FirstName`, `LastName`  
- **Sorting Algorithm Selection**: Bubble Sort, Insertion Sort, Merge Sort  
- **Progress Bar**: Live sorting progress with percentage  
- **Cancel Sorting**: Instantly terminate sorting if it's taking too long  
- **Performance Metrics**: Load time, sort time, total execution time  
- **Output**: First 10 rows of sorted results, scrollable text box  

---

## Requirements

- Python 3.x  
- Standard libraries only: `tkinter`, `csv`, `time`, `threading`  
- No additional packages needed  

---

## Usage

1. **Open the project in VSCode**  
   - Make sure `sorting_gui.py` and your CSV file (optional) are in the project folder.  

2. **Select Python Interpreter**  
   - Press `Ctrl+Shift+P` → type `Python: Select Interpreter` → choose Python 3.x  

3. **Run the GUI**  
   - Press `F5` or right-click `sorting_gui.py` → **Run Python File in Terminal**  

4. **Select CSV File**  
   - Click **“Select CSV File”** and pick your CSV file  

5. **Select Column**  
   - Choose which column to sort: `ID`, `FirstName`, or `LastName`  

6. **Select Algorithm**  
   - Choose Bubble Sort, Insertion Sort, or Merge Sort   

7. **Set Row Limit (N)**  
   - Enter how many rows to sort (e.g., `1000`, `10000`)  

8. **Run Sort**  
   - Click **Run Sort** to start sorting  
   - Watch the progress bar and percentage  

9. **Cancel Sort (if needed)**  
   - Click **Cancel** to stop instantly  
   - Output box will show **CANCELLED!**  

10. **View Results**  
    - The first 10 sorted rows of the selected column will be displayed  
    - Performance metrics appear under the status label  

---

## Notes

- Sorting algorithms are **implemented from scratch**; no built-in `.sort()` or `sorted()` is used  
- Bubble Sort and Insertion Sort can be slow on large datasets  

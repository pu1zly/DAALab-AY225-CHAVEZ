import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import time
import threading
import os

# BUBBLE SORT
def bubble_sort(arr):
    """Bubble Sort Algorithm"""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


# INSERTION SORT
def insertion_sort(arr):
    """Insertion Sort Algorithm"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# MERGE SORT
def merge_sort(arr):
    """Merge Sort Algorithm"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)


def merge(left, right):
    """Merge two sorted arrays"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# LOAD DATASET
def load_dataset(filename):
    """Load dataset from file"""
    try:
        with open(filename, 'r') as file:
            data = [int(line.strip()) for line in file]
        return data
    except FileNotFoundError:
        return None
    except ValueError:
        return None


class SortingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Performance Analyzer")
        self.root.geometry("900x750")
        self.root.configure(bg="#f0f0f0")
        
        # Current dataset file
        self.current_file = None
        self.data = None
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#f0f0f0')
        self.style.configure('Info.TLabel', font=('Arial', 10), background='#f0f0f0')
        
        # Create UI
        self.create_ui()
        
    def create_ui(self):
        """Create the GUI layout"""
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50")
        title_frame.pack(fill=tk.X, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="🔀 SORTING ALGORITHM ANALYZER",
            font=('Arial', 16, 'bold'),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=10)
        
        # Info Frame
        info_frame = ttk.LabelFrame(self.root, text="Dataset Information", padding=10)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        info_text = "Total Numbers in Dataset: 0 | No dataset loaded"
        self.info_label = ttk.Label(info_frame, text=info_text, font=('Arial', 10))
        self.info_label.pack()
        
        file_info_text = "Current File: None"
        self.file_label = ttk.Label(info_frame, text=file_info_text, font=('Arial', 9, 'italic'), foreground="gray")
        self.file_label.pack()
        
        # File Management Frame
        file_frame = ttk.LabelFrame(self.root, text="File Management", padding=10)
        file_frame.pack(fill=tk.X, padx=20, pady=5)
        
        btn_add = tk.Button(
            file_frame,
            text="📁 Add File",
            font=('Arial', 10, 'bold'),
            bg="#9b59b6",
            fg="white",
            padx=15,
            pady=8,
            command=self.add_file,
            cursor="hand2"
        )
        btn_add.pack(side=tk.LEFT, padx=5)
        
        btn_remove = tk.Button(
            file_frame,
            text="❌ Remove File",
            font=('Arial', 10, 'bold'),
            bg="#c0392b",
            fg="white",
            padx=15,
            pady=8,
            command=self.remove_file,
            cursor="hand2"
        )
        btn_remove.pack(side=tk.LEFT, padx=5)
        
        # Buttons Frame
        button_frame = ttk.LabelFrame(self.root, text="Sorting Algorithms", padding=10)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Button grid
        btn_bubble = tk.Button(
            button_frame,
            text="🔵 Bubble Sort",
            font=('Arial', 11, 'bold'),
            bg="#3498db",
            fg="white",
            padx=15,
            pady=10,
            command=lambda: self.run_sort("bubble"),
            cursor="hand2"
        )
        btn_bubble.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        btn_insertion = tk.Button(
            button_frame,
            text="🟢 Insertion Sort",
            font=('Arial', 11, 'bold'),
            bg="#2ecc71",
            fg="white",
            padx=15,
            pady=10,
            command=lambda: self.run_sort("insertion"),
            cursor="hand2"
        )
        btn_insertion.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        btn_merge = tk.Button(
            button_frame,
            text="🟡 Merge Sort",
            font=('Arial', 11, 'bold'),
            bg="#f39c12",
            fg="white",
            padx=15,
            pady=10,
            command=lambda: self.run_sort("merge"),
            cursor="hand2"
        )
        btn_merge.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        btn_compare = tk.Button(
            button_frame,
            text="⚡ Compare All",
            font=('Arial', 11, 'bold'),
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=10,
            command=self.compare_all,
            cursor="hand2"
        )
        btn_compare.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        btn_clear = tk.Button(
            button_frame,
            text="🗑️ Clear",
            font=('Arial', 11, 'bold'),
            bg="#95a5a6",
            fg="white",
            padx=15,
            pady=10,
            command=self.clear_results,
            cursor="hand2"
        )
        btn_clear.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        
        # Configure column weights
        for i in range(5):
            button_frame.columnconfigure(i, weight=1)
        
        # Results Frame
        results_frame = ttk.LabelFrame(self.root, text="Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrolled Text Widget
        self.output_text = scrolledtext.ScrolledText(
            results_frame,
            font=('Courier', 10),
            bg="white",
            fg="#2c3e50",
            height=15
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for styling
        self.output_text.tag_configure("header", font=('Courier', 11, 'bold'), foreground="#2c3e50")
        self.output_text.tag_configure("success", foreground="#27ae60")
        self.output_text.tag_configure("time", foreground="#e74c3c", font=('Courier', 10, 'bold'))
        self.output_text.tag_configure("info", foreground="#3498db")
        
        # Initial message
        self.output_text.insert(tk.END, "Welcome to Sorting Algorithm Analyzer!\n", "header")
        self.output_text.insert(tk.END, "Click a button to run a sorting algorithm.\n", "info")
        self.output_text.config(state=tk.DISABLED)
        
        # Status Bar
        status_frame = tk.Frame(self.root, bg="#34495e")
        status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=('Arial', 9),
            bg="#34495e",
            fg="white",
            padx=10,
            pady=5
        )
        self.status_label.pack(anchor=tk.W)
    
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update()
    
    def append_output(self, text, tag="info"):
        """Append text to output"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text, tag)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.root.update()
    
    def clear_results(self):
        """Clear output text"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.update_status("Ready")
    
    def run_sort(self, sort_type):
        """Run sorting algorithm in a separate thread"""
        if self.data is None or len(self.data) == 0:
            messagebox.showwarning("No Dataset", "Please load a dataset first using 'Add File'")
            return
        
        thread = threading.Thread(target=self._run_sort_thread, args=(sort_type,))
        thread.daemon = True
        thread.start()
    
    def _run_sort_thread(self, sort_type):
        """Execute sort in thread"""
        self.update_status(f"Running {sort_type.capitalize()} Sort...")
        
        self.append_output(f"\n{'='*60}\n", "header")
        self.append_output(f"Running {sort_type.upper()} SORT\n", "header")
        self.append_output(f"{'='*60}\n", "header")
        
        data_copy = self.data.copy()
        
        try:
            start_time = time.time()
            
            if sort_type == "bubble":
                bubble_sort(data_copy)
            elif sort_type == "insertion":
                insertion_sort(data_copy)
            elif sort_type == "merge":
                data_copy = merge_sort(data_copy)
            
            elapsed = time.time() - start_time
            
            self.append_output(f"Status: ✓ COMPLETED\n", "success")
            self.append_output(f"\nAll Sorted Elements (Descending):\n", "header")
            self.append_output(f"{'-'*60}\n", "info")
            
            # Display all elements in descending order, formatted in rows
            data_descending = sorted(data_copy, reverse=True)
            for i in range(0, len(data_descending), 20):
                row = data_descending[i:i+20]
                self.append_output(f"{str(row)[1:-1]}\n", "info")
            
            self.append_output(f"{'-'*60}\n", "info")
            self.append_output(f"Time Taken: ", "info")
            self.append_output(f"{elapsed:.6f} seconds\n", "time")
            self.append_output(f"Dataset Size: {len(data_copy)} numbers\n\n", "info")
            
            self.update_status(f"✓ {sort_type.capitalize()} Sort completed in {elapsed:.6f} seconds")
            
        except Exception as e:
            self.append_output(f"Error: {str(e)}\n", "error")
            self.update_status("Error occurred")
    
    def compare_all(self):
        """Compare all algorithms in a separate thread"""
        if self.data is None or len(self.data) == 0:
            messagebox.showwarning("No Dataset", "Please load a dataset first using 'Add File'")
            return
        
        thread = threading.Thread(target=self._compare_all_thread)
        thread.daemon = True
        thread.start()
    
    def _compare_all_thread(self):
        """Execute comparison in thread"""
        self.update_status("Comparing all algorithms...")
        
        self.append_output(f"\n{'='*60}\n", "header")
        self.append_output(f"COMPARING ALL ALGORITHMS\n", "header")
        self.append_output(f"{'='*60}\n", "header")
        
        times = {}
        
        # Bubble Sort
        self.append_output("Running Bubble Sort", "info")
        data_copy = self.data.copy()
        start_time = time.time()
        bubble_sort(data_copy)
        times['Bubble Sort'] = time.time() - start_time
        self.append_output(f" → {times['Bubble Sort']:.6f}s\n", "time")
        
        # Insertion Sort
        self.append_output("Running Insertion Sort", "info")
        data_copy = self.data.copy()
        start_time = time.time()
        insertion_sort(data_copy)
        times['Insertion Sort'] = time.time() - start_time
        self.append_output(f" → {times['Insertion Sort']:.6f}s\n", "time")
        
        # Merge Sort
        self.append_output("Running Merge Sort", "info")
        data_copy = self.data.copy()
        start_time = time.time()
        data_copy = merge_sort(data_copy)
        times['Merge Sort'] = time.time() - start_time
        self.append_output(f" → {times['Merge Sort']:.6f}s\n", "time")
        
        # Results Summary
        self.append_output(f"\n{'-'*60}\n", "info")
        self.append_output(f"PERFORMANCE SUMMARY\n", "header")
        self.append_output(f"{'-'*60}\n", "info")
        
        for name, time_taken in sorted(times.items(), key=lambda x: x[1]):
            self.append_output(f"  {name:<20} {time_taken:.6f} seconds\n", "info")
        
        fastest = min(times, key=times.get)
        slowest = max(times, key=times.get)
        speedup = times[slowest] / times[fastest]
        
        self.append_output(f"\n{'-'*60}\n", "info")
        self.append_output(f"⚡ Fastest: ", "header")
        self.append_output(f"{fastest} ({times[fastest]:.6f}s)\n", "time")
        self.append_output(f"🐢 Slowest: ", "header")
        self.append_output(f"{slowest} ({times[slowest]:.6f}s)\n", "time")
        self.append_output(f"Speedup: ", "header")
        self.append_output(f"{speedup:.2f}x faster\n\n", "time")
        
        self.update_status(f"✓ Comparison complete. Fastest: {fastest}")
    
    def add_file(self):
        """Open file dialog to add a new dataset file"""
        file_path = filedialog.askopenfilename(
            title="Select a dataset file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            # Load the selected file
            data = load_dataset(file_path)
            
            if data is None:
                messagebox.showerror("Error", f"Cannot load file or invalid format:\n{file_path}")
                return
            
            if len(data) == 0:
                messagebox.showerror("Error", "File is empty!")
                return
            
            # Update dataset
            self.data = data
            self.current_file = file_path
            
            # Update UI
            info_text = f"Total Numbers in Dataset: {len(self.data)} | First 5 Elements: {self.data[:5]} | Last 5 Elements: {self.data[-5:]}"
            self.info_label.config(text=info_text)
            
            file_info_text = f"Current File: {os.path.basename(file_path)}"
            self.file_label.config(text=file_info_text)
            
            self.append_output(f"\n✓ Dataset loaded successfully!\n", "success")
            self.append_output(f"File: {os.path.basename(file_path)}\n", "info")
            self.append_output(f"Total numbers: {len(self.data)}\n\n", "info")
            
            self.update_status(f"✓ Loaded: {os.path.basename(file_path)} ({len(self.data)} numbers)")
    
    def remove_file(self):
        """Remove current dataset"""
        if self.data is None or len(self.data) == 0:
            messagebox.showinfo("Info", "No dataset is currently loaded")
            return
        
        # Clear the dataset
        self.data = None
        self.current_file = None
        
        # Update UI
        self.info_label.config(text="Total Numbers in Dataset: 0 | No dataset loaded")
        self.file_label.config(text="Current File: None")
        
        self.append_output(f"\n✓ Dataset removed!\n", "success")
        self.append_output(f"No dataset is currently loaded.\n", "info")
        self.append_output(f"Use 'Add File' to load a new dataset.\n\n", "info")
        
        self.update_status(f"✓ Dataset removed. Use 'Add File' to load a new dataset.")


def main():
    root = tk.Tk()
    app = SortingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

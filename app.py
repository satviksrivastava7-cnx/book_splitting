import tkinter as tk
from tkinter import filedialog, ttk
import os
from extract import process_books_in_directory
from helper import process_txt_files
from process import organize_books
from postprocess import create_syllabus_json 
import traceback

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("BrightClass AI Data Pre-Processor")
        self.root.geometry("560x720")
        self.create_widgets()

    def create_widgets(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10, padx=10, fill="x")

        self.source_dir_label = tk.Label(input_frame, text="Select Source Directory:", anchor="w")
        self.source_dir_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.source_dir_dropdown = ttk.Combobox(input_frame, width=40, state="readonly")
        self.source_dir_dropdown.grid(row=1, column=0, padx=5, pady=10, sticky="w")

        self.source_dir_button = tk.Button(input_frame, text="Browse", command=self.browse_source_directory)
        self.source_dir_button.grid(row=1, column=1, padx=5, pady=10)

        self.dest_dir_label = tk.Label(input_frame, text="Enter Destination Directory Name:", anchor="w")
        self.dest_dir_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.dest_dir_dropdown = ttk.Combobox(input_frame, width=40, state="normal")
        self.dest_dir_dropdown.grid(row=4, column=0, padx=5, pady=10, sticky="w")

        self.dest_dir_button = tk.Button(input_frame, text="Browse", command=self.browse_dest_directory)
        self.dest_dir_button.grid(row=4, column=1, padx=5, pady=10)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_process, bg="green", fg="black")
        self.start_button.pack(anchor="center", pady=10, padx=5)

        self.progress_label = tk.Label(self.root, text="Progress:")
        self.progress_label.pack(pady=5, padx=5, anchor="w")
        style = ttk.Style()
        style.configure("Green.Horizontal.TProgressbar", thickness=20, troughcolor="lightgray", background="green")  
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=575, mode="determinate", style="Green.Horizontal.TProgressbar")
        self.progress_bar.pack(pady=10, padx=5, anchor="w")

        self.log_label = tk.Label(self.root, text="Logs:")
        self.log_label.pack(pady=1, padx=5, anchor="w")

        log_frame = tk.Frame(self.root)
        log_frame.pack(pady=0, padx=10, fill="x", expand=True)

        self.log_text = tk.Text(log_frame, height=20, width=70, wrap="word")
        self.log_text.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.log_text.config(yscrollcommand=self.scrollbar.set)

    def browse_source_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.source_dir_dropdown["values"] = [dir_path]
            self.source_dir_dropdown.set(dir_path)

    def browse_dest_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.dest_dir_dropdown["values"] = [dir_path]
            self.dest_dir_dropdown.set(dir_path)

    def start_process(self):
        source_dir = self.source_dir_dropdown.get()
        dest_dir = self.dest_dir_dropdown.get()

        if not source_dir or not dest_dir:
            self.log_message("Please select a source directory and enter a destination directory name.")
            return

        self.log_message("Starting process...")
        self.progress_bar["value"] = 0
        self.root.update()
        self.start_button.config(state="disabled", bg="gray") 

        try:
            self.progress_bar["value"] = 10
            self.log_message("Step 1: Parsing PDFs...")
            self.root.update()
            parsed_dir = os.path.join(source_dir, "parsed")
            process_books_in_directory(source_dir, parsed_dir, self.log_message, self.root)

            self.progress_bar["value"] = 50
            self.log_message("Step 2: Converting TXT to JSON...")
            self.root.update()
            parsed_json_dir = os.path.join(source_dir, "parsed_json")
            process_txt_files(parsed_dir, parsed_json_dir, self.log_message, self.root)

            self.progress_bar["value"] = 75
            self.log_message("Step 3: Splitting PDFs by chapters...")
            self.root.update()
            output_dir = os.path.join(source_dir, dest_dir)
            organize_books(source_dir, parsed_json_dir, output_dir, self.log_message, self.root)

            self.progress_bar["value"] = 95
            self.log_message("Step 4: Post-processing...")
            self.root.update()
            create_syllabus_json('Andhra', '10', 'Generic', dest_dir, parsed_json_dir, self.log_message)

            self.progress_bar["value"] = 100
            self.log_message("Process completed successfully!")
            self.root.update()
        
        except Exception as e:
            e = traceback.format_exc()
            self.log_message(f"Error: {e}")
            self.root.update()
        
        self.start_button.config(state="normal", bg="green") 

    def log_message(self, message):
        self.log_text["state"] = "normal"
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text["state"] = "disabled"
        self.log_text.see(tk.END)
        self.root.update_idletasks()  

def run_app():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

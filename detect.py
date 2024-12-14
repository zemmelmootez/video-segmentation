import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import sys


class YOLOv5ProcessorApp:
    def __init__(self, master):
        self.master = master
        master.title("YOLOv5 Segmentation Processor")
        master.geometry("600x500")

        # File selection
        self.file_frame = tk.Frame(master)
        self.file_frame.pack(padx=10, pady=10, fill='x')

        self.file_label = tk.Label(self.file_frame, text="Select Source File/Directory:")
        self.file_label.pack(side=tk.LEFT)

        self.file_path = tk.StringVar()
        self.file_entry = tk.Entry(self.file_frame, textvariable=self.file_path, width=50)
        self.file_entry.pack(side=tk.LEFT, padx=10)

        self.browse_button = tk.Button(self.file_frame, text="Browse", command=self.browse_file)
        self.browse_button.pack(side=tk.LEFT)

        # Configuration Frame
        self.config_frame = tk.LabelFrame(master, text="Processing Options")
        self.config_frame.pack(padx=10, pady=10, fill='x')

        # Confidence Threshold
        self.conf_frame = tk.Frame(self.config_frame)
        self.conf_frame.pack(fill='x', pady=5)
        tk.Label(self.conf_frame, text="Confidence Threshold:").pack(side=tk.LEFT)
        self.conf_var = tk.DoubleVar(value=0.25)
        self.conf_entry = tk.Entry(self.conf_frame, textvariable=self.conf_var, width=10)
        self.conf_entry.pack(side=tk.LEFT, padx=10)

        # Tracking Option
        self.track_var = tk.BooleanVar(value=False)
        self.track_check = tk.Checkbutton(self.config_frame, text="Enable Tracking", variable=self.track_var)
        self.track_check.pack(anchor='w')

        # View Image Option
        self.view_var = tk.BooleanVar(value=False)
        self.view_check = tk.Checkbutton(self.config_frame, text="View Images During Processing",
                                         variable=self.view_var)
        self.view_check.pack(anchor='w')

        # Progress Bar
        self.progress = ttk.Progressbar(master, orient="horizontal", length=500, mode="indeterminate")
        self.progress.pack(pady=10)

        # Process Button
        self.process_button = tk.Button(master, text="Process with YOLOv5", command=self.process_yolo)
        self.process_button.pack(pady=10)

        # Log Text Area
        self.log_text = tk.Text(master, height=10, width=70)
        self.log_text.pack(padx=10, pady=10)

    def browse_file(self):
        """Open file/directory selection dialog"""
        filename = filedialog.askopenfilename(
            title="Select Input File/Directory",
            initialdir=os.getcwd()
        ) or filedialog.askdirectory(
            title="Select Input Directory"
        )
        if filename:
            self.file_path.set(filename)

    def process_yolo(self):
        """Process the selected file/directory with YOLOv5"""
        source = self.file_path.get()
        if not source:
            messagebox.showerror("Error", "Please select a source file or directory")
            return

        # Prepare command arguments
        cmd = [
            sys.executable,  # Current Python interpreter
            'detect.py',  # YOLOv5 script
            '--source', source,
            '--conf-thres', str(self.conf_var.get())
        ]

        # Add optional arguments
        if self.track_var.get():
            cmd.append('--trk')
        if self.view_var.get():
            cmd.append('--view-img')

        # Clear previous log
        self.log_text.delete(1.0, tk.END)

        # Start progress bar
        self.progress.start()
        self.process_button.config(state=tk.DISABLED)

        try:
            # Run the process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Stream output to log
            for line in process.stdout:
                self.log_text.insert(tk.END, line)
                self.log_text.see(tk.END)
                self.master.update_idletasks()

            # Check for errors
            _, stderr = process.communicate()
            if stderr:
                self.log_text.insert(tk.END, f"Error: {stderr}")
                messagebox.showerror("Processing Error", stderr)

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log_text.insert(tk.END, f"Exception: {str(e)}")

        finally:
            # Stop progress bar
            self.progress.stop()
            self.process_button.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    app = YOLOv5ProcessorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
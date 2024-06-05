import os
import hashlib
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
import time

class FileIntegrityMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Integrity Monitor")
        self.root.geometry("600x400")

        self.directory_path = tk.StringVar()
        self.file_hashes = {}
        self.monitoring = False

        self.setup_gui()

    def setup_gui(self):
        # Background color
        self.root.configure(bg='#212121')

        # Title label
        title_label = tk.Label(self.root, text="File Integrity Monitor", bg='#212121', fg='#ffffff', font=("Helvetica", 24, "bold"))
        title_label.pack(pady=(20, 10))

        # Directory selection frame
        dir_frame = tk.Frame(self.root, bg='#212121')
        dir_frame.pack(fill=tk.X, padx=20)

        # Directory selection label
        dir_label = tk.Label(dir_frame, text="Select directory to monitor:", bg='#212121', fg='#b9f6ca', font=("Helvetica", 12))
        dir_label.pack(side=tk.LEFT)

        # Directory entry field
        self.directory_entry = tk.Entry(dir_frame, textvariable=self.directory_path, width=40, bg='#424242', fg='#ffffff', font=("Helvetica", 10))
        self.directory_entry.pack(side=tk.LEFT, padx=(10, 0), ipady=3)

        # Browse button
        browse_icon = ImageTk.PhotoImage(Image.open("folder_icon.png").resize((20, 20)))
        browse_button = tk.Button(dir_frame, image=browse_icon, command=self.browse_directory, bg='#212121', borderwidth=0, activebackground='#212121')
        browse_button.image = browse_icon
        browse_button.pack(side=tk.LEFT, padx=(10, 0))

        # Start Monitoring button
        self.start_button = tk.Button(self.root, text="Start Monitoring", command=self.start_monitoring, bg='#388e3c', fg='#ffffff', font=("Helvetica", 14, "bold"), borderwidth=0, padx=20)
        self.start_button.pack(pady=(20, 10), fill=tk.X, ipady=5)

        # Stop Monitoring button
        self.stop_button = tk.Button(self.root, text="Stop Monitoring", command=self.stop_monitoring, bg='#d32f2f', fg='#ffffff', font=("Helvetica", 14, "bold"), borderwidth=0, padx=20)
        self.stop_button.pack(pady=(0, 20), fill=tk.X, ipady=5)

        # Status label
        self.status_label = tk.Label(self.root, text="Not Monitoring", fg="#ef9a9a", bg='#212121', font=("Helvetica", 12))
        self.status_label.pack()

        # Text area for monitoring results
        self.text_area = tk.Text(self.root, bg="#303030", fg="#ffffff", font=("Helvetica", 10), wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

    def browse_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.directory_path.set(directory_path)

    def hash_file(self, file_path):
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(65536)  # Read file in chunks to conserve memory
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()

    def monitor_directory(self):
        directory_path = self.directory_path.get()
        self.status_label.config(text="Monitoring...", fg="#a5d6a7")
        while self.monitoring:
            current_files = set()
            for root, _, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    current_hash = self.hash_file(file_path)
                    current_files.add(file_path)
                    if file_path in self.file_hashes:
                        if current_hash != self.file_hashes[file_path]:
                            self.text_area.insert(tk.END, f"File changed: {file_path}\n")
                            self.text_area.see(tk.END)  # Scroll to the end
                            self.file_hashes[file_path] = current_hash
                    else:
                        self.file_hashes[file_path] = current_hash

            # Check for deleted files
            deleted_files = set(self.file_hashes.keys()) - current_files
            for deleted_file in deleted_files:
                self.text_area.insert(tk.END, f"File deleted: {deleted_file}\n")
                self.text_area.see(tk.END)  # Scroll to the end
                del self.file_hashes[deleted_file]

            time.sleep(1)
        self.status_label.config(text="Not Monitoring", fg="#ef9a9a")

    def start_monitoring(self):
        if not self.monitoring:
            self.monitoring = True
            self.start_button.config(state="disabled", bg='#5cb85c')
            self.stop_button.config(state="normal")
            threading.Thread(target=self.monitor_directory, daemon=True).start()

    def stop_monitoring(self):
        if self.monitoring:
            self.monitoring = False
            self.start_button.config(state="normal", bg='#388e3c')
            self.stop_button.config(state="disabled")

def main():
    root = tk.Tk()
    FileIntegrityMonitorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

class FoldmerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Foldmer - Batch Renamer with Audit Trail")
        self.root.geometry("600x500")

        self.folder_path = ""
        self.files = []

        # Folder selection
        tk.Button(root, text="Select Folder", command=self.select_folder).pack(pady=10)

        # Label entry
        tk.Label(root, text="Label for renamed files:").pack()
        self.label_entry = tk.Entry(root, width=40)
        self.label_entry.pack(pady=5)

        # File list frame
        self.file_frame = tk.Frame(root)
        self.file_frame.pack(fill="both", expand=True)

        # Rename button
        tk.Button(root, text="Rename Selected Files", command=self.rename_files).pack(pady=10)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if not self.folder_path:
            return

        self.files = sorted(os.listdir(self.folder_path))
        self.display_files()

    def display_files(self):
        for widget in self.file_frame.winfo_children():
            widget.destroy()

        self.check_vars = []

        for file in self.files:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.file_frame, text=file, variable=var, anchor="w")
            cb.pack(fill="x")

            # Hover highlight
            cb.bind("<Enter>", lambda e, w=cb: w.config(bg="#e0e0e0"))
            cb.bind("<Leave>", lambda e, w=cb: w.config(bg="SystemButtonFace"))

            self.check_vars.append((var, file))

    def rename_files(self):
        label = self.label_entry.get().strip()
        if not label:
            messagebox.showerror("Error", "Please enter a label.")
            return

        selected = [(var, file) for var, file in self.check_vars if var.get()]
        if not selected:
            messagebox.showerror("Error", "No files selected.")
            return

        # Audit log file
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        log_path = os.path.join(self.folder_path, f"foldmer_log_{timestamp}.txt")

        counter = 1
        with open(log_path, "w") as log:
            for var, file in selected:
                ext = os.path.splitext(file)[1]
                new_name = f"{label}_{counter:03d}{ext}"
                old_path = os.path.join(self.folder_path, file)
                new_path = os.path.join(self.folder_path, new_name)

                os.rename(old_path, new_path)
                log.write(f"{file} → {new_name}\n")

                counter += 1

        messagebox.showinfo("Success", f"Renamed {len(selected)} files.\nAudit log saved:\n{log_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FoldmerApp(root)
    root.mainloop()

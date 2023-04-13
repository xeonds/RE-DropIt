import shutil

import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("File List")
        self.master.geometry("400x400")
        self.master.resizable(False, False)
        self.file_list_label = tk.Label(self.master, text="Folders to be processed:")
        self.file_list_label.pack(side=tk.TOP, padx=5, pady=5)
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(side=tk.TOP, padx=5, pady=5)
        self.add_folder_button = tk.Button(self.button_frame, text="+", command=self.add_folder)
        self.add_folder_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.remove_folder_button = tk.Button(self.button_frame, text="-", command=self.remove_folder)
        self.remove_folder_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.file_list = tk.Listbox(self.master)
        self.file_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.process_button = tk.Button(self.master, text="Process", command=lambda: self.process_folders(mode = "process"))
        self.process_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.extract_button = tk.Button(self.master, text="Extract", command=lambda: self.process_folders(mode = "extract"))
        self.extract_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Align buttons and label horizontally
        self.file_list_label.pack(side=tk.TOP, anchor=tk.W)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.add_folder_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.remove_folder_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Add menu bar
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Add "Show folders after processed" checkbox
        self.show_folders_var = tk.BooleanVar()
        self.show_folders_var.set(False)
        options_menu = tk.Menu(menubar)
        options_menu.add_checkbutton(label="Show folders after processed", variable=self.show_folders_var)
        menubar.add_cascade(label="Options", menu=options_menu)

        # Add "About" menu item
        def show_about():
            messagebox.showinfo("About", "This is a file processing app.\n Process means sort all files by extension.\n Extract means move all files to the root dir.")
        menubar.add_command(label="About", command=show_about)

    def add_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_name = os.path.basename(folder_path)
            self.file_list.insert(tk.END, f"{folder_name} - {folder_path}")
        else:
            print("Folder not selected")

    def remove_folder(self):
        self.file_list.delete(tk.END)

    def process_folders(self, mode):
        processed_folders = []
        for directory in self.file_list.get(0, tk.END):
            directory_path = directory.split(" - ")[-1]
            process_directory(directory_path, mode)
            self.file_list.delete(self.file_list.get(0, tk.END).index(directory))
            processed_folders.append(directory_path)
            if self.show_folders_var.get():
                os.startfile(directory_path)
        messagebox.showinfo("Processing Complete", "All selected folders have been processed.")

class process_directory:
    def __init__(self, directory, mode, parent_dir=None):
        self.directory = directory
        self.mode = mode
        self.parent_dir = directory
        self.file_dict = {}
        self.run()

    def run(self):
        self.scan_dir()
        if self.mode == "process":
            for extension, filenames in self.file_dict.items():
                temp_path = os.path.join(self.directory, extension[1:])
                os.makedirs(temp_path, exist_ok=True)
                for file in filenames:
                    old_path = os.path.join(self.directory, file['path'])
                    new_path = os.path.join(temp_path, file['name'])
                    shutil.move(old_path, new_path)
        elif self.mode == "extract":
            for _, filenames in self.file_dict.items():
                for file in filenames:
                    old_path = os.path.join(self.directory, file['path'])
                    new_path = os.path.join(self.parent_dir, file['name'])
                    shutil.move(old_path, new_path)
        else:
            print("Invalid mode selected")

    def scan_dir(self):
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                extension = os.path.splitext(file)[1]
                if extension:
                    if extension not in self.file_dict:
                        self.file_dict[extension] = []
                    self.file_dict[extension].append({'name': file, 'path': os.path.join(root, file)})


root = tk.Tk()
app = App(root)
root.mainloop()

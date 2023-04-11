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

        self.process_button = tk.Button(self.master, text="Process", command=self.process_folders)
        self.process_button.pack(side=tk.BOTTOM, padx=5, pady=5)

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
        def toggle_show_folders():
            pass # TODO: Implement function to toggle show_folders_var
        options_menu = tk.Menu(menubar)
        options_menu.add_checkbutton(label="Show folders after processed", variable=self.show_folders_var, command=toggle_show_folders)
        menubar.add_cascade(label="Options", menu=options_menu)

        # Add "About" menu item
        def show_about():
            messagebox.showinfo("About", "This is a file processing app.")
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

    def process_folders(self):
        processed_folders = []
        for directory in self.file_list.get(0, tk.END):
            directory_path = directory.split(" - ")[-1]
            if process_directory(directory_path):
                self.file_list.delete(self.file_list.get(0, tk.END).index(directory))
                processed_folders.append(directory_path)
                if self.show_folders_var.get():
                    os.startfile(directory_path)
        messagebox.showinfo("Processing Complete", "All selected folders have been processed.")

    def show_folders(self, folders):
        pass

def process_directory(directory, parent_dir=None):
    if parent_dir is None:
        parent_dir = directory
    file_dict = {}
    for filename in os.listdir(directory):
        extension = os.path.splitext(filename)[1]
        if os.path.isdir(os.path.join(directory, filename)):
            process_directory(os.path.join(directory, filename), parent_dir)
        elif extension:
            if extension not in file_dict:
                file_dict[extension] = []
            file_dict[extension].append(filename)
    for extension, filenames in file_dict.items():
        temp_path = os.path.join(parent_dir, extension[1:])
        os.makedirs(temp_path, exist_ok=True)
        for filename in filenames:
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(temp_path, filename)
            shutil.move(old_path, new_path)
    return True

root = tk.Tk()
app = App(root)
root.mainloop()

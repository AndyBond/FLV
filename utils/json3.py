import os
import json
import tkinter as tk
from tkinter import messagebox

class FormApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Form with Listbox")
        self.root.geometry("450x350")
        
        # Define path for JSON file in local appdata
        local_appdata = os.getenv('LOCALAPPDATA')
        if not local_appdata:  # Fallback for non-Windows system
            local_appdata = os.path.expanduser('~/.local/share')
        
        self.app_folder = os.path.join(local_appdata, 'form_app')
        os.makedirs(self.app_folder, exist_ok=True)
        self.json_path = os.path.join(self.app_folder, 'form_data.json')
        
        # Create form elements
        self.create_widgets()
        
        # Load saved data if it exists
        self.load_data()

    def create_widgets(self):
        # Text input field
        tk.Label(self.root, text="Enter text:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.text_input = tk.Entry(self.root, width=30)
        self.text_input.grid(row=0, column=1, padx=10, pady=10)
        
        # Listbox with multiple selection enabled
        tk.Label(self.root, text="Select options:").grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        
        # Frame to contain listbox and scrollbar
        list_frame = tk.Frame(self.root)
        list_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Scrollbar for the listbox
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        
        # Create listbox with multiple selection enabled (MULTIPLE mode)
        self.listbox = tk.Listbox(list_frame, height=5, width=28, selectmode=tk.MULTIPLE, 
                                yscrollcommand=scrollbar.set)
        
        # Configure the scrollbar
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)
        
        # Add items to the listbox
        self.listbox_items = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
        for item in self.listbox_items:
            self.listbox.insert(tk.END, item)
        
        # Submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.save_data)
        self.submit_button.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Status message
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(self.root, textvariable=self.status_var, fg="green")
        self.status_label.grid(row=3, column=0, columnspan=2)

    def save_data(self):
        # Get text input
        text_data = self.text_input.get()
        
        # Get selected items from listbox
        selected_indices = self.listbox.curselection()
        selected_items = [self.listbox.get(i) for i in selected_indices]
        
        # Create data dictionary
        data = {
            "text_input": text_data,
            "selected_options": selected_items
        }
        
        # Save data to JSON file
        try:
            with open(self.json_path, 'w') as file:
                json.dump(data, file, indent=4)
            self.status_var.set("Data saved successfully!")
        except Exception as e:
            self.status_var.set(f"Error saving  {str(e)}")
            messagebox.showerror("Save Error", f"Could not save  {str(e)}")
    
    def load_data(self):
        # Load data from JSON file if it exists
        try:
            if os.path.exists(self.json_path):
                with open(self.json_path, 'r') as file:
                    data = json.load(file)
                
                # Fill text input field
                self.text_input.insert(0, data.get("text_input", ""))
                
                # Select items in listbox
                selected_options = data.get("selected_options", [])
                for i, item in enumerate(self.listbox_items):
                    if item in selected_options:
                        self.listbox.selection_set(i)
        except Exception as e:
            self.status_var.set(f"Error loading  {str(e)}")
            messagebox.showerror("Load Error", f"Could not load saved  {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FormApp(root)
    root.mainloop()
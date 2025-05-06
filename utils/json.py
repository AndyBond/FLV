import os
import json
import tkinter as tk
from tkinter import ttk
from pathlib import Path

class FormApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Form Application")
        self.root.geometry("400x250")
        
        # Define the path for the JSON file in appdata
        appdata_path = os.path.join(os.getenv('APPDATA') or 
                                   os.path.expanduser('~/.config'), 
                                   'form_app')
        os.makedirs(appdata_path, exist_ok=True)
        self.json_path = os.path.join(appdata_path, 'form_data.json')
        
        # Create form elements
        self.create_widgets()
        
        # Load saved data if it exists
        self.load_data()

    def create_widgets(self):
        # Text input field
        tk.Label(self.root, text="Enter text:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.text_input = tk.Entry(self.root, width=30)
        self.text_input.grid(row=0, column=1, padx=10, pady=10)
        
        # Multichoice select field (combobox)
        tk.Label(self.root, text="Select option:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.options = ["Option 1", "Option 2", "Option 3", "Option 4"]
        self.option_select = ttk.Combobox(self.root, values=self.options, width=27)
        self.option_select.grid(row=1, column=1, padx=10, pady=10)
        
        # Submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.save_data)
        self.submit_button.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Status message
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(self.root, textvariable=self.status_var, fg="green")
        self.status_label.grid(row=3, column=0, columnspan=2)

    def save_data(self):
        # Get data from form fields
        data = {
            "text_input": self.text_input.get(),
            "selected_option": self.option_select.get()
        }
        
        # Save data to JSON file
        try:
            with open(self.json_path, 'w') as file:
                json.dump(data, file, indent=4)
            self.status_var.set("Data saved successfully!")
        except Exception as e:
            self.status_var.set(f"Error saving  {str(e)}")
    
    def load_data(self):
        # Load data from JSON file if it exists
        try:
            if os.path.exists(self.json_path):
                with open(self.json_path, 'r') as file:
                    data = json.load(file)
                
                # Fill form fields with loaded data
                self.text_input.insert(0, data.get("text_input", ""))
                
                selected_option = data.get("selected_option", "")
                if selected_option in self.options:
                    self.option_select.set(selected_option)
        except Exception as e:
            self.status_var.set(f"Error loading data: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FormApp(root)
    root.mainloop()
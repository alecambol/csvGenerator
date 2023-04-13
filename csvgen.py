import os
import random
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv

os.chdir(os.path.dirname(os.path.abspath(__file__)))



class CSVGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CSV Generator")

        self.geometry("600x180")

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=10, pady=10, expand=True)

        self.data_categories = self.get_data_categories()

        self.column_var_list = []
        self.column_dropdown_list = []

        self.create_widgets()

    def create_widgets(self):
        self.column_label = ttk.Label(self.main_frame, text="Select the number of columns:")
        self.column_label.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        self.column_entry_var = tk.StringVar()
        self.column_entry_var.trace("w", self.update_column_dropdowns)

        num_columns_options = list(range(1, len(self.data_categories) + 1))
        self.column_entry = ttk.OptionMenu(self.main_frame, self.column_entry_var, num_columns_options[0], *num_columns_options)
        self.column_entry.grid(column=1, row=0, padx=10, pady=10)

        self.row_label = ttk.Label(self.main_frame, text="Enter the number of rows:")
        self.row_label.grid(column=0, row=1, padx=10, pady=10, sticky="w")

        self.row_entry = ttk.Entry(self.main_frame)
        self.row_entry.grid(column=1, row=1, padx=10, pady=10)

        self.generate_button = ttk.Button(self.main_frame, text="Generate CSV", command=self.generate_csv)
        self.generate_button = ttk.Button(self.main_frame, text="Generate CSV", command=self.generate_csv)

        self.generate_button.grid(column=0, row=2, padx=10, pady=10, columnspan=2, sticky="w")

        # Error message label for invalid row input
        self.error_label = ttk.Label(self.main_frame, text="Please enter a valid number for rows.", foreground="red")
        self.error_label.grid(column=2, row=2, padx=10, pady=5, sticky="w")
        self.error_label.grid_remove()  # Hide the error message initially

    def calculate_window_width(self, num_columns):
        base_width = 300
        additional_width_per_column = 150
        return base_width + (num_columns * additional_width_per_column)

    def update_column_dropdowns(self, *args):
        num_columns = self.column_entry_var.get()

        if not num_columns.isdigit():
            return

        num_columns = int(num_columns)

        for dropdown in self.column_dropdown_list:
            dropdown.grid_remove()

        self.column_var_list = []
        self.column_dropdown_list = []

        for i in range(num_columns):
            if i != 0:
                self.main_frame.columnconfigure(i, weight=0)
            column_var = tk.StringVar()
            column_dropdown = ttk.OptionMenu(self.main_frame, column_var, self.data_categories[0], *self.data_categories)
            column_dropdown.grid(column=i, row=3, padx=10, pady=10)
            self.column_var_list.append(column_var)
            self.column_dropdown_list.append(column_dropdown)

    def generate_csv(self):
        row_input = self.row_entry.get()

        if not row_input.isdigit():
            self.error_label.grid()  # Show the error message
            return
        else:
            self.error_label.grid_remove()  # Hide the error message

        rows = int(row_input)

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if not file_path:
            return

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # Write header
            header = [var.get() for var in self.column_var_list]
            writer.writerow(header)

            # Write data rows
            for _ in range(rows):
                row = self.generate_random_data_row()
                writer.writerow(row)

    def generate_random_data_row(self):
        row = []
        for var in self.column_var_list:
            category = var.get()
            value = self.get_random_data(category)
            row.append(value)

        return row

    def get_random_data(self, category):
        file_path = os.path.join("Data", f"{category}.txt")
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        return random.choice(lines).strip()

    def get_data_categories(self):
        data_folder = "Data"
        data_files = [f for f in os.listdir(data_folder) if f.endswith(".txt")]
        data_categories = [os.path.splitext(f)[0] for f in data_files]
        return data_categories


if __name__ == "__main__":
    app = CSVGeneratorApp()
    app.mainloop()

   
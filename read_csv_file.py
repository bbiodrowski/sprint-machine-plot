import pandas as pd
from tkinter import Tk, filedialog

def load_csv_file():
    # Create a Tkinter root window (it will remain hidden)
    root = Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog to select a file
    file_path = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )
    
    # If a file is selected, load and display its contents
    if file_path:
        data = pd.read_csv(file_path)
        print("CSV File Contents:")
        print(data)
    else:
        print("No file selected.")

if __name__ == '__main__':
    load_csv_file()

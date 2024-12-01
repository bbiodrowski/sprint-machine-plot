import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from tkinter import Tk, filedialog

def load_csv_file():
    # Create a Tkinter root window (it will remain hidden)
    root = Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog to select a CSV file
    file_path = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )
    
    # If a file is selected, load the data
    if file_path:
        return pd.read_csv(file_path)
    else:
        print("No file selected.")
        return None

def find_local_extrema(data, x_col, y_col):
    # Extract the x and y data from the DataFrame
    x = data[x_col].values
    y = data[y_col].values

    # Find local maxima
    peaks, _ = find_peaks(y)

    # Find local minima by inverting the signal
    minima, _ = find_peaks(-y)

    # Plot the data
    plt.plot(x, y, label='Data')
    plt.plot(x[peaks], y[peaks], "x", label='Maxima')
    plt.plot(x[minima], y[minima], "o", label='Minima')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.legend()
    plt.show()

def main():
    data = load_csv_file()
    
    if data is not None:
        # Assume 'x' and 'y' are the column names, modify if needed
        x_col = 'x'  # Replace with your x-axis column name
        y_col = 'y'  # Replace with your y-axis column name
        
        if x_col in data.columns and y_col in data.columns:
            find_local_extrema(data, x_col, y_col)
        else:
            print(f"Columns '{x_col}' or '{y_col}' not found in the CSV file.")

if __name__ == '__main__':
    main()

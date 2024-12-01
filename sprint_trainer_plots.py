import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog
from scipy.signal import find_peaks

def load_data(file_path):
    # Load data from CSV file
    data = pd.read_csv(file_path)
    # Convert time to seconds and speed to meters per second
    data['time(s)'] = data['time(ms)'] / 1000
    data['speed(m/s)'] = data['speed(mm/s)'] / 1000
    data['position(m)'] = data['position(mm)'] / 1000
    return data

def filter_data(data, speed_threshold=2, time_prior=0.5):
    # Find the first index where the speed exceeds the threshold
    exceeds_threshold_index = data[data['speed(m/s)'] > speed_threshold].index[0]
    # Find the time 0.5 seconds prior to this index
    start_time_prior = data.iloc[exceeds_threshold_index]['time(ms)'] - (time_prior * 1000)
    start_index_prior = data[data['time(ms)'] >= start_time_prior].index[0]
    # Filter the data starting from this index and zero out the time and position axis
    filtered_data = data.iloc[start_index_prior:].copy()
    filtered_data['time(s)'] -= filtered_data['time(s)'].iloc[0]
    filtered_data['position(m)'] -= filtered_data['position(m)'].iloc[0]
    return filtered_data

def calculate_power(data):
    # Convert load to Newtons and calculate power in Watts
    data['force(N)'] = data['load(g)'] * 0.00981
    data['power(W)'] = data['force(N)'] * data['speed(m/s)']
    return data

def plot_speed_time(datasets, titles):
    plt.figure(figsize=(10, 6))
    for data, title in zip(datasets, titles):
        plt.plot(data['time(s)'], data['speed(m/s)'], label=title)
    plt.xlabel('Time (s)')
    plt.ylabel('Speed (m/s)')
    plt.title('Speed over Time')
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2g}'))
    plt.show()

def plot_speed_distance(datasets, titles):
    plt.figure(figsize=(10, 6))
    for data, title in zip(datasets, titles):
        plt.plot(data['position(m)'], data['speed(m/s)'], label=title)
    plt.xlabel('Distance (m)')
    plt.ylabel('Speed (m/s)')
    plt.title('Speed over Distance')
    plt.legend()
    plt.grid(True)
    plt.show()

def calculate_metrics(data):
    max_speed = data['speed(m/s)'].max()
    max_speed_time = data['time(s)'][data['speed(m/s)'].idxmax()]
    max_power = data['power(W)'].max()
    max_power_time = data['time(s)'][data['power(W)'].idxmax()]
    load = data['load(g)'] * 0.00981
    return max_speed, max_speed_time, max_power, max_power_time, load

def calculate_acceleration(data):
    data['acceleration(m/s^2)'] = data['speed(m/s)'].diff() / data['time(s)'].diff()
    return data

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
    # Create a Tkinter root window (it will remain hidden)
    root = Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog to select multiple files
    file_paths = filedialog.askopenfilenames(
        title="Select CSV files",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )
    
    datasets = []
    titles = []
    
    # Process each selected file
    for file_path in file_paths:
        data = load_data(file_path)
        filtered_data = filter_data(data)
        filtered_data = calculate_power(filtered_data)
        filtered_data = calculate_acceleration(filtered_data)
        datasets.append(filtered_data)
        titles.append(file_path.split('/')[-1])  # Use the file name as the title

    if datasets:
        plot_speed_time(datasets, titles)
        plot_speed_distance(datasets, titles)
        
        for data, title in zip(datasets, titles):
            max_speed, max_speed_time, max_power, max_power_time, load = calculate_metrics(data)
            print(f"File: {title}")
            print(f"Max Speed: {max_speed} m/s at {max_speed_time} s")
            print(f"Max Power: {max_power} W at {load} s")  # load not working correctly
            print()
    else:
        print("No files selected.")

if __name__ == '__main__':
    main()

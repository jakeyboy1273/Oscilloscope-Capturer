import csv
from datetime import datetime
from clint.textui import prompt

def generate_filename(name, alias=None):
    """Generate a timestamped filename"""

    # Fetch and format the current date and time
    date = datetime.strftime(datetime.now(), "%Y%m%d")
    time = datetime.strftime(datetime.now(), "%H%M%S")

    # Compile and return the filename
    if alias == None:
        filename = f"{name}_{date}_{time}"
    else:
        filename = f"{name}_{alias}_{date}_{time}"
    return filename

def save_as_csv(filename, data):
    """Writes a data list to a CSV file"""
    
    print("Saving as .csv")

    # Append the file type if not already defined
    if filename[-4:] != ".csv":
        filename = f"Results/{filename}.csv"

    # Open the file and write the data
    with open(filename, "w", newline="") as csvfile:
        logfile = csv.writer(csvfile)
        length = len(data)
        for i in range(length):
            logfile.writerow(data[i])
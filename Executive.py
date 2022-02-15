import csv
from datetime import datetime

class Scope_Data:
    """Oscilloscope trace data class"""

    def __init__(self, alias, data):
        self.alias = alias
        self.data = data

    def save_as_csv(self):
        """Writes a data list to a CSV file"""
        
        print("Saving as .csv")

        # Append the file type if not already defined
        if self.filename[-4:] != ".csv":
            self.filename = f"Results/{self.filename}.csv"

        # Open the file and write the data
        with open(self.filename, "w", newline="") as csvfile:
            logfile = csv.writer(csvfile)
            length = len(self.data)
            for i in range(length):
                logfile.writerow(self.data[i])
        

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
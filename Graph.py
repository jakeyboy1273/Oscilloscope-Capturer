import pandas as pd
import matplotlib.pyplot as plt

def import_scope_trace(filename):
        """Import and generate a graph of a scope trace file"""

        # Import the file and name the columns
        df = pd.read_csv(filename)
        df.columns = ["Time (s)", "Voltage (V)"]

        # Specify the axes as variables
        t = df.iloc[:, 0]
        v = df.iloc[:, 1]

        return t, v

def save_graph(data_dict):
        pass

def save_graph_composite(data_dict):
        pass


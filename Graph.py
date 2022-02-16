import matplotlib.pyplot as plt

def save_graph(data_dict):
    """Save a graph of the scope data"""

    # Iterate through data_dict and graph all the data
    for item in data_dict:
        data = data_dict[item].data
        plt.plot(data[0], data[1])
        # TODO: Change this from show to saving the graph as .png
        plt.show()


def save_graph_composite(data_dict):
    # TODO: add this feature 
        print("save_graph_composite called!")


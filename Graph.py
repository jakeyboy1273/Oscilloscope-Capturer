import matplotlib.pyplot as plt

def format_graph(fig, title_ch):
    """Format the figure and save as a .png file"""

    # Set the figure title
    fig.suptitle(title_ch.alias, fontsize=24)
    fig.canvas.manager.set_window_title(title_ch.alias)

    # Format the plot and save as a .png
    fig.set_size_inches(32, 18)
    save_str = f"{title_ch.filename[:-4]}.png"
    plt.savefig(save_str, bbox_inches="tight")

def save_graph(scope_data):
    """Save a graph of the scope data"""
    x = []
    y = []
    for item in scope_data.data:
        x.append(item[0])
        y.append(item[1])
    fig, ax = plt.subplots()
    ax.plot(x, y)
    format_graph(fig, scope_data)

def fig_format(num_graphs):
    """Calculate optimal fig array size, based on number of series"""

    # Keep increasing row count and then column count until all graphs will fit
    box = 0
    rows = 0
    cols = 0
    while box < num_graphs:
        rows += 1
        box = rows * cols
        if box < num_graphs:
            cols += 1
            box = rows * cols
    return [rows, cols]

def place_format(narray, index):
    """Calculate where on the fig array a particular series should go"""

    # place = [row, column, index]
    place = [0, 0, 0]
    while place[2] < index:
        # increment row, and check
        place[0] += 1
        place[1] = 1
        place[2] = (place[0] - 1) * narray[1] + place[1]
        # increment column, and check
        while place[2] < index and place[1] < narray[1]:
            place[1] += 1
            place[2] = (place[0] - 1) * narray[1] + place[1]
    return place


def save_graph_composite(ch_dict):
    """Save a composite graph displaying all the channels"""

    # TODO: colour coordinate the graphs to match the channel colours on the scope
    # TODO: don't label the figure with the alias of channel 1 if it is a composite!
    # TODO: order it from top left to bottom right
    narray = fig_format(len(ch_dict))
    fig, axs = plt.subplots(narray[0], narray[1])
    for i, item in enumerate(ch_dict):
        place = place_format(narray, i)
        scope_data = ch_dict[item]
        x = []
        y = []
        for item in scope_data.data:
            x.append(item[0])
            y.append(item[1])
        if narray[1] > 1:
            axs[place[0]-1, place[1]-1].plot(x, y)
        else:
            axs[place[2]].plot(x, y)

    first_ch = next(iter(dict.values(ch_dict)))
    format_graph(fig, first_ch)


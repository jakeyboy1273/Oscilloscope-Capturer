import os
from clint.textui import prompt
from Executive import Scope_Data, generate_filename
from Instrument import load_type, select_instrument
from Graph import save_graph, save_graph_composite

"""This program allows the user to save a screenshot or a .csv file of an oscilloscope trace"""

def save_scope_trace():
    """Runs the user through saving a screenshot or .csvs"""

    print("Welcome to the Clydespace Oscilloscope Capturing Kit!")
    print("Detecting available oscilloscopes...")

    # Load a list of every connected detectable oscilloscope
    scopes = load_type("Scope")

    # Allow the user to select an oscilloscope to use
    scope = select_instrument(scopes)

    # Prompt the user to select which action they'd like to complete
    action = prompt.options(
        "What would you like to capture?",
        [
            "Save a screenshot of the current display",
            "Save a .csv of the trace",
            "Perform both of the above actions",
        ],
    )

    # Enter a project name as a prefix for all subsequently saved files
    proj_name = prompt.query(
        "Enter a name for the save files",
        default="Scope_Capture",
    )

    # If there is no "Results" director, make one
    results_folder = "Results"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)

    # If user wants a screenshot (or both)
    if action == 1 or action == 3:
        print("\n\nGenerating a screenshot...")
        filename = generate_filename(proj_name)
        scope.capture(filename)

    # If user wants the trace data (or both)
    if action == 2 or action == 3:
        print("\n\nGenerating channel captures...")

        # Ask which channels are to be saved
        ch_dict = scope.select_channels()

        # Skip if no channels are selected
        if len(ch_dict) == 0:
            print("No channels selected, skipping this step")
        else:
            # Save each selected channel as an object and as a csv
            for ch in ch_dict:
                data = scope.acquire_all(ch)
                alias = ch_dict[ch]
                ch_dict[ch] = Scope_Data(alias, data)
                ch_dict[ch].filename = generate_filename(proj_name, alias)
                ch_dict[ch].save_as_csv()

            # Ask the user if they want to save graphs
            if prompt.yn("Do you want to save a graph of the trace(s)?"):
                # If there are multiple series, ask the user to save them all as one
                if len(ch_dict) > 1 and prompt.options(
                        "How do you want the graphs to be formatted?",
                        ["All on one figure", "On individual figures"],
                        ) == 1:
                        save_graph_composite(ch_dict)
                # Otherwise, save the graph(s) individually
                else:
                    for item in ch_dict:
                        scope_data = ch_dict[item]
                        save_graph(scope_data)

    print("All finished! Have a nice day.")

if __name__ == "__main__":
    save_scope_trace()
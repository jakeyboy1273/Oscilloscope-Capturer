import os
from Executive import Scope_Data, generate_filename
from Instrument import load_type
from Graph import save_graph, save_graph_composite

"""This program allows the user to save a screenshot or a .csv file of an oscilloscope trace"""

def save_scope_trace():
    """Runs the user through saving a screenshot or .csvs"""

    print("Welcome to the Combined Oscilloscope Capturing Kit!")
    print("Detecting available oscilloscopes...")

    # Load the first scope, and configure the program to quicksave all files
    scopes = load_type("Scope")
    scope = list(scopes.values())[0]
    action = 3
    proj_name = "quick_save"

    # If there is no "Results" director, make one
    results_folder = "Results"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)

    # Ensure the oscilloscope is stopped
    scope.output("STOP")

    # If user wants a screenshot (or both)
    if action == 1 or action == 3:
        print("\n\nGenerating a screenshot...")
        filename = generate_filename(proj_name)
        scope.capture(filename)

    # If user wants the trace data (or both)
    if action == 2 or action == 3:
        print("\n\nGenerating channel captures...")

        # Ask which channels are to be saved
        ch_dict = {1: "ch1"}

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

            # If there are multiple series, ask the user to save them all as one
            if len(ch_dict) > 1:
                save_graph_composite(ch_dict)
            # Otherwise, save the graph(s) individually
            else:
                for item in ch_dict:
                    scope_data = ch_dict[item]
                    save_graph(scope_data)

    print("All finished! Have a nice day.")

if __name__ == "__main__":
    save_scope_trace()
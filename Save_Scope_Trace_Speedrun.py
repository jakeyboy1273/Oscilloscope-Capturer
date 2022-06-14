import os
from clint.textui import prompt
from Executive import Scope_Data, generate_filename
from Instrument import load_type, select_instrument
from Graph import save_graph, save_graph_composite

"""This program allows the user to save a screenshot or a .csv file of an oscilloscope trace"""

SCOPE = 0
ACTION = 3
PROJ_NAME = "quick_save"
CH_DICT = {1: "ch1"}
COMPOSITE = True

def save_scope_trace():
    """Runs the user through saving a screenshot or .csvs"""

    print("Welcome to the Combined Oscilloscope Capturing Kit!")
    print("Detecting available oscilloscopes...")

    # Load a list of every connected detectable oscilloscope
    scopes = load_type("Scope")
    scope = list(scopes.values())[SCOPE]

    # If there is no "Results" director, make one
    results_folder = "Results"
    if not os.path.isdir(results_folder):
        os.makedirs(results_folder)

    # Ensure the oscilloscope is stopped
    scope.output("STOP")

    action = ACTION
    proj_name = PROJ_NAME

    # If user wants a screenshot (or both)
    if action == 1 or action == 3:
        print("\n\nGenerating a screenshot...")
        filename = generate_filename(proj_name)
        scope.capture(filename)

    # If user wants the trace data (or both)
    if action == 2 or action == 3:
        print("\n\nGenerating channel captures...")

        ch_dict = CH_DICT

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
            if len(ch_dict) > 1 and COMPOSITE:
                filename = f"Results/{generate_filename(proj_name)}"
                save_graph_composite(ch_dict, proj_name, filename, scope.colors)

            # Otherwise, save the graph(s) individually
            else:
                for item in ch_dict:
                    scope_data = ch_dict[item]
                    save_graph(scope_data)

    print("All finished! Have a nice day.")

if __name__ == "__main__":
    save_scope_trace()
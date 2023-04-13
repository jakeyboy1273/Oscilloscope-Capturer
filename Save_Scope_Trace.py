import sys
from datetime import datetime
from clint.textui import prompt
import Oscilloscopes
from Instrument import load_type, select_instrument
from Graph import save_graph, save_graph_composite

"""This program allows the user to save a screenshot or a .csv file of an oscilloscope trace"""

def save_scope_trace():
    """Runs the user through saving a screenshot or .csv"""

    print("Welcome to the Combined Oscilloscope Capturing Kit!")
    print("Detecting available oscilloscopes...")

    # Load a list of every connected detectable oscilloscope
    scopes = load_type("Scope")

    # Allow the user to select an oscilloscope to use
    scope = select_instrument(scopes)

    restart = True
    while restart:
        # Enter a project name as a prefix for all subsequently saved files
        proj_name = prompt.query(
            "Enter a name for the save files",
            default="Scope_Capture",
        )

        # Prompt the user to select which action they'd like to complete
        action = prompt.options(
            "What would you like to capture?",
            [
                "Save a screenshot of the current display",
                "Save a .csv of the trace(s)",
                "Perform both of the above actions",
            ],
        )

        # Select which channels to save the traces on
        if action == 2 or action == 3:
            ch_dict = scope.select_channels()

            # Ask the user if they want to save graphs
            graph_save = prompt.yn("\nDo you want to save a graph of the trace(s)?")

            # Ask the user how they want the graphs to be formatted
            if graph_save and len(ch_dict) > 1:
                graph_format = prompt.options(
                    "\nHow do you want the graphs to be formatted?",
                    ["All on one figure", "On individual figures"]
                    )
            else:
                graph_format = 0

        
        # Main loop to repeat while the user wants to save more graphs
        rerun = True
        while rerun:
            # Ensure the oscilloscope is stopped
            scope.output("STOP")

            # Initialise the filename format for the captures
            timestamp = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")
            filename = f"{proj_name}_{timestamp}"

            # If user wants a screenshot (or both)
            if action == 1 or action == 3:
                print("\nGenerating a screenshot...")
                scope.capture(f"{filename}_screenshot")

            # If user wants the trace data (or both)
            if action == 2 or action == 3:
                print("\nGenerating channel captures...")

                # Skip if no channels are selected
                if len(ch_dict) == 0:
                    print("No channels selected, skipping this step")
                else:
                    # Save each selected channel as an object and as a csv
                    for ch in ch_dict:
                        data = scope.acquire_all(ch)
                        # Make a scope data object if it is a first pass
                        if type(ch_dict[ch]) == str:
                            ch_dict[ch] = Oscilloscopes.Scope_Data(ch_dict[ch], data)
                        # Just update the data of the object if it is a rerun
                        else:
                            ch_dict[ch].data = data
                        # Update the filename and save as a .csv
                        ch_dict[ch].filename = f"{filename}_{ch_dict[ch].alias}"
                        ch_dict[ch].save_as_csv()

                    # Save the graph figures if specified by the user
                    if graph_save:
                        print("Saving as .png")
                        # If there are multiple series, save the graphs in the desired format
                        if graph_format == 1:
                            save_graph_composite(ch_dict, proj_name, f"{filename}_graph", scope.colors)

                        # Otherwise, save the graph(s) individually
                        elif graph_format == 0 or graph_format == 2:
                            for item in ch_dict:
                                scope_data = ch_dict[item]
                                save_graph(scope_data)

            # Ask to run the program again with the same settings
            print("All finished!\n")
            rerun = prompt.yn("Do you want to run the program again with the same settings?")

        # Ask to restart the program with different settings
        restart = prompt.yn("Do you want to run the program again with different settings?") 

if __name__ == "__main__":

    try:
        save_scope_trace()
    except Exception as e:
        print(f"Error encountered: {e}")
    
    print("All finished! Have a nice day.")
    input("Press ENTER to exit...")
    sys.exit()
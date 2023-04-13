from clint.textui import prompt
import pyvisa, pyvisa_py

class Instrument:
    """Generic instrument abstract class"""

    def __init__(self, vendor, model, address, resource, type, delay=0):
        self.vendor = vendor
        self.model = model
        self.address = address
        self.resource = resource
        self.type = type
        self.delay = delay

def find_inheritance(klass):
    """Finds all subclasses of a class, including nested subclasses"""
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses

def count_occurrences(list, x):
    """Counts how many entries in a list have x present"""
    i = 0
    for z in list:
        if x in z:
            i = +1
    return i

def detect_instruments(rm):
    """Detect & identify all connected resources, return a list of instruments"""

    # Produce a list of USB addresses for all connected instruments
    resource_list = rm.list_resources()

    if len(resource_list) == 0:
        raise IndexError("No USB resources were detected")

    # Load and ID query each instrument address, and produce a list of names
    device_list = []
    device_detect = False
    for x in resource_list:
        try:
            resource_x = rm.open_resource(x)
            device_x = resource_x.query("*IDN?")
            device_list.append(device_x)
            device_detect = True
        except:
            device_list.append(None)
    
    # Raise an exception if none of the USB resources correspond to connected instruments
    if device_detect == False:
        raise Exception(f"No valid instruments were detected: {resource_list}")

    # Concatenate device name & address into a 2D instrument_list
    instrument_list = [[None] * 2 for _ in range(len(device_list))]
    for i, x in enumerate(device_list):
        instrument_list[i][0] = device_list[i]
        instrument_list[i][1] = resource_list[i]   
    return instrument_list
    
def load_instruments(rm):
    """Instantiate all connected instruments as objects of the appropriate instrument classes"""
    
    # Detect all the connected instruments
    instrument_list = detect_instruments(rm)
    instruments = {}

    # Import the instrument subclasses to identify against
    from Oscilloscopes import Oscilloscope

    # Match up connected instruments with supported classes
    for x in instrument_list:
        for y in find_inheritance(Instrument):
            y_OK = False
            try:
                if y.vendor in x[0] and y.model in x[0]:
                    y_OK = True
            except:
                pass
            # Create a PyVISA object and assign it as an attribute of the instrument
            if y_OK == True:
                i = count_occurrences(instruments, y.type) + 1
                address = x[1]
                instruments[str(y.type + " " + str(i))] = y(address, rm.open_resource(address))

    # Raise an exception if no connected instruments have a supporting class
    if instruments == {}:
        raise Exception(f"None of the connected instruments are supported: {instrument_list}")

    return instruments

def load_type(type, instruments = None):
    """Load all instruments of a particular type"""

    # If an instruments dict does not already exist, create one
    if instruments == None:
        instruments = load_instruments(pyvisa.ResourceManager())
    
    # Return all instruments of the expected type
    active_type = {}
    for instrument in instruments:
        inst = instruments[instrument]
        if inst.type == type:
            active_type[inst.resource] = inst

    if active_type == {}:
        raise Exception(f"No instruments of type \"{type}\" were detected")

    return active_type

def select_instrument(inst_dict):
    """Allows the user to select from the list of available instruments"""

    # Append all the available instruments to a readable list
    inst_list = []
    for inst in inst_dict:
        instrument = inst_dict[inst]
        entry = f"{instrument.vendor} {instrument.model}"
        inst_list.append([inst, entry])

    # Create a human-readable list of instruments to select from
    entry_list = []
    for entry in inst_list:
        entry_list.append(entry[1])
    
    # Prompt the user to select from the list
    if len(entry_list) > 1:
        inst_select = prompt.options(
            "Please select the instrument you wish to use",
            entry_list,
            )
    # Auto-select if there is only one available instrument
    else:
        print(f"Auto-selecting the only available instrument: {entry_list[0]}")
        inst_select = 1
    
    # Return the selected instrument as an object
    inst = inst_dict[inst_list[inst_select-1][0]]
    return inst

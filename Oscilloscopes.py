import time
from clint.textui import prompt
from Instrument import Instrument

class Oscilloscope(Instrument):
    """Generic oscilloscope abstract class"""

    type = "Scope"

    def __init__(self, vendor, model, address, resource, delay, channels, buf_size, data_size):
        super().__init__(vendor, model, address, resource, Oscilloscope.type, delay)
        self.channels = channels
        self.buf_size = buf_size
        self.data_size = data_size

    def select_channels(self):
        """User selects from the list of available channels"""

        # Make a list of available channels from the instrument
        ch_dict = {}
        ch_list = []
        for i in range (1, self.channels + 1):
            ch_list.append(f"Channel {i}")
        ch_list.append("Done")

        # Loop through the prompt to select all required channels
        repeat = True
        while repeat == True:
            channel = prompt.options("Select a channel to acquire", ch_list)
            # If "Done" is selected, quit the loop
            if channel == self.channels + 1:
                repeat = False
            # If the channel is already on the dict, raise an error message
            elif channel in ch_dict.keys():
                print("This channel has already been selected!")
            # Otherwise, add the selected channel to the dict
            else:
                ch_alias = prompt.query(
                    "\nEnter an alias for this channel",
                    default = f"Chan{channel}"
                )
                ch_dict[channel] = ch_alias

        # Return a dictionary of "channel: ch_alias" pairs
        return ch_dict

    def output(self, state_set, wait=False):
        """Run or stop the scope"""

        output_command = ":%s" % state_set
        
        if state_set == "STOP" and wait == True:
            # Calculate when there will be a full screen of data
            refresh_time = float(self.resource.query("TIM:SCAL?"))
            time.sleep(self.delay)
            # refresh_time * 6 for the screen to update - then press stop
            time.sleep(refresh_time * 6)

            self.resource.write(output_command)
            time.sleep(self.delay)
            # refresh_time * 12 to complete divisions and fill screen
            time.sleep(refresh_time * 6)
            
        # Else, just send the command
        else:
            self.resource.write(output_command)       

    def capture(self, filename):
        """Save a screenshot of the trace to the test PC"""

        # Append the directory and file type to the file name
        filename = f"Results/{filename}.png"      

        # Pull the data from the scope and save as a .png
        buf = self.resource.query_binary_values("DISP:DATA? ON,0", datatype="B")
        with open(filename, "wb") as f:
            f.write(bytearray(buf))

        # Wait for the action to complete
        time.sleep(2)

    def acquire(self, start, end, parameters):
        """Return a long list of raw datapoints for the scope trace"""

        # Define the start end end point for the data packet
        self.resource.write(f"WAV:STAR {start}")
        time.sleep(self.delay)
        self.resource.write(f"WAV:STOP {end}")
        time.sleep(self.delay)

        # Read the data packet
        raw_data = self.resource.query_binary_values(
            "WAV:DATA?", datatype="B", is_big_endian=True
        )
        time.sleep(self.delay)

        # Use the calculated parameters to translate the raw data to useful
        data = [[None] * 2 for _ in range(len(raw_data))]
        for i in range(1, len(data)):
            data[i][0] = parameters["Xor"] + (parameters["Xinc"] * (start + i))
            data[i][1] = ((raw_data[i] - parameters["Yref"]) * parameters["Yinc"]) - parameters["Yoffs"]
        
        return data

    def acquire_all(self, ch=1):
        """Get all the available raw data from the scope, packet by packet"""

        print(f"Loading scope channel {ch} data...")

        # Set the scope parameters as required
        self.resource.write("WAV:SOUR CHAN%s" % ch)
        time.sleep(self.delay)
        self.resource.write("WAV:MODE RAW")
        time.sleep(self.delay)
        self.resource.write("WAV:FORM BYTE")
        time.sleep(self.delay)
        
        # Get the required parameters from the preamble
        parameters = {}
        raw_preamble = self.resource.query("WAV:PRE?")
        time.sleep(self.delay)
        preamble = raw_preamble.split(",")
        parameters["Xinc"] = float(preamble[4])
        parameters["Xor"] = float(preamble[5])
        parameters["Yinc"] = float(preamble[7])
        parameters["Yref"] = float(preamble[9][:-1])
        parameters["Yoffs"] = float(self.resource.query("CHAN%s:OFFS?" % (ch)))
        time.sleep(self.delay)

        # Iterate through all the data, packet by packet
        data = []
        packets = self.data_size / self.buf_size
        buf_list = [i*self.buf_size + 1 for i in range(int(packets))]
        for item in buf_list:
            ll = item
            ul = item+self.buf_size-1
            data_packet = self.acquire(ll, ul, parameters)
            print(f"Loading data packet from {ll} to {ul}")
            data.extend(data_packet)
        return data

class DS1104Z(Oscilloscope):
    """Rigol Technologies DS1104Z"""

    vendor = "RIGOL TECHNOLOGIES"
    model = "DS1104Z"
    delay = 0.2

    channels = 4
    buf_size = 200000
    data_size = 1200000

    def __init__(self, address, resource):
        super().__init__(
            DS1104Z.vendor,
            DS1104Z.model,
            address,
            resource,
            DS1104Z.delay,
            DS1104Z.channels,
            DS1104Z.buf_size,
            DS1104Z.data_size,
        )
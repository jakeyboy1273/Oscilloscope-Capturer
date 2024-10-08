from time import time
import csv
import matplotlib.pyplot as plt
from RsInstrument import *


def main():
    # Load the oscilloscope
    rta = RsInstrument("TCPIP::10.212.3.176::INSTR", True, False)
    print(f"Device IDN: {rta.idn_string}")

    # Define the timebase
    time_base = rta.write_str("TIM:SCAL?")
    time_range = time_base * 10

    # Download the voltage data
    start = time()
    rta.write_str("FORMat:DATA REAL,32")
    rta.data_chunk_size = 100000  # transfer in blocks of 100k bytes (default)
    data_voltage = rta.query_bin_or_ascii_float_list("CHAN1:DATA?")
    print(f"Binary waveform transfer elapsed time: {time() - start:.3f}sec")
    
    # Define the sample rate
    sample_num = len(data_voltage)
    sample_rate = time_range / sample_num
    
    # Add the time base column
    data_time = [n * sample_rate for n in range(sample_num+1)]
    data = [[data_time[i], data_voltage[i]] for i in range(sample_num+1)]
    
    with open("new_file.csv", "w") as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=",")
        csvWriter.writerows(data)

    plt.figure(1)
    plt.plot(data)
    plt.title("Binary waveform")
    plt.show()
    
    rta.close()

if __name__ == "__main__":
    main()
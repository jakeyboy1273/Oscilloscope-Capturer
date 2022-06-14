# Oscilloscope Capturer
## Saves the data from an oscilloscope trace
This repository contains a program which can connect to an oscilloscope via USB, and save a screenshot and/or raw trace data from the scope to the test PC. The data can then also be displayed as a graph.

## Program Setup
The setup for this program is simple; create a virtual environment and use the `requirements.txt` or `Pipfile` to install all the required dependencies. Then you're good to go!

## Equipment Setup
To connect to an oscilloscope via USB, you'll need to install [NI-VISA](https://www.ni.com/en-gb/support/downloads/drivers/download/packaged.ni-visa.442805.html) upon which PyVISA depends.  
Depending on the oscilloscope, there may be additional driver downloads required:
### Rigol DS1104Z
[ICP / IVI Compliance](https://www.ni.com/en-gb/support/downloads/drivers/download/packaged.ivi-compliance-package.409836.html)  
[DS1000Z IVI Driver](https://www.rigolna.com/download/)

## Usage
Firstly, use your oscilloscope to capture your required trace. It will probably help to stop the scope but if you don't then the program will do it anyway at the time of capture, so no worries. Also, ensure it is connected to your PC via USB cable.  
To use the full program, run `Save_Scope_Trace.py`. This program has a text UI which guides you through the options on the program. You can:
- save a .png screenshot of the oscilloscope screen
- save a .csv file of every datapoint (time, voltage) on the screen, for any of the enabled channels
- save a .png matplotlib graph for any or all of the enabled channels

If you want to run the program quicker, or multiple times with the same settings, give `Save_Scope_Trace_Speedrun.py` a go. You can modify any of the constants to make the program run through quickly and with minimal human intervention. Then you can get REALLY capture-happy!

## Notes
- If you save a .csv and then try to open it with excel, it will probably be too big and get clipped. Best to do any further analyses with, you guessed it, even more Python!


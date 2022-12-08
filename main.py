import sys
import os
import glob
import re
import tkinter as tk
from tkinter import filedialog

#object to represent a raw file
class dataFile:
    def __init__(self, name, data):
        self.name = name
        self.data = data

#parse the data from a file and return a dataFile obj
def parseFile(filename):
    file = dataFile("", {})
    sample_name = os.path.basename(filename)
    match = re.search('^(.*)\.ISD', sample_name)
    if match:
        file.name = match[1]
        data = {}
        with open(filename, 'r') as f:
            contents = f.readlines()
            for line in contents:
                match = re.search('^(\d*)\t(-?\d*.\d*)(E?-?\d*)\n',line)
                if match:
                    wav = match[1]
                    value = match[2]+match[3]
                    data[wav] = value
        file.data = data
    return file

#create a string in csv format for dataFiles
def join_data(entry):
    return ('\n').join(entry.name + ", " + ', '.join((key,val)) for (key,val) in entry.data.items())

#prompt for file dir
root = tk.Tk()
root.withdraw()
dir = filedialog.askdirectory()
if not dir:
    sys.exit(0)

#list of all Sample files
files = glob.glob(os.path.join(dir, '*.ISD'))


#parse all files
allFiles = []
for filename in files:
    tempFile = parseFile(filename)
    allFiles.append(tempFile)

#create CSV output
output = "sample, wav (nm), data\n"
for entry in allFiles:
    file_str = join_data(entry)
    output += (file_str + '\n')

#prompt output save location
f = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
if not f:
    sys.exit(0)
f.write(output)
f.close()
import os
import argparse
import numpy as np

# Parse user args
parser = argparse.ArgumentParser()
parser.add_argument('fileIn')
parser.add_argument('fileOut')
args = parser.parse_args()

# Remove special chars that may confuse Numpy
#   and save to a temp file so that the original doesn't have to be modified
with open(args.fileIn, 'r') as file :
  filedata = file.read()

special_char = '"@_!#$%^&*()<>?/\|}{~:;[]'
for i in special_char:
    filedata = filedata.replace(i, '')

with open('temp.csv', 'w') as file:
  file.write(filedata)

# Numpy read in csv
dataIn = np.genfromtxt('temp.csv', delimiter=',', dtype='U70', skip_header=True)

# Delete temp file
if os.path.exists("temp.csv"):
  os.remove("temp.csv")
else:
  print("Temp file does not exist.")

    
partNames = dataIn[:,0]
xDist = dataIn[:,3]
yDist = dataIn[:,4]
rot = dataIn[:,5]
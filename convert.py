import argparse
import numpy as np
import re

# Parse user args
parser = argparse.ArgumentParser()
parser.add_argument('fileIn')
parser.add_argument('fileOut')
args = parser.parse_args()

# Remove special chars that may confuse Numpy
with open(args.fileIn, 'r') as file :
  filedata = file.read()

special_char = '"@_!#$%^&*()<>?/\|}{~:;[]'
for i in special_char:
    filedata = filedata.replace(i, '')

with open(args.fileIn, 'w') as file:
  file.write(filedata)

# Numpy read in csv
dataIn = np.genfromtxt(args.fileIn, delimiter=',', dtype='U70', skip_header=True)
    
partNames = dataIn[:,0]
xDist = dataIn[:,3]
yDist = dataIn[:,4]
rot = dataIn[:,5]
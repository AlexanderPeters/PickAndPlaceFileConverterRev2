#TODO:
# Fix parameter intake with help and other info
# x and y -> (5 digits) mm/100

import os
import argparse
import numpy as np

# Parse user args
parser = argparse.ArgumentParser()
parser.add_argument('fileIn')
parser.add_argument('fileOut')
parser.add_argument('boardSize_X')
parser.add_argument('boardSize_Y')
args = parser.parse_args()

fileIn = args.fileIn
fileOut = args.fileOut
boardSize_X = float(args.boardSize_X)
boardSize_Y = float(args.boardSize_Y)

# Remove special chars that may confuse Numpy
#   and save to a temp file so that the original doesn't have to be modified
with open(fileIn, 'r') as file :
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

# Extract useful values
partNames = [str(i) for i in dataIn[:,0]]
xDist = [float(i) for i in dataIn[:,3]]
yDist = [float(i) for i in dataIn[:,4]]
rot = [int(float(i)) for i in dataIn[:,5]]

# Convert positioning for board size

# This math translates the origin point from
#   the upper left (KiCad Refference) to 
#   the lower right (Pick and Place Machine Static Refference)

# * 100 so that units are mm/100 instead of mm
for x in range(len(xDist)):
  xDist[x] = int((-(boardSize_X - xDist[x])) * 100) 
for y in range(len(yDist)):
  yDist[y] = int((boardSize_Y + yDist[y]) * 100)

# Dummy Parameters to assemble
skip = '0'
mCode = '000'
headNum = '1'
feederNum = '017'
unused = '00'
mountHeightPlusMinus = '+'
mountHeight = '000'

# Assemble with .NC format
newLines = []
for i in range(len(partNames)):
  # Assembly logic
  xPlusMinus = '+' if xDist[i] >= 0 else '-'
  yPlusMinus = '+' if yDist[i] >= 0 else '-'

  # Build lines using .NC format
  line = 'N' + str(i + 1).zfill(4) + '/' + skip + 'M' + mCode + \
    'X' + xPlusMinus + str(xDist[i]).replace('+', '').replace('-', '').zfill(5) + \
    'Y' + yPlusMinus + str(yDist[i]).replace('+', '').replace('-', '').zfill(5) + \
    'Z0' + feederNum + 'W' + str(rot[i]).zfill(3) + 'U' + unused + 'MH' + \
    mountHeightPlusMinus + mountHeight + ';' + partNames[i]

  # Add to list
  newLines.append(line)

# Write .NC file
with open(fileOut, 'w') as file:
  file.write('\r\n'.join(newLines))
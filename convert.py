#TODO:
# Fix parameter intake with help and other info
# Fix broken origin conversion, logic different
#    depending upon in which quadrant the new origin is in

import os
import argparse
import numpy as np

# Parse user args
parser = argparse.ArgumentParser()
parser.add_argument('fileIn')
parser.add_argument('configFile')
parser.add_argument('fileOut')
args = parser.parse_args()

fileIn = args.fileIn
configFile = args.configFile
fileOut = args.fileOut

# Remove special chars that may confuse Numpy
#   and save to a temp file so that the original doesn't have to be modified
with open(fileIn, 'r') as file :
  filedata = file.read()

special_char = '"@_!#$%^&*()<>?/\|}{~:;[]'
for i in special_char:
    filedata = filedata.replace(i, '')

with open('temp.csv', 'w') as file:
  file.write(filedata)

# Numpy read in KiCad Position .csv
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

# Numpy read in Board Configuration .csv
configData = np.genfromtxt(configFile, delimiter=',', dtype='int_', skip_header=True)

# Extract useful values
stepNumber = configData[:,0]
skip = configData[:,1]
mCode = configData[:,2]
feederNum = configData[:,3]
unused = '00'
headNum = configData[:,4]
mountHeight = configData[:,5]

originOffsetX = float(configData[0,7])
originOffsetY = float(configData[0,8])

# Convert positioning for board size

# This math translates the origin point from
#   the KiCad Origin to 
#   Pick and Place Machine Static Refference
# * 100 so that units are mm/100 instead of mm

for x in range(len(xDist)):
  xDist[x] = int((xDist[x] - originOffsetX) * 100) 
for y in range(len(yDist)):
  yDist[y] = int((yDist[y] - originOffsetY) * 100)

# Check to make sure the KiCad Pos file and the 
#   Config file have the same number of steps
if len(partNames) != len(stepNumber):
  print('Given parameter files do not have the same number of steps.')
  quit(0)

# Assemble with .NC format
newLines = []
for i in range(len(partNames)):
  # Assembly logic
  xPlusMinus = '+' if xDist[i] >= 0 else '-'
  yPlusMinus = '+' if yDist[i] >= 0 else '-'
  mountHeightPlusMinus = '+' if mountHeight[i] >= 0 else '-'
  
  if headNum[i] == 1:
    feeder = feederNum[i]
  elif headNum[i] == 2:
    feeder = feederNum[i] + 200
  elif headNum[i] == 3:
    feeder = feederNum + 400
  else:
    print('Error: Head Specified not 1,2, or 3')
    quit(0)

  # Build lines using .NC format
  line = 'N' + str(i + 1).zfill(4) + '/' + str(skip[i]) + 'M' + str(mCode[i]).zfill(3) + \
    'X' + xPlusMinus + str(xDist[i]).replace('+', '').replace('-', '').zfill(5) + \
    'Y' + yPlusMinus + str(yDist[i]).replace('+', '').replace('-', '').zfill(5) + \
    'Z0' + str(feeder).zfill(3) + 'W' + str(rot[i]).zfill(3) + 'U' + unused + 'MH' + \
    mountHeightPlusMinus + str(mountHeight[i]).zfill(3) + ';' + partNames[i]

  # Add to list
  newLines.append(line)

# Write .NC file
with open(fileOut, 'w') as file:
  file.write('\r\n'.join(newLines))
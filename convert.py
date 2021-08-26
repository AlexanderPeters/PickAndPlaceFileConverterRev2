import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

with open(args.filename, neline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
        
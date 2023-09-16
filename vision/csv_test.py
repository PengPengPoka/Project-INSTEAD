import csv
import os

home = os.path.expanduser("~")
path = home + "\\Repositories\\Project-INSTEAD\\vision\\default_param.txt"
data_list = []

# Open the CSV file for reading
with open(path, newline='') as csvfile:
    # Create a CSV reader
    csvreader = csv.DictReader(csvfile)
    
    # Loop through each row in the CSV file
    for row in csvreader:
        # Append each row as a dictionary to the list
        data_list.append(row)

# Print the list of dictionaries
for item in data_list:
    print(item)
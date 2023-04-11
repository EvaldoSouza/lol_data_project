import os
import csv
import json

def make_folder_if_inexistent(folder_path):
    # checking if the directory demo_folder
    # exist or not.
    if not os.path.exists(folder_path):
        
        # if the demo_folder directory is not present
        # then create it.
        os.makedirs(folder_path)


def read_csv(filename):
    """
    Reads the contents of a CSV file and returns a list of dictionaries, where
    each dictionary represents a row in the CSV file.
    """
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    return rows

def read_json(filename):
    with open(filename) as file:
        dados = json.load(file)

    return dados
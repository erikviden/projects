import csv
import json
import os
import sys

class Reader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    def read_data(self):
        extension = os.path.splitext(self.filepath)[1].lower()
        if extension == '.csv':
            try:
                with open(self.filepath, newline='') as file_stream:
                    self.data = list(csv.reader(file_stream))
            except FileNotFoundError:
                print(f"File {self.filepath} does not exist.")
                self.data = None
            return

        elif extension == '.json':
            try:
                with open(self.filepath, 'r') as file_stream:
                    self.data = json.load(file_stream)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error reading JSON file: {e}")
                self.data = None
            return

        else:
            raise ValueError(f"Unsupported file: {extension}")

    def write_data(self):
        extension = os.path.splitext(self.filepath)[1].lower()
        if extension == '.csv':
            try:
                with open(self.filepath, mode="w", newline="") as file_stream:
                    csv_writer = csv.writer(file_stream)
                    csv_writer.writerows(self.data)
            except Exception as e:
                print(f"Error writing CSV file: {e}")
        elif extension == '.json':
            try:
                with open(self.filepath, 'w') as file_stream:
                    json.dump(self.data, file_stream, indent=4)
            except Exception as e:
                print(f"Error writing JSON file: {e}")
        else:
            raise ValueError(f"Unsupported file: {extension}")

def modify_data(data, changes):
    for change in changes:
        try:
            c, r, value = change.split(',')
            c = int(c)
            r = int(r)
            if 0 <= r < len(data) and 0 <= c < len(data[r]):
                data[r][c] = value
            else:
                print(f"Error.")
        except ValueError:
            print(f"Wrong format, try again.")


if len(sys.argv) < 4:
    print("Command needs to be in this format: 'reader.py <src> <dst> <change1> <change2> ...'")
    sys.exit(1)

src_file = Reader(sys.argv[1])
dst_file = Reader(sys.argv[2])
changes = sys.argv[3:]
src_file.read_data()
if src_file.data is None:
    sys.exit(1)
print("Old file:")
print(src_file.data)
modify_data(src_file.data, changes)
dst_file.data = src_file.data
dst_file.write_data()
print("Modified file:")
print(dst_file.data)

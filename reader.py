import csv
import sys

if len(sys.argv) < 4:
    print("Command needs to be in this format: 'reader.py <src> <dst> <change1> <change2> ...'")
    sys.exit(1)

src = sys.argv[1]
dst = sys.argv[2]
change = sys.argv[3:]

try:
    with open(src, newline='') as file_stream:
        csv_reader = csv.reader(file_stream)
        values_from_csv_file = list(csv_reader)
        print("Old CSV file:")
        for r in values_from_csv_file:
            print(r)
except:
    print(f"File {src} does not exist.")

for change in change:
    try:
        c, r, value = change.split(',')
        c = int(c)
        r = int(r)
        if r < len(values_from_csv_file) and c < len(values_from_csv_file[r]):
            values_from_csv_file[r][c] = value
        else:
            print(f"Error.")
    except ValueError:
        print(f"Wrong format, try again.")

try:
    with open(dst, mode="w", newline="") as file_stream:
        csv_writer = csv.writer(file_stream)
        csv_writer.writerows(values_from_csv_file)
        print("New CSV file:")
        for row in values_from_csv_file:
            print(row)
except:
    print(f"Error writing the file.")

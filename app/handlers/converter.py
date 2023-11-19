import csv
from ..config.conf import DB_CSV_NAME, DB_CSV_NAME_OUT


def make_conv():
    with open(DB_CSV_NAME, "r") as file:
        reader = csv.reader(file)

        with open(DB_CSV_NAME_OUT, "w", newline="") as output_file:
            writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)

            count = 0
            for row in reader:
                if count == 0:
                    columns = row
                print(count, end="\t")
                writer.writerow(row)
                count += 1
    return columns

import csv
import json


def make_conv(csv_file: str, csv_file_out: str) -> tuple[list, int]:
    """Функция конвертирует исходный CSV в CSV "str"

    Args:
        csv_file (str): имя исходного csv файла
        csv_file_out (str): имя выходного csv файла

    Returns:
        tuple[list, int]: возвращает кортеж со списком полей и количеством записей
    """
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        with open(csv_file_out, "w", newline="") as output_file:
            writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)

            count = 0
            for row in reader:
                if count == 0:
                    columns = row
                print(count, end="\t")
                writer.writerow(row)
                count += 1
    return columns, count


def csv_to_json(csv_file: str, json_file: str) -> tuple[list, int]:
    """Функция конвертирует csv в json

    Args:
        csv_file (str): имя csv файла
        json_file (str): имя json файла

    Returns:
        tuple[list, int]: возвращает кортеж со списком полей и количеством записей
    """
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, quotechar='"')

        with open(json_file, "w", encoding="utf-8") as jf:
            count = 0
            for row in reader:
                json.dump(row, jf, ensure_ascii=False)
                jf.write("\n")

                count += 1
                print(count, end="\t")

    return list(row.keys()), count


if __name__ == "__main__":
    from app.config.conf import DB_CSV_NAME, DB_CSV_NAME_OUT, DB_JSON_NAME_OUT

    csv_to_json(DB_CSV_NAME, DB_JSON_NAME_OUT)

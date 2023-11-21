DB_NAME = "default"
TABLE_NAME = "lenta_ru"
URL_DB_DOWNLOAD = "https://github.com/yutkin/Lenta.Ru-News-Dataset/releases/download/v1.1/lenta-ru-news.csv.bz2"

DB_ZIP_NAME = URL_DB_DOWNLOAD.split("/")[-1]
DB_CSV_NAME = DB_ZIP_NAME.split(".bz2")[0]
DB_CSV_NAME_OUT = DB_CSV_NAME.split(".")[0] + "-out." + DB_CSV_NAME.split(".")[-1]
DB_JSON_NAME_OUT = DB_CSV_NAME.split(".")[0] + "-out.json"

CH_CLI_USER_FILES_PATH = "/var/lib/clickhouse/user_files/"

if __name__ == "__main__":
    print(f"{DB_NAME = }")
    print(f"{TABLE_NAME = }")
    print(f"{URL_DB_DOWNLOAD = }")
    print(f"{DB_ZIP_NAME = }")
    print(f"{DB_CSV_NAME = }")
    print(f"{DB_CSV_NAME_OUT = }")
    print(f"{DB_JSON_NAME_OUT = }")
    print(f"{CH_CLI_USER_FILES_PATH = }")

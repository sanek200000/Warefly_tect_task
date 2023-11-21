import sys
import subprocess
from app.config.conf import (
    DB_NAME,
    TABLE_NAME,
    URL_DB_DOWNLOAD,
    DB_ZIP_NAME,
    DB_CSV_NAME,
    DB_JSON_NAME_OUT,
    CH_CLI_USER_FILES_PATH,
)
from app.handlers.conv import csv_to_json


if __name__ == "__main__":
    # Чистим окно терминала
    subprocess.run(["clear"])

    # Проверяем, установлен ли Docker и Docker-compose
    try:
        subprocess.check_output(["docker", "--version"])
        doc_ver = subprocess.run(["docker", "--version"], stdout=subprocess.PIPE)
        print(doc_ver.stdout)

        subprocess.check_output(["docker-compose", "--version"])
        dc_ver = subprocess.run(["docker-compose", "--version"], stdout=subprocess.PIPE)
        print(dc_ver.stdout)
    except:
        print("Docker или docker-compose не установлен в системе.")
        sys.exit(1)

    # Если установлены, запускаем контейнер
    subprocess.run(["docker-compose", "up", "-d"])

    # Проверяем, есть ли в Clickhouse наша БД
    table_name = subprocess.run(
        [
            "docker",
            "exec",
            "some-clickhouse-server",
            "clickhouse-client",
            '--query="SHOW TABLES;"',
        ],
        stdout=subprocess.PIPE,
        text=True,
    )

    # Если есть, то завершаем выполнение скрипта
    if table_name == TABLE_NAME:
        print(
            f"БД {TABLE_NAME} уже существует, можете пройти по ссылке: http://localhost:9090/"
        )
        sys.exit(0)

    # Иначе, качаем БД в формате CSV
    subprocess.run(["wget", URL_DB_DOWNLOAD])

    # Распаковываем архив
    try:
        subprocess.check_output(["which", "bzip2"])
    except:
        print("Не установлен архиватор bzip2")
        sys.exit(1)
    subprocess.run(["bzip2", "-d", DB_ZIP_NAME])

    # Конверитуем CSV в JSON
    # columns = ["url", "title", "text", "topic", "tags", "date"]
    columns, rec_count = csv_to_json(DB_CSV_NAME, DB_JSON_NAME_OUT)

    # Копируем файл JSON в контейнер Clickhouse
    copy_file = subprocess.run(
        [
            "docker",
            "cp",
            DB_JSON_NAME_OUT,
            f"some-clickhouse-server:{CH_CLI_USER_FILES_PATH}{DB_JSON_NAME_OUT}",
        ],
        stdout=subprocess.PIPE,
        text=True,
    )
    print(f"{copy_file.stdout = }")

    # Создаем БД
    table_columns = ", ".join(col + " Nullable(String)" for col in columns)
    query_string = f"--query=CREATE TABLE {DB_NAME}.{TABLE_NAME} ( {table_columns} ) ENGINE = MergeTree() ORDER BY tuple();"

    make_db = subprocess.run(
        [
            "docker",
            "exec",
            "some-clickhouse-server",
            "clickhouse-client",
            query_string,
        ],
        stdout=subprocess.PIPE,
        text=True,
    )
    print(f"{make_db.stdout = }")

    # Заливаем данные из JSON в БД Clickhouse
    with subprocess.Popen(
        [
            "docker",
            "exec",
            "-i",
            "-w",
            f"{CH_CLI_USER_FILES_PATH}",
            "some-clickhouse-server",
            "/bin/bash",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
    ) as process:
        output, error = process.communicate(
            input=f'cat {DB_JSON_NAME_OUT} | clickhouse-client --query="INSERT INTO {TABLE_NAME} FORMAT JSONEachRow"\n'.encode()
        )

    # Проверяем, все ли данные попали в таблицу
    ch_rec_count = subprocess.run(
        [
            "docker",
            "exec",
            "some-clickhouse-server",
            "clickhouse-client",
            f"--query=SELECT COUNT(*) FROM {DB_NAME}.{TABLE_NAME};",
        ],
        stdout=subprocess.PIPE,
        text=True,
    )

    if int(ch_rec_count.stdout) == rec_count:
        print("Теперь можно зайти на http://localhost:9090/ и узнать заветные 100 слов")
        subprocess.run(["rm", DB_CSV_NAME])
        subprocess.run(["rm", DB_JSON_NAME_OUT])
        subprocess.run(
            [
                "docker",
                "exec",
                "-w",
                CH_CLI_USER_FILES_PATH,
                "some-clickhouse-server",
                "rm",
                DB_JSON_NAME_OUT,
            ]
        )
        subprocess.run(["rm", DB_ZIP_NAME])
    else:
        print(
            f"Что-то пошло не так. Количество строкв файле {DB_JSON_NAME_OUT} = {rec_count}"
        )
        print(f"Количество строк в таблице {TABLE_NAME} = {int(ch_rec_count.stdout)}")

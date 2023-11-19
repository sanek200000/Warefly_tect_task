import sys
import subprocess
from app.config.conf import (
    DB_NAME,
    TABLE_NAME,
    URL_DB_DOWNLOAD,
    DB_ZIP_NAME,
    DB_CSV_NAME_OUT,
)
from app.handlers.converter import make_conv


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

    # Конверитуем CSV с помощью скрипта
    columns = make_conv()

    # Копируем файл CSV в контейнер Clickhouse
    subprocess.run(
        ["docker", "cp", DB_CSV_NAME_OUT, f"some-clickhouse-server:/{DB_CSV_NAME_OUT}"]
    )

    # Создаем БД
    make_query = ", ".join(col + " Nullable(String)" for col in columns)
    subprocess.run(
        [
            "docker",
            "exec",
            "some-clickhouse-server",
            "clickhouse-client",
            f'--query="CREATE TABLE {DB_NAME}.{TABLE_NAME} ( {make_query} ) ENGINE = MergeTree() ORDER BY tuple();"',
        ]
    )

    # Заливаем данные из CSV в БД
    subprocess.run(
        [
            "docker",
            "exec",
            "some-clickhouse-server",
            "clickhouse-client",
            f'--query="INSERT INTO {DB_NAME}.{TABLE_NAME} FORMAT CSV < /{DB_CSV_NAME_OUT};"',
        ]
    )

    print("Теперь можно зайти на http://localhost:9090/ и узнать заветные 100 слов")

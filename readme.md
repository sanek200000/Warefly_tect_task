# Task
Развернуть Clickhouse в него загрузить датасет https://www.kaggle.com/datasets/yutkin/corpus-of-russian-news-articles-from-lenta

Написать сервис который  выводит топ100 самых часто встречаемых слов. Как должен работать сервис: localhost:9090/getWords в ответ json с словами и кол-вом вхождений. Сюда прислать ссылку на исходники и пример вывода. 

# Plan
1. Установить и настройть ClickHouse.
2. Загрузить датасет в ClickHouse.
3. Создать сервис, который будет выводить топ100 слов.

### Шаг 1: Установить и настройть ClickHouse

Вы можете установить ClickHouse с помощью Docker. Выполните следующие команды:

```bash
docker pull yandex/clickhouse-server
docker run -d --name some-clickhouse-server --ulimit nofile=262144:262144 yandex/clickhouse-server
```
### Шаг 2: Загрузите датасет в ClickHouse

Прежде чем загрузить датасет, вам нужно его преобразовать в формат CSV. После этого, вы можете загрузить его в ClickHouse с помощью команды clickhouse-client.

```bash
cat your_file.csv | clickhouse-client --query="INSERT INTO table_name FORMAT CSV"
```
### Шаг 3: Создайте сервис, который будет выводить топ100 слов

Вы можете использовать любой язык программирования для создания сервиса. В этом примере я буду использовать Python с Flask.

```python
from flask import Flask, jsonify
from clickhouse_driver import Client

app = Flask(__name__)

@app.route('/getWords', methods=['GET'])
def get_words():
    client = Client('localhost')

    query = 'SELECT word, count FROM table_name ORDER BY count DESC LIMIT 100'
    result = client.execute(query)

    return jsonify(result)

if __name__ == '__main__':
    app.run(port=9090)
```

Этот сервис будет подключаться к ClickHouse, выполнять запрос к базе данных для получения топ100 слов, а затем возвращать эти слова в формате JSON.

Пожалуйста, замените table_name на название вашей таблицы в ClickHouse.

Примечание: Прежде чем запускать этот сервис, убедитесь, что ClickHouse запущен и выполнен запрос для создания таблицы и загрузки данных.



# Temp
- docker exec -it some-clickhouse-server clickhouse-client

- docker cp lenta-ru-news_ver01.csv some-clickhouse-server:/lenta-ru-news.csv

- docker cp lenta-ru-news.csv 54ad12bfff98bf50f744544fe9d33d67b1add28f4901d24485dcd6667780d427:/lenta-ru-news.csv

CREATE TABLE default.lenta_ru
(
    `url` Nullable(String),
    `title` Nullable(String),
    `text` Nullable(String),
    `topic` Nullable(String),
    `tags` Nullable(String),
    `date` Nullable(String)
)
ENGINE = MergeTree()
ORDER BY tuple();

- clickhouse-client --query="INSERT INTO default.lenta_ru FORMAT CSV" < lenta-ru-news.csv

- INSERT INTO default.lenta_ru FORMAT CSV < /lenta-ru-news.csv

- url,title,text,topic,tags,date

    INSERT INTO default.lenta_ru (text) SELECT text FROM file('lenta-ru-news.csv', 'CSV', 'url VARCHAR, title VARCHAR, text VARCHAR, topic VARCHAR, tags VARCHAR, date VARCHAR');
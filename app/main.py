from flask import Flask, Response, render_template
from clickhouse_driver import Client
import json


app = Flask(__name__)
clickhouse_client = Client(host="clickhouse", port=9000)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/getWords", methods=["POST"])
def get_top_words() -> Response:
    """Функция делает запрос к БД, ищет 100 самых используемых слов

    Returns:
        Response: возвращает ответ с данными в формате json
    """

    query = """SELECT word, count() as word_count
    FROM (
        SELECT arrayJoin(splitByChar(' ', coalesce(text, ''))) as word
        FROM default.lenta_ru
        WHERE text IS NOT NULL
    )
    GROUP BY word ORDER BY word_count DESC LIMIT 100;
    """

    result = clickhouse_client.execute(query)

    top_words = [{"word": row[0], "count": row[1]} for row in result]

    json_data = json.dumps(top_words, ensure_ascii=False)
    response = Response(json_data, content_type="application/json; charset=utf-8")
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)

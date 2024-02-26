from flask import Flask, jsonify, request
import json

app = Flask(__name__)


def get_collection_data_mock(collection_slug):
    with open('stats.json', 'r') as file:
        data = json.load(file)
    return data


@app.route('/openapi/v1/collection/stats', methods=['GET'])
def get_stats():
    data = request.args
    collection_slug = data.get("collection_slug")
    stats_data = get_collection_data_mock(collection_slug)
    response = jsonify(stats_data)
    response.status_code = 200
    return response


if __name__ == '__main__':
    app.run(debug=False)

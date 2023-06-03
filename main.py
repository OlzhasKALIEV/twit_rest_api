import json

from flask import Flask, jsonify, request
from flask.json import JSONEncoder
from model.twit import Twit

app = Flask(__name__)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Twit):
            return {'body': obj.body, 'author': obj.author}
        else:
            return super().default(obj)


app.json_encoder = CustomJSONEncoder
twits =[]


@app.route("/")
def ping():
    return jsonify({"response": "pong"})


@app.route('/twit', methods=["POST"])
def creat_twit():
    twit_json = request.get_json()
    twit = Twit(twit_json['body'], twit_json['author'])
    twits.append(twit)
    return jsonify({"soper": "super"})


@app.route('/twit', methods=["GET"])
def read_twits():
    return jsonify({'twits': twits})


if __name__ == "__main__":
    app.run(debug=True)

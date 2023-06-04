import json

from flask import Flask, jsonify, request, make_response
from model.twit import Twit

app = Flask(__name__)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Twit):
            return {"body": o.body, "author": o.author}
        return super()


app.json_encoder(CustomJSONEncoder)

twits = list()


@app.route("/")
def ping():
    return jsonify({"response": "pong"})


@app.route('/twit', methods=["POST"])
def creat_twit():
    ''' {"body": "Hello World", "author": "@Olzhas"}
    '''
    twit_json = request.get_json()
    twit = Twit(twit_json["body"], twit_json["author"])
    jsonized = json.dumps(twit, cls=CustomJSONEncoder)
    twits.append(json.loads(jsonized))
    return make_response("Успех", 200)


@app.route('/twit', methods=["GET"])
def read_twits():
    return jsonify({"twits": twits})


if __name__ == "__main__":
    app.run(debug=True)

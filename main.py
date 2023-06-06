import json

from flask import Flask, jsonify, request, make_response
from model.twit import Twit
from model.user import User, get_users_comment

app = Flask(__name__)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Twit):
            return {"body": o.body, "author": o.author}
        if isinstance(o, User):
            return {"user_name": o.user_name, "user_comment": o.user_comment(request.get_json()["user_comment"])}


app.json_encoder(CustomJSONEncoder)

twits = list()  # []
comment_user = list()


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


@app.route('/twit/comment', methods=["GET", "POST"])
def get_post_users():
    if request.method == "GET":
        ''' {"author": "@Olzhas"}
        '''
        post_user = request.get_json()
        get_post_user = get_users_comment(post_user, twits)
        comment_user.append(get_post_user["body"])
        return get_post_user

    if request.method == "POST":
        ''' {"user_name": "@Olzhas", "user_comment"}
        '''
        comment_post_user = request.get_json()
        user_post = User(comment_post_user["user_name"])
        user_post_comment = json.dumps(user_post, cls=CustomJSONEncoder)
        comment_user.append(json.loads(user_post_comment))
        return jsonify({"user_comment": comment_user})


if __name__ == "__main__":
    app.run(debug=True)

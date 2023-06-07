import json

from flask import Flask, jsonify, request, make_response
from model.twit import Twit
from model.user import User, get_users_comment, delete, update_post

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
    ''' {"body": "Hello World", "author": "@Ray"}
    '''
    twit_json = request.get_json()
    twit = Twit(twit_json["body"], twit_json["author"])
    jsonized = json.dumps(twit, cls=CustomJSONEncoder)
    twits.append(json.loads(jsonized))
    return make_response("Пост добавлен", 200)


@app.route('/twit', methods=["GET"])
def read_twits():
    return jsonify({"twits": twits})


@app.route('/twit/comment', methods=["GET", "POST"])
def get_post_users():
    if request.method == "GET":
        ''' {"author": "@Ray"}
        '''
        post_user = request.get_json()
        get_post_user = get_users_comment(post_user, twits)
        comment_user.append(get_post_user["body"])
        return get_post_user

    if request.method == "POST":
        ''' {"user_name": "@Olzhas", "user_comment: like"}
        '''
        comment_post_user = request.get_json()
        user_post = User(comment_post_user["user_name"])
        user_post_comment = json.dumps(user_post, cls=CustomJSONEncoder)
        comment_user.append(json.loads(user_post_comment))
        return jsonify({"user_comment": comment_user})


@app.route('/twit/post/delete', methods=["DELETE"])
def delete_post():
    '''{"author": "@Ray","body": "Hello world"}
    '''
    post_user = request.get_json()
    post_user = delete(post_user, twits)
    return post_user


@app.route('/twit/post/update', methods=["PUT"])
def update_post_put():
    '''{"author": "@Ray","body": "And today, tomorrow, not everyone can watch. Or rather, not only everyone can watch, few can do it"}
    '''
    update = request.get_json()
    update = update_post(update, twits)
    return update


if __name__ == "__main__":
    app.run(debug=True)

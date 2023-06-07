from flask import make_response


class User:
    def __init__(self, user_name: str):
        self.user_name = user_name

    def user_comment(self, comment: str):
        return comment


def get_users_comment(post_user, twits):
    for user in twits:
        for key, value in post_user.items():
            if value == user[key]:
                return user
            if value != user[key]:
                continue
    return make_response("Такого пользователя нет", 400)


def delete(post_user, twits):
    for i in twits:
        if i == post_user:
            twits.remove(i)
            return twits
        else:
            return make_response("Такого поста нет", 400)


def update_post(update, twits):
    for i in twits:
        for key, value in update.items():
            if value == i[key]:
                i["body"] = update["body"]
    return twits
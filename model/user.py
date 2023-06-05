from flask import make_response


class User:
    def __init__(self, user_name: str):
        self.user_name = user_name

    def user_comment(self, comment: str):
        return comment, self.user_name


def get_users_comment(post_user, twits):
    for user in twits:
        for key, value in post_user.items():
            if value == user[key]:
                return user
            if value != user[key]:
                continue
    return make_response("Такого пользователя нет", 400)


fop = User("Olzhas")
print(fop.user_comment("Loh"))
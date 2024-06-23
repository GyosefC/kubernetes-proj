from docker.mini_project.app import mongo


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email


def save_user(username, email):
    user_data = {"username": username, "email": email}
    mongo.db.users.insert_one(user_data)


def get_users():
    users = mongo.db.users.find()
    return users

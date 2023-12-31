from models.ChatHistory import ChatHistory


def login(username, password):
    # TODO: Return JWT upon successful login
    return f"Logged in user '{username}'", 200

def register(username, password, role):
    # TODO: Create user row in DB upon successful registration
    return f"Registered user '{username}'", 201

def get_chat_history(user_id):
    return [chat.to_json() for chat in ChatHistory.query.filter_by(user_id=user_id).all()], 200
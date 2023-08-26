
def login(username, password):
    # TODO: Return JWT upon successful login
    return f"Logged in user '{username}'", 200

def register(username, password, role):
    # TODO: Create user row in DB upon successful registration
    return f"Registered user '{username}'", 201
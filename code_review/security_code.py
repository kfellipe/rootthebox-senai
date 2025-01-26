def authenticate(username, password):
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    return database.execute(query)

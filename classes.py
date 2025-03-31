class Client:

    def __init__(self, client_id, username, password):
        self.client_id = client_id
        self.username = username
        self.password = password

    @staticmethod
    def represent(client_id, username):
        print(f"Client with client ID: {client_id} is active with username: {username}")

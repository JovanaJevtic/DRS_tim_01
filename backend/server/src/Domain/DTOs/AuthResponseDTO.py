class AuthResponseDTO:
    def __init__(self, user_id=0, email=None, role=None, token=None):
        self.user_id = user_id
        self.email = email
        self.role = role
        self.token = token

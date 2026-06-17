class UserManager:
    def __init__(self, users):
        self.users = users

    def can_execute(self, username):
        return (
            username in self.users and
            self.users[username]["executed"] <
            self.users[username]["quota"]
        )

    def record_execution(self, username):
        self.users[username]["executed"] += 1

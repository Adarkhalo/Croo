from package import Utility


class Comment:
    def __init__(self, name: str, email: str, comment: str):
        self.name = name
        self.email = email
        self.comment = comment
        self.__validate_input()

    def serialize(self):
        return {
            'name': self.name,
            'email': self.email,
            'comment': self.comment
        }

    def __validate_input(self):
        if type(self.name) is not str:
            raise ValueError("Incorrect name format, should be str")
        if type(self.email) is not str:
            raise ValueError("Incorrect email format, should be str")
        if Utility.validate_email(self.email) is False:
            raise ValueError("Invalid email")
        if type(self.comment) is not str:
            raise ValueError("Incorrect comment format, should be str")

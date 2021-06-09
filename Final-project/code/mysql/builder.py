from mimesis import Person
from mysql.models import Users

person = Person()


class MySQLBuilder:
    def __init__(self, client):
        self.client = client

    def create_user(self, username=None, password=None, email=None, access=1, active=0):
        if username is None:
            username = person.username()[:16]
        if password is None:
            password = person.password(length=10)
        if email is None:
            email = person.email(unique=True)

        user = Users(
            username=username,
            password=password,
            email=email,
            access=access,
            active=active
        )
        self.client.session.add(user)
        self.client.session.commit()
        return user
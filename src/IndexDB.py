from bsddb3 import db

class IndexDB:
    database = None
    name = None

    def __init__(self, name):
        self.name = name
        self.database = db.DB()
        self.database.open(self.name)

    def get(self):
        return None



from sqlalchemy import exists
from database_setup import Base, CruiseLine
import db

class Line:
    def __init__(self, name):
        self.name = name

    def add_line(self):
        if not self.exists():
            self.add_line_to_db()
        return self.get_line()

    def exists(self):
        line_obj = db.session.query(exists().where(CruiseLine.name == self.name)).scalar()
        if not line_obj:
            return False
        return True

    def add_line_to_db(self):
        print("Adding Line %s" % self.name)
        new_line = CruiseLine(name = self.name)
        db.session.add(new_line)
        db.session.commit()

    def get_line(self):
        return db.session.query(CruiseLine).filter_by(name=self.name).one()



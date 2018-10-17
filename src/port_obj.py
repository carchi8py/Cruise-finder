from bs4 import BeautifulSoup
import requests
from sqlalchemy import exists
from database_setup import Base, CruiseLine, Ship, Port
import db
import sys

class Ports:
    def __init__(self, name):
        self.name = name

    def add_port(self):
        if not self.exists():
            self.add_port_to_db()
        return self.get_port()

    def exists(self):
        port_obj = db.session.query(exists().where(Port.name == self.name)).scalar()
        if not port_obj:
            return False
        return True

    def add_port_to_db(self):
        print("Adding Port %s" % self.name)
        new_port = Port(name=self.name)
        db.session.add(new_port)
        db.session.commit()

    def get_port(self):
        return db.session.query(Port).filter_by(name=self.name).one()
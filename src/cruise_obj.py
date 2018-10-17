from bs4 import BeautifulSoup
import requests
from sqlalchemy import exists
from database_setup import Base, CruiseLine, Ship, Cruise
import db
import sys

class Cruises:
    def __init__(self, cruse_id, date, destination, port_obj, nights, price, line_obj, ship_obj):
        self.id = cruse_id
        self.date = date
        self.destination = destination
        self.port_obj = port_obj
        self.nights = nights
        self.price = price
        self.line_obj = line_obj
        self.ship_obj = ship_obj

    def add_cruise(self):
        if not self.exists():
            self.add_cruise_to_db()
        return self.get_cruise()

    def exists(self):
        curise_obj = db.session.query(exists().where(Cruise.id == self.id)).scalar()
        if not curise_obj:
            return False
        return True

    def add_cruise_to_db(self):
        print("Adding Cruise %s" % self.id)
        new_ship = Cruise(id=self.id,
                        date=self.date,
                        line=self.line_obj,
                        ship=self.ship_obj,
                        destination=self.destination,
                        departs=self.port_obj,
                        nights=self.nights,
                        price=self.price)
        db.session.add(new_ship)
        db.session.commit()

    def get_cruise(self):
        return db.session.query(Cruise).filter_by(id=self.id).one()

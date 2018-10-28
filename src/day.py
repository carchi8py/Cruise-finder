from bs4 import BeautifulSoup
import requests
from sqlalchemy import exists
from database_setup import Base, CruiseLine, Ship, Cruise, Day
import db
import sys

class Days:
    def __init__(self, cruise, day, date, port, arrival, departure):
        self.id = int(str(cruise) + str(day))
        self.curise_id = cruise
        self.day = day
        self.date = date
        self.port_obj = port
        self.arrival = arrival
        self.departure = departure

    def add_day(self):
        if not self.exists():
            self.add_day_to_db()
        return self.get_day()

    def exists(self):
        day_obj = db.session.query(exists().where(Day.id == self.id)).scalar()
        if not day_obj:
            return False
        return True

    def add_day_to_db(self):
        print("Adding Day %s, to cruise %s" % (str(self.day), str(self.curise_id)))
        new_day = Day(id = self.id,
                      cruise_id = self.curise_id,
                      day = self.day,
                      date = self.date,
                      port = self.port_obj,
                      arrival = self.arrival,
                      Departure = self.departure)
        db.session.add(new_day)
        db.session.commit()


    def get_day(self):
        return db.session.query(Day).filter_by(id=self.id).one()

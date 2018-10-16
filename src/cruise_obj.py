from bs4 import BeautifulSoup
import requests
from sqlalchemy import exists
from database_setup import Base, CruiseLine, Ship
import db
import sys

class Cruise:
    def __init__(self, id):
        self.id

    def add_curise(self):
        if not self.exists():
            self.add_cruise_to_db()
        return self.get_cruise()

    def exists(self):
        curise_obj = db.session.query(exists().where(Cruise.id == self.id)).scalar()
        if not curise_obj:
            return False
        return True

    def add_cruise_to_db(self):
        cruise_url = self._curise_url()
        data = self._parse_cruise_data(cruise_url)


    def _curise_url(self):
        url = 'https://cruises.affordabletours.com/search/itsd/cruises/'
        return url + str(self.id) + '/'

    def _parse_cruise_data(self, cruise_url):
        data = {}
        r = requests.get(cruise_url)
        soup = BeautifulSoup(r.text, 'html.parser')


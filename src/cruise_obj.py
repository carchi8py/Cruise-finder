

from sqlalchemy import exists
from database_setup import Base
import db

class Cruise:
    def __init__(self, date, ship):
        self.date = date
        self.ship = ship

    def exists(self, date, ship):
        print(ship)


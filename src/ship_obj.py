
from sqlalchemy import exists
from database_setup import Base, CruiseLine, Ship
import db

class Ship:
    def __init__(self, name, build_year, refurbished_year, crew, passagers, bars, pools, casinos):
        self.name = name
        self.build_year = build_year
        self.refurbished_year = refurbished_year
        self.crew = crew
        self.passagers = passagers
        self.bars = bars
        self.pools = pools
        self.casinos = casinos

    def __init__(self, name):
        self.name = name

    def add_ship(self):
        if not self.exists():
            self.add_ship_to_db()
        return self.get_ship()

    def exists(self):
        ship_obj  = db.session.query(exists().where(Ship.name == self.name)).scalar()
        if ship_obj:
            return False
        return True

    def add_ship_to_db(self):
        print("Adding Ship %s" % self.name)
        new_ship = Ship(name = self.name)
        db.session.add(new_ship)
        db.session.commit()
        self.get_ship_data()

    def get_ship(self):
        return db.session.query(Ship).filter_by(name=self.name)

    def get_ship_data(self):
        ship_obj = self.get_ship()

    def _ship_url(self):
        url = "https://cruises.affordabletours.com/"
        line = ship.line.name
        # replace spaces with "_"
        line = line.replace(" ", "_")
        # Add Cruise to the end of the name
        line = line + "_Cruises"
        ship_name = ship.name
        ship_name = ship_name.replace(" ", "_")
        return url + line + "/" + ship_name

from bs4 import BeautifulSoup
import requests
from sqlalchemy import exists
from database_setup import Base, CruiseLine, Ship
import db
import sys

class Ships:
    def __init__(self, name, build_year, refurbished_year, crew, passagers, bars, pools, casinos):
        self.name = name
        self.build_year = build_year
        self.refurbished_year = refurbished_year
        self.crew = crew
        self.passagers = passagers
        self.bars = bars
        self.pools = pools
        self.casinos = casinos

    def __init__(self, name, line, line_obj):
        self.name = name
        self.line = line
        self.line_obj = line_obj

    def add_ship(self):
        if not self.exists():
            self.add_ship_to_db()
        return self.get_ship()

    def exists(self):
        ship_obj = db.session.query(exists().where(Ship.name == self.name)).scalar()
        if not ship_obj:
            return False
        return True

    def add_ship_to_db(self):
        print("Adding Ship %s" % self.name)
        ship_url = self._ship_url()
        data = self._parse_ship_data(ship_url)
        if data:
            new_ship = Ship(name = self.name,
                            build_year = data['build_year'],
                            refurbished_year=data['refurbished_year'],
                            crew=data['crew'],
                            passagers=data['passagers'],
                            bars=data['bars'],
                            pools=data['pools'],
                            casinos=data['casinos'],
                            line=self.line_obj)
        else:
            print(ship_url)
            sys.exit(1)
        db.session.add(new_ship)
        db.session.commit()

    def get_ship(self):
        return db.session.query(Ship).filter_by(name=self.name).one()

    def _ship_url(self):
        url = "https://cruises.affordabletours.com/"
        line = self.line
        # replace spaces with "_"
        line = line.replace(" ", "_")
        # Add Cruise to the end of the name
        line = line + "_Cruises"
        if line == 'Carnival_Cruises':
            ship_name = 'Carnival'+ self.name
        elif line == 'Crystal_Cruises':
            ship_name = 'Crystal' + self.name
        elif line == 'MSC_Cruises':
            ship_name = 'MSC' + self.name
        elif line == 'Celebrity_Cruises':
            ship_name = 'Celebrity' + self.name
        elif line == 'Norwegian_Cruises' and self.name != 'Pride of America':
            ship_name = 'Norwegian' + self.name
        elif line == 'Seabourn_Cruises':
            ship_name = 'Seabourn' + self.name
        elif line == 'Costa_Cruises':
            ship_name = 'Costa' + self.name
        else:
            ship_name = self.name
        ship_name = ship_name.replace(" ", "_")
        return url + line + "/" + ship_name

    def _parse_ship_data(self, ship_url):
        data = {}
        r = requests.get(ship_url)
        soup = BeautifulSoup(r.text, "html.parser")
        try:
            results = soup.find("ul", {"class": "medium-block-grid-8"})
            results = results.findAll("ul")
        except:
            print("Could not find ship %s", self.name)
            return False
        for each in results:
            if each.find("h5").text == "Built Year":
                data['build_year'] = int(each.find("h3").text)
            if each.find("h5").text == "Refurbished Year":
                data['refurbished_year'] = int(each.find("h3").text)
            if each.find("h5").text == "Crew":
                data['crew'] = int(each.find("h3").text)
            if each.find("h5").text == "Pax Capacity":
                data['passagers'] = int(each.find("h3").text)
            if each.find("h5").text == "Bars":
                data['bars'] = int(each.find("h3").text)
            if each.find("h5").text == "Pools":
                data['pools'] = int(each.find("h3").text)
            if each.find("h5").text == "Casinos":
                data['casinos'] = int(each.find("h3").text)
        if 'casinos' not in data:
            data['casinos'] = 0
        if 'refurbished_year' not in data:
            data['refurbished_year'] = data['build_year']
        if 'crew' not in data:
            data['crew'] = 0
        return data

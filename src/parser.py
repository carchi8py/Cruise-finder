from bs4 import BeautifulSoup
import requests
import sys
from cruise_obj import Cruises
from line_obj import Line
from ship_obj import Ships
from port_obj import Ports
import datetime
from re import sub


URL = "https://cruises.affordabletours.com/search/advanced_search"

def main(destination):
    more_cruises = True
    i = 1
    params = {"destination": destination}
    while more_cruises:
        try:
            cruises = find_search_results(i, params)
        except:
            more_cruises = False
            continue
        for cruise in cruises[1:]:
            cruise_data = get_cruise_data(cruise)
            new_line = Line(cruise_data[1])
            line_obj = new_line.add_line()
            new_ship = Ships(cruise_data[2], cruise_data[1], line_obj)
            ship_obj = new_ship.add_ship()
            new_port = Ports(cruise_data[4])
            port_obj = new_port.add_port()
            cruise_date = datetime.datetime.strptime(cruise_data[0], "%b %d, %Y").date()
            money_int = int(sub(r'[^\d.]', '', cruise_data[6]))
            new_cruise = Cruises(cruise_data[7], cruise_date, cruise_data[3], port_obj,
                                cruise_data[5], money_int, line_obj, ship_obj)
            new_cruise.add_cruise()

        i+=1


def find_search_results(page, params):
    params["Page"] = page
    r = requests.get(URL, params=params)
    print(r.url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find("table", {"class": "search-results"})
    return results.findAll("tr")


def get_cruise_data(cruise):
    """
    Parses a single row of the affordable tours cruise search results to get cruise information
    :param cruise: a single html row from the search results
    :return: a list of information on a single cruise
    """
    k = cruise.find("td", {"class": "table-date"})
    id = k.find("a")["href"].split("cruises/")[1].split('/')[0]
    date = cruise.find("td", {"class": "table-date"}).text
    line = cruise.find("td", {"class": "table-line"}).text
    ship = cruise.find("td", {"class": "table-ship"}).text
    destination = cruise.find("td", {"class": "table-destination"}).text
    departs = cruise.find("td", {"class": "table-departs"}).text
    nights = cruise.find("td", {"class": "table-nights"}).text
    price = cruise.find("td", {"class": "table-price"}).text
    return [date, line, ship, destination, departs, nights, price, id]



if __name__ == "__main__":
    main("21")
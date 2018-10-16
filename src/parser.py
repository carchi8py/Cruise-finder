from bs4 import BeautifulSoup
import requests
import sys
from cruise_obj import Cruise
from line_obj import Line
from ship_obj import Ship


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
            new_line.add_line()
            new_ship = Ship(cruise_data[2])

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
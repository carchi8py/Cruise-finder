from bs4 import BeautifulSoup
import requests
import sys
from cruise_obj import Cruises
from line_obj import Line
from ship_obj import Ships
from port_obj import Ports
from day import Days
import datetime
from re import sub


URL = "https://cruises.affordabletours.com/search/advanced_search"
INFO_URL = "https://cruises.affordabletours.com/search/itsd/cruises/"

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
            itinerary = get_crusie_day(cruise_data[7])
            parse_days(itinerary, cruise_data[7])

        i+=1


def parse_days(itinerary, curise_id):
    """
    Parse each day in a cruise itinerary.
    :param itinerary: The Cruise's itinerary in HTML format
    :param curise_id: The Cruise_id so that we can create a ForeignKey relation
    :return: nothing
    """
    i = 1
    for each in itinerary[1:]:
        days = each.findAll("td")
        arrival_time = None
        departure_time = None
        if len(days) < 4:
            return
        date = days[0].text.split(":")[1]
        date = datetime.datetime.strptime(date, "%b %d, %Y").date()
        port = days[1].text.split(":")[1]
        new_port = Ports(port)
        port_obj = new_port.add_port()
        arrival = days[2].text.split(":",1)[1]
        departure = days[3].text.split(":",1)[1]
        if "---" not in arrival:
            arrival_time = format_time(arrival)
        if "---" not in departure:
            departure_time = format_time(departure)
        new_day = Days(curise_id, i, date, port_obj, arrival_time, departure_time)
        new_day.add_day()
        i += 1

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

def get_crusie_day(cruise_id):
    """
    Grab the content of a specific cruise from affordable tours website
    :param cruise_id: The cruise ID to grab data from
    :return: The table that contains the cruise itinerary
    """
    r = requests.get(INFO_URL + str(cruise_id))
    print(r.url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find("table", {"id": "maintable"})
    return results.findAll("tr")

def format_time(unformatted_time):
    """
    Sanitize the times we get from the website so python can understand them
    :param unformatted_time: the unformated times
    :return: the formated times.
    """
    #Python hour format require a lead zero so, 1:00am become 01:00AM
    if len(unformatted_time.split(":")[0]) == 1:
        unformatted_time = "0" + unformatted_time
    #They use P.M. python time formating wants PM
    unformatted_time = unformatted_time.replace(".", "")
    #even though there using a 12 hour clock they sometime use 00 for 12:00am
    unformatted_time = unformatted_time.replace("00:", "12:")
    #Sometime they print Noon instead of 12:00 pm"
    if unformatted_time == "Noon":
        unformatted_time = "12:00 pm"
    return datetime.datetime.strptime(unformatted_time, "%I:%M %p").time()


if __name__ == "__main__":
    main("21")
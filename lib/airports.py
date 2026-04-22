import os
import csv

AIRPORTS_DAT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "share", "airports.dat"
)

def load_aiports_index():
    try:
        file_ = open(AIRPORTS_DAT_FILE, "r")
        reader = csv.reader(file_)
        airport_index = {}

        for line in reader:
            airport_index[line[4]] = line

        return airport_index
    except FileNotFoundError:
        return {}


AIRPORTS_INDEX = load_aiports_index()


def get_airport_gps_location(iata_code):
    if iata_code in AIRPORTS_INDEX:
        airport = AIRPORTS_INDEX[iata_code]
        return "%s,%s airport" % (airport[6], airport[7])  # , airport[1])
    return None

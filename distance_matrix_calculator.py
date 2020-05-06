from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests
import os

def create_distance_matrix(addresses):
    # if os.getenv('GOOGLE_DISTANCE_MATRIX_API_KEY') is not None:
    if False:
        distance_matrix, locations = create_distance_matrix_gdm(addresses)
    else:
        distance_matrix, locations = create_distance_matrix_osm(addresses)
    return distance_matrix, locations
    
# Using Google Distance Matrix API
def create_distance_matrix_gdm(addresses):
    API_key = os.getenv('GOOGLE_DISTANCE_MATRIX_API_KEY')
    # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
    max_elements = 100
    num_addresses = len(addresses) # 16 in this example.
    # Maximum number of rows that can be computed per request (6 in this example).
    max_rows = max_elements // num_addresses
    # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
    q, r = divmod(num_addresses, max_rows)
    dest_addresses = addresses
    distance_matrix = []
    # Send q requests, returning max_rows rows per request.
    for i in range(q):
        origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)

    # Get the remaining remaining r rows, if necessary.
    if r > 0:
        origin_addresses = addresses[q * max_rows: q * max_rows + r]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)

    locations = get_geocodes_osm(addresses)
    return distance_matrix, locations

# convert meters to miles
def get_miles(i):
     return i*0.000621371192

def build_distance_matrix(response):
    distance_matrix = []
    for row in response['rows']:
        row_list = [get_miles(row['elements'][j]['distance']['value']) for j in range(len(row['elements']))]
        distance_matrix.append(row_list)
    return distance_matrix

def send_request(origin_addresses, dest_addresses, API_key):
    """ Build and send request for the given origin and destination addresses."""
    def build_address_str(addresses):
        # Build a pipe-separated string of addresses
        address_str = ''
        for i in range(len(addresses) - 1):
            address_str += addresses[i] + '|'
        address_str += addresses[-1]
        return address_str

    request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
    origin_address_str = build_address_str(origin_addresses)
    dest_address_str = build_address_str(dest_addresses)
    request = request + '&origins=' + origin_address_str + '&destinations=' + \
                       dest_address_str + '&key=' + API_key
    response = requests.get(request).json()
    return response

def get_geocodes_osm(addresses):
    addresses_osm = [i.replace('+', ' ') for i in addresses]
    geolocator = Nominatim(user_agent="mutual_aid_tsp")
    locations = [geolocator.geocode(i) for i in addresses_osm]
    if any(i is None for i in locations):
        raise NotAllAddressesValidOSM
    return locations


# Using OpenStreetMap
def create_distance_matrix_osm(addresses):
    locations = get_geocodes_osm(addresses)
    distance_matrix = [[
        0 if i==j 
        else geodesic((i.latitude, i.longitude), (j.latitude, j.longitude)).miles
        for j in locations]
        for i in locations
    ]
    return distance_matrix, locations

def create_distance_matrix_from_geocodes(addresses):
    locations = [Address(address) for address in addresses]
    distance_matrix = [[
        0 if i==j 
        else geodesic((i.latitude, i.longitude), (j.latitude, j.longitude)).miles
        for j in locations]
        for i in locations
    ]
    print("locations")
    print(locations)
    print("distance_matrix")
    print(distance_matrix)
    
    return distance_matrix, locations

class NotAllAddressesValidOSM(Exception):
    pass

class Address(object):
    def __init__(self, address_dict):
        self.address = address_dict["address"]
        self.latitude = address_dict["lat"]
        self.longitude = address_dict["lng"]

    def __str__(self):
        return ('< address: {address}\n'
                  'latitude: {latitude}\n'
                  'longitude: {longitude}\n')\
        .format(**self.__dict__)

    def __repr__(self):
        return self.__str__()

from geopy.geocoders import Nominatim
from location import *

geolocator = Nominatim()
location = geolocator.reverse(Longitude, Latitude)
print(location.address)

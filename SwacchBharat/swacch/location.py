from geopy.geocoders import Nominatim
import googlemaps
def location():
    gmaps = googlemaps.Client(key='AIzaSyCuXHbiVdA2HY39QOyuUZ9P4xdluDgLKwQ')
    loc = gmaps.geolocate()
    #print(loc)
    a= loc['location']['lat']
    b= loc['location']['lng']
    Latitude= ("Latitude is " + str(a))
    Longitude= ("Longitude is " + str(b))
    geolocator = Nominatim()
    location = geolocator.reverse(Longitude, Latitude)
    print(location.address)






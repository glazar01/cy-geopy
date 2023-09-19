# pip install geopy 
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="myGeo")

# Important to use country_codes=['CY',] to narrow down the searching area for the API to CY
location = geolocator.geocode("Agios Ioannis Pafou", country_codes=['CY',])

# We get the coordinates of the location
print((location.latitude, location.longitude))

# Testing that the coordinates are correct
lat_long_str = f"{location.latitude}, {location.longitude}"
location_rev = geolocator.reverse(lat_long_str)
print(location_rev.address)
# pip install pandas
import pandas as pd
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError

# read csv file for total population
df = pd.read_csv("population.csv")
# set zero value to NaN 
df = df.fillna(0)
print(df)

class Coordinates:
    def __init__(self, latitude, longitude):
        self.lat = latitude
        self.long = longitude

    def __str__(self):
        return f"({self.lat}, {self.long})"

class DataRow:
    def __init__(self, location, population):
        self.location = location
        self.coordinates = Coordinates(*self.geopyAPI()[:2])
        self.address = self.geopyAPI()[2]
        self.population = population

    def __str__(self):
        return f"{self.location}, Population: {self.population}"
    
    def geopyAPI(self):
        geolocator = Nominatim(user_agent="myGeo")
        try:
            location = geolocator.geocode(self.location, country_codes=['CY'], timeout=None)
            if location is not None:
                address = geolocator.reverse(f"{location.latitude}, {location.longitude}").address
                return location.latitude, location.longitude, address
            else:
                # Handle the case where geocoding didn't return a location
                return None, None, None
        except (GeocoderServiceError) as e:
            # Handle service error
            print(f"Geocoding error: {e}")
            return None, None, None

class DataCity:
    
    def __init__(self, city, population):
        self.city = city
        self.coordinates = Coordinates(*self.geopyAPI())
        self.population = population

    def geopyAPI(self):
        geolocator = Nominatim(user_agent="myGeo")
        location = geolocator.geocode(self.city, country_codes=['CY',], timeout=None)
        # address = geolocator.reverse(f"{location.latitude}, {location.longitude}").address
        return location.latitude, location.longitude

    def __str__(self):
        return f"{self.city}{self.coordinates}, Population: {self.population}"

# store all the records
records = df.to_records()

# population only per city
populationPerCity = []
for record in records:
    if "District" in record.LOCATION:
        populationPerCity.append(DataCity(record.LOCATION, record.POPULATION))

# population per place 
populationPerPlace = []
for record in records:
    if "District" in record.LOCATION:
        city = record.LOCATION.split()[0]
    elif "Municipality" in record.LOCATION:
        municipality = ' '.join(record.LOCATION.split()[:-1])
    else:
        location = f"{record.LOCATION}, {municipality}, {city}"
        populationPerPlace.append(DataRow(location, record.POPULATION))

for city in populationPerCity:
    print(city)

for place in populationPerPlace:
    print(place)

# Create a dictionary to store city populations
city_data = {}
for city in populationPerCity:
    city_data[city.city] = city.population

# Create a dictionary to store place populations
place_data = {}
for place in populationPerPlace:
    place_data[place.location] = place.population

# Save city data to JSON
with open('city_population.json', 'w') as city_file:
    json.dump(city_data, city_file)

# Save place data to JSON
with open('place_population.json', 'w') as place_file:
    json.dump(place_data, place_file)

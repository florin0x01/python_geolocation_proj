from math import cos, asin, sqrt, pi, sin, atan2
from enum import Enum


class DistanceType(Enum):
    KM = 1
    MILES = 2


class StoreFinder:
    def __init__(self, list_stores, distance_type=DistanceType.KM):
        self.distance_type = distance_type
        self.stores = list_stores

    def __degrees_to_radians(self, degrees):
        return degrees * pi / 180

    # https://stackoverflow.com/questions/365826/calculate-distance-between-2-gps-coordinates
    # https://en.wikipedia.org/wiki/Great-circle_distance
    # Could have used the <nearest> endpoint from postcodes.io but this is local calc.
    def __distance_in_km_between_earth_coordinates(self, lat1, lon1, lat2, lon2):
        earth_radius_km = 6371
        d_lat = self.__degrees_to_radians(lat2 - lat1)
        d_lon = self.__degrees_to_radians(lon2 - lon1)

        lat1 = self.__degrees_to_radians(lat1)
        lat2 = self.__degrees_to_radians(lat2)

        a = sin(d_lat / 2) * sin(d_lat / 2) + sin(d_lon / 2) * sin(d_lon / 2) * cos(lat1) * cos(lat2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return earth_radius_km * c

    def __distance_in_miles_between_earth_coordinates(self, lat1, lon1, lat2, lon2):
        return self.__distance_in_km_between_earth_coordinates(lat1, lon1, lat2, lon2) * 0.621371

    def by_text(self, txt):
        if txt is None:
            return None
        if len(txt) == 0:
            return None
        txt = txt.lower()
        results1 = [e for e in self.stores if e['postcode'].lower().find(txt) != -1]
        results2 = [e for e in self.stores if e['name'].lower().find(txt) != -1]
        results1.extend(results2)
        return results1

    def __find_entry_by_postcode(self, postcode):
        entry = next((e for e in self.stores if e['postcode'] == postcode), None)
        if entry is None:
            return None
        return entry

    def __within_radius(self, entry, e, radius):
        if self.distance_type == DistanceType.KM:
            return self.__distance_in_km_between_earth_coordinates(entry['latitude'], entry['longitude'], e['latitude'],
                                                                   e['longitude']) < radius
        return self.__distance_in_miles_between_earth_coordinates(entry['latitude'], entry['longitude'], e['latitude'],
                                                               e['longitude']) < radius

    # Returns list of longitude latitude
    def by_radius(self, postcode, radius):
        if not isinstance(postcode, str):
            return []
        if len(postcode) < 3:
            return []
        if not (isinstance(radius, int) or isinstance(radius, float)):
            return []
        if radius <= 0:
            return []
        candidates = []
        entry = self.__find_entry_by_postcode(postcode)
        if entry is None:
            return []

        for e in self.stores:
            if 'longitude' not in e or 'latitude' not in e:
                continue
            if e['postcode'] == postcode:
                continue
            if e['longitude'] is None or e['latitude'] is None:
                continue
            if self.__within_radius(entry, e, radius):
                candidates.append((e['longitude'], e['latitude']))
        candidates_sorted = sorted(candidates, key=lambda x: x[1], reverse=True)  # sort by latitude north south
        return candidates_sorted

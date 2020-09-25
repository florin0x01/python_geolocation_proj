import json
from app_package.reversegeocoder import ReverseGeocoder
from app_package.storefinder import StoreFinder, DistanceType
from app_package.storesorter import StoreSorter


class StoreRepository:
    def __init__(self, file_name):
        self.json_file = None
        self.json_stores = None
        self.file_name = file_name
        self.store_sorter = None
        self.store_finder = None

    def __del__(self):
        if not self.json_file is None:
            self.json_file.close()

    def __from_file(self):
        self.json_file = open(self.file_name, "r")
        self.json_stores = json.loads(self.json_file.read())
        self.store_sorter = None
        self.store_finder = None

    def add_geocodes(self):
        if self.json_file is None:
            self.__from_file()
        postcodes = [entry['postcode'] for entry in self.json_stores]
        long_lats = ReverseGeocoder.get_longlat(postcodes)

        for entry in self.json_stores:
            if entry['postcode'] not in long_lats:
                continue
            entry['longitude'] = long_lats[entry['postcode']]['longitude']
            entry['latitude'] = long_lats[entry['postcode']]['latitude']

    def sort_by_name(self):
        if self.json_file is None:
            self.__from_file()
        if self.store_sorter is None:
            self.store_sorter = StoreSorter(self.json_stores)
        self.json_stores = self.store_sorter.sortByName()

    def find_by_radius(self, postcode, radius, distance_type=DistanceType.KM):
        if self.json_file is None:
            self.__from_file()
        if self.store_finder is None:
            self.store_finder = StoreFinder(self.json_stores, distance_type)
        return self.store_finder.by_radius(postcode, radius)

    def find_by_text(self, text):
        if self.json_file is None:
            self.__from_file()
        if self.store_finder is None:
            self.store_finder = StoreFinder(self.json_stores)
        return self.store_finder.by_text(text)

    def get_stores(self):
        return self.json_stores

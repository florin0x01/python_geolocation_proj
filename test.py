import unittest
import json
from app_package.storefinder import StoreFinder, DistanceType
from app_package.reversegeocoder import ReverseGeocoder

store_finder = None


class TestFinder(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestFinder, self).__init__(*args, **kwargs)
        self.json_file = open("stores.json", "r")
        self.json_stores = json.loads(self.json_file.read())
        self.store_finder = StoreFinder(self.json_stores)
        postcodes = [entry['postcode'] for entry in self.json_stores]
        long_lats = ReverseGeocoder.get_longlat(postcodes)
        for entry in self.json_stores:
            if entry['postcode'] not in long_lats:
                continue
            entry['longitude'] = long_lats[entry['postcode']]['longitude']
            entry['latitude'] = long_lats[entry['postcode']]['latitude']

    def __del__(self):
        self.json_file.close()

    def test_by_radius_expect_results_km(self):
        self.assertEqual(self.store_finder.by_radius('BN14 9GB', 30),
                         [(-0.325105, 51.061363), (-0.149078, 50.950564), (-0.757297, 50.841461), (-0.17436, 50.837916),
                          (-0.498092, 50.817576), (-0.667151, 50.798685)])

    def test_no_entry_by_that_postcode(self):
        self.assertEqual(self.store_finder.by_radius('SMTH', 3), [])

    def test_no_entry_by_negative_radius(self):
        self.assertEqual(self.store_finder.by_radius('', -1), [])

    def test_no_entry_by_invalid_radius(self):
        self.assertEqual(self.store_finder.by_radius('', 'string'), [])

    def test_no_entry_by_invalid_postcode(self):
        self.assertEqual(self.store_finder.by_radius(3, ''), [])

    def test_no_entry_by_empty_postcode(self):
        self.assertEqual(self.store_finder.by_radius('', 5), [])

    def test_search_by_text(self):
        self.assertEqual(self.store_finder.by_text('hello'), [])

    def test_search_by_text2(self):
        self.assertEqual(self.store_finder.by_text('br'),
                         [{'latitude': 51.392983,
                           'longitude': 0.112496,
                           'name': 'Orpington',
                           'postcode': 'BR5 3RP'},
                          {'latitude': 51.361584,
                           'longitude': 1.398326,
                           'name': 'Broadstairs',
                           'postcode': 'CT10 2RQ'},
                          {'latitude': 51.414577,
                           'longitude': -0.755313,
                           'name': 'Bracknell',
                           'postcode': 'RG12 1EN'},
                          {'latitude': 51.155923,
                           'longitude': 0.28795,
                           'name': 'Tunbridge_Wells',
                           'postcode': 'TN2 3FB'},
                          {'latitude': 51.482172,
                           'longitude': -0.314343,
                           'name': 'Brentford',
                           'postcode': 'TW8 8JW'}])

    def test_search_by_text3(self):
        self.assertEqual(self.store_finder.by_text('Orpington'),
                         [{'latitude': 51.392983,
                           'longitude': 0.112496,
                           'name': 'Orpington',
                           'postcode': 'BR5 3RP'}])

    def test_search_by_text4(self):
        self.assertEqual(self.store_finder.by_text('orpi'),
                         [{'latitude': 51.392983,
                           'longitude': 0.112496,
                           'name': 'Orpington',
                           'postcode': 'BR5 3RP'}])

    def test_search_by_text5(self):
        self.assertEqual(self.store_finder.by_text('Orpi'),
                         [{'latitude': 51.392983,
                           'longitude': 0.112496,
                           'name': 'Orpington',
                           'postcode': 'BR5 3RP'}])

    def test_search_by_text6(self):
        self.assertEqual(self.store_finder.by_text('TW8 8JW'),
                         [{'latitude': 51.482172,
                           'longitude': -0.314343,
                           'name': 'Brentford',
                           'postcode': 'TW8 8JW'}])

    def test_search_by_text7(self):
        self.assertEqual(self.store_finder.by_text('TW8'),
                         [{'latitude': 51.482172,
                           'longitude': -0.314343,
                           'name': 'Brentford',
                           'postcode': 'TW8 8JW'}])


if __name__ == '__main__':
    unittest.main()

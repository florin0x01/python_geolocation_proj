import requests
import json
import sys


class ReverseGeocoder:
    @staticmethod
    def get_longlat(list_of_codes):
        try:
            url = 'http://api.postcodes.io/postcodes'
            myrequest = {}
            myrequest['postcodes'] = list_of_codes

            response = requests.post(url, data=myrequest)
            response_json = json.loads(response.content)
            longlats = {}
            for entry in response_json['result']:
                if entry['result'] is None:
                    continue
                longlats[entry['query']] = {
                    'longitude': entry['result']['longitude'],
                    'latitude': entry['result']['latitude']
                }
            return longlats
        except:
            e = sys.exc_info()[0]
            print ("Exception ", e)
            return {}

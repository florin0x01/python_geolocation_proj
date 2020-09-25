from app_package.app import App

from app_package.storerepository import StoreRepository
import json

#Sample usage small script

app = App()
storeRepository = StoreRepository("stores.json")
storeRepository.sort_by_name()
storeRepository.add_geocodes()

output = app.list_stores(stores=storeRepository.get_stores())
print(output)

candidates = storeRepository.find_by_radius('BN14 9GB', 30)
searches = storeRepository.find_by_text('br')

print(candidates)

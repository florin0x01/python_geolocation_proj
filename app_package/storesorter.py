class StoreSorter:
    def __init__(self, list_stores):
        self.stores = list_stores

    def sortByName(self):
        return sorted(self.stores, key=lambda x: x['name'])

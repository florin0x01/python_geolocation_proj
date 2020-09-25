import falcon
import json
from app_package.app import App
from app_package.storerepository import StoreRepository

falcon_app = falcon.API()
app = App()
storeRepository = StoreRepository("stores.json")
storeRepository.add_geocodes()

class ListSearchResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.set_headers({
            'Content-Type': 'text/html'
        })
        resp.status = falcon.HTTP_200
        resp.body = app.display_stores()


class PostSearchResource(object):
    def on_post(self, req, resp):
        resp.set_headers({
            'Content-Type': 'text/json'
        })
        resp.status = falcon.HTTP_200
        body = req.media
        print('Media ', body['input'])

        if 'input' not in body:
            resp.status = falcon.HTTP_400
            resp.body = 'Bad Input'
        else:
            resp.body = json.dumps(storeRepository.find_by_text(body['input']))


list_search = ListSearchResource()
post_search = PostSearchResource()

falcon_app.add_route('/', list_search)
falcon_app.add_route('/search', post_search)

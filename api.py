from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from hashids import Hashids

app = Flask(__name__)
api = Api(app)

#urls = {}
urls = []
parser = reqparse.RequestParser()
hashids = Hashids()

class Url(Resource):
    def get(self, url_hash):
        #print('TODO-GET:url_hash=', url_hash)
        self.end_point = "http://localhost:5000/url/"
        for url in urls:
            if self.end_point+url_hash == url['short']:
                return url,200
        return {'id': 'Not Found', 'short': 'Not Found', 'url': 'Not Found'}

    def delete(self, url_hash):
        #print('TODO-DELETE')
        self.end_point = "http://localhost:5000/url/"
        for url in urls:
            if self.end_point+url_hash == url['short']:
                temp_id = url['id']
                urls.pop(temp_id)
                break

        return None, 204

def check_duplicate(self, input_url):
    url_found = False
    #print(urls)
    for url in urls:
        #print('input url' + input_url)
        #print(url['url'])
        #print(url)
        if input_url == url['url']:
            url_found = True
            break
    return url_found
        
class ShortenUrl(Resource):

    def post(self):
        self.end_point = "http://localhost:5000/url/"
        #print('TODO-POST:Shorten URL')
        #args = parser.parse_args()
        #input_url = args['url'] 
        input_url = request.form['url']
        
        if not urls:
            max_id = 0
            hashed_url = hashids.encrypt(0)
            #print('hashing the url' + hashed_url)
            hashed_url = self.end_point + hashed_url
            dict_item = {
                'id' : max_id,
                'short' : hashed_url,
                'url' : input_url
            }
            urls.append(dict_item)
            #urls[max_id] = dict_item
            #print(urls)
            return dict_item,201


        url_present = check_duplicate(self, input_url)
        if url_present == False:
            max_id = len(urls) + 1
            hashed_url = hashids.encrypt(max_id)
            hashed_url = self.end_point + hashed_url
            dict_item = {
                'id' : max_id,
                'short' : hashed_url,
                'url' : input_url
            }
            #urls[max_id] = dict_item
            urls.append(dict_item)
            return dict_item,201
        else:
            abort(409)



api.add_resource(ShortenUrl, '/url')
api.add_resource(Url, '/url/<string:url_hash>')

if __name__ == '__main__':
    app.run(debug=True)
from util import *
from databaseController import *
from productController import *

class apiController():

    def jsonExport(self, urlArgs):
        logger.info('[START] jsonExport()')

        query = ''

        if "query" in urlArgs:
            query = urlArgs["query"]

        info = dict()

        if 'minprice' in urlArgs:
            info['min_price'] = int(urlArgs['minprice'])
        if 'maxprice' in urlArgs:
            info['max_price'] = int(urlArgs['maxprice'])
        if 'condition' in urlArgs:
            info['conditie'] = urlArgs['condition']
        if 'country' in urlArgs:
            info['country'] = urlArgs['country']
        if 'city' in urlArgs:
            info['city'] = urlArgs['city']
        if 'category' in urlArgs:
            info['category'] = urlArgs['category']

        products = databaseController.getProductsByFilter(info, None, None, query)

        results = list()

        for product in products:

            item = dict()

            item["title"] = product[PROD_TITLE]
            item["description"] = product[PROD_DESCRIPTION]
            item["condition"] = product[PROD_CONDITIE]
            item["price"] = product[PROD_PRICE]
            item["currency"] = product[PROD_CURRENCY]
            item["category"] = product[PROD_CATEGORY]

            results.append(item)

        return json.dumps(results)


apiController = apiController()
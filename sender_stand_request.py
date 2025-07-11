from http.client import responses

import configuration
import requests
import data

def get_docs ():
    return requests.get(configuration.URL_SERVICE + configuration.DOC_PATH)

def get_logs():
    return requests.get(configuration.URL_SERVICE + configuration.LOG_MAIN_PATH,
                        params={"count":20})

def get_users_table():
    return requests.get(configuration.URL_SERVICE + configuration.USERS_TABLE_PATH)

def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json = body,
                         headers=data.headers)


##Agregar productos a un kit##
def post_product_kit(products_ids):
    return requests.post(configuration.URL_SERVICE + configuration.PRODUCTS_KITS_PATH,
                         json= products_ids,
                         headers=data.headers)
response = post_product_kit(data.product_ids)

print(response.status_code)
print(response.json())


import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
  print(kwargs)
  print('GET from {}'.format(url))
  
  try:
    # if(kwargs["api_key"]):
    #   response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs,
    #                           auth=HTTPBasicAuth('apikey', kwargs["api_key"]))
    # else:
      response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
  except:
    print('Network exception occurred')
  
  status_code = response.status_code
  print('With status {}'.format(status_code))
  json_data = json.loads(response.text)
  return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload):
  try:
    response = requests.post(url, json=json_payload)
    print(response) 
  except(requests.exceptions.RequestException, ConnectionResetError) as err:
    print('Error occurred while posting review: ', err)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
  results = []
  json_result = get_request(url)
  
  if json_result:
    dealers = json_result['rows']
    for dealer in dealers:
      dealer_doc = dealer['doc']
      dealer_obj = CarDealer(address=dealer_doc["address"], 
                             city=dealer_doc["city"], 
                             full_name=dealer_doc["full_name"],
                             id=dealer_doc["id"], 
                             lat=dealer_doc["lat"], 
                             long=dealer_doc["long"],
                             short_name=dealer_doc["short_name"],
                             st=dealer_doc["st"], 
                             zip=dealer_doc["zip"])
      results.append(dealer_obj)
  
  return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
  results = []
  json_result = get_request(url, dealer_id = dealer_id)

  if json_result:
    reviews = json_result['data']
    for review in reviews['docs']:
      review_obj= DealerReview(dealership=review["dealership"],
                               name=review["name"],
                               purchase=review["purchase"],
                               review=review["review"],
                               purchase_date=review["purchase_date"],
                               car_make=review["car_make"],
                               car_model=review["car_model"],
                               car_year=review["car_year"],
                               sentiment=analyze_review_sentiments(review['review']),
                               id=review["id"])
      results.append(review_obj)

  return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
  api_key = "xghC0IkTzlrjwMra7ottsH8xZ8VJFYDXAvJLKLtrjddd"
  url = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/85550ee6-f388-4f45-b5ef-6f4fd9a5e73c'
  
  try:
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07', authenticator=authenticator)
    natural_language_understanding.set_service_url(url)

    response = natural_language_understanding.analyze(text = text, features=Features(sentiment=SentimentOptions(targets=[text])), language="en", return_analyzed_text=True).get_result()
    # print(json.dumps(response, indent=2))
    return response['sentiment']['document']['label']

  except(requests.exceptions.RequestException, ConnectionResetError) as err:
    print("connection error")
    return {"error": err}

def get_dealer_by_id(url, dealer_id):
  result = {}
  json_result = get_request(url)
  # print(json_result)
  
  if json_result:
    dealers = json_result['rows']
    for dealer in dealers:
      dealer_doc = dealer['doc']
      if dealer_doc['id'] == dealer_id:
        dealer_obj = CarDealer(address=dealer_doc["address"], 
                              city=dealer_doc["city"], 
                              full_name=dealer_doc["full_name"],
                              id=dealer_doc["id"], 
                              lat=dealer_doc["lat"], 
                              long=dealer_doc["long"],
                              short_name=dealer_doc["short_name"],
                              st=dealer_doc["st"], 
                              zip=dealer_doc["zip"])
        result = dealer_obj
  
  # print(result)
  
  return result
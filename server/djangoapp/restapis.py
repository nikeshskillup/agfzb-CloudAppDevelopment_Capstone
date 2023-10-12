import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import time
 

def analyze_review_sentiments(text):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/84fa55a8-9345-4506-93e5-08cf32b2b02f"
    api_key = "Uor15izqvTNG6I8Zx5Y8kzWFjf6twBh7VAKVFKP7xSjZ"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    return(label)


def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)

    if json_result:
        # The json_result is expected to be a list of dealers, not a dictionary
        # Loop through the list to process each dealer
        for dealer in json_result:
            dealer_obj = CarDealer(
                address=dealer.get("address"),
                city=dealer.get("city"),
                id=dealer.get("id"),
                lat=dealer.get("lat"),
                long=dealer.get("long"),
                full_name=dealer.get("full_name"),
                st=dealer.get("st"),
                zip=dealer.get("zip"),
                short_name=dealer.get("short_name")
            )
            results.append(dealer_obj)

    return results


def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    # print('json_result from line 54',json_result)

    if json_result:
        dealers = json_result
        dealer_doc = dealers[0]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],
                                st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc.get("short_name"))
    return dealer_obj


def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    # print(json_result)
    
    if json_result:
        # The structure of json_result should be a list, not a dictionary
        # So, loop through the list to process each dealer review
        for dealer_review in json_result:
            review_obj = DealerReview(
                dealership=dealer_review.get("dealership"),
                name=dealer_review.get("name"),
                purchase=dealer_review.get("purchase"),
                review=dealer_review.get("review")
            )
            
            # Use .get() to safely access optional fields
            review_obj.id = dealer_review.get("id")
            review_obj.purchase_date = dealer_review.get("purchase_date")
            review_obj.car_make = dealer_review.get("car_make")
            review_obj.car_model = dealer_review.get("car_model")
            review_obj.car_year = dealer_review.get("car_year")
            
            sentiment = analyze_review_sentiments(review_obj.review)
            print(sentiment)
            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results


def get_request(url, **kwargs):
    
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# def post_request(url, payload, **kwargs):
#     print(kwargs)
#     print("POST to {} ".format(url))
#     print(payload)
#     response = requests.post(url, params=kwargs, json=payload)
#     status_code = response.status_code
#     print("With status {} ".format(status_code))
#     json_data = json.loads(response.text)
#     return json_data

def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    try:
        response = requests.post(url, params=kwargs, json=payload)
        response.raise_for_status()  # Check for HTTP errors

        # Check if the response contains valid JSON
        try:
            json_data = response.json()
            return json_data
            print(json_data)
        except json.JSONDecodeError:
            print("Invalid JSON response")
            return None
    except requests.exceptions.RequestException as e:
        print("Request Exception:", e)
        return None

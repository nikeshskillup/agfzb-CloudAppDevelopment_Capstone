import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import time
 

def analyze_review_sentiments(text):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/a7d55b2b-30e4-4d58-91a1-bd84cb7b5c14"
    api_key = "S8Ncd3903aq7KoTo6MJPqi3nrpIvivQuWJdwqmMQifFK"
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
        # Check if the JSON result is a valid list
        if isinstance(json_result, list):
            dealers = json_result
            for dealer in dealers:
                # Create a CarDealer object with values from the JSON data
                dealer_obj = CarDealer(
                    address=dealer.get("address"),
                    city=dealer.get("city"),
                    id=dealer.get("id"),
                    lat=dealer.get("lat"),
                    long=dealer.get("long"),
                    full_name=dealer.get("full_name"),
                    st=dealer.get("st"),
                    zip=dealer.get("zip")
                )
                results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    print('json_result from line 54', json_result)

    dealer_obj = None  # Initialize dealer_obj with None to ensure it's always defined

    if json_result:
        dealers = json_result.get("body")

        if dealers:
            dealer_doc = dealers[0]
            dealer_obj = CarDealer(
                address=dealer_doc.get("address"),
                city=dealer_doc.get("city"),
                id=dealer_doc.get("id"),
                lat=dealer_doc.get("lat"),
                long=dealer_doc.get("long"),
                full_name=dealer_doc.get("full_name"),
                st=dealer_doc.get("st"),
                zip=dealer_doc.get("zip")
            )

    return dealer_obj



def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")

    # Prepare API request parameters
    params = {"id": id} if id else {}

    try:
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'})
        response.raise_for_status()  # Check for HTTP request errors

        json_result = response.json()
        reviews = json_result.get("body", {}).get("data", {}).get("docs", [])

        for dealer_review in reviews:
            review_obj = DealerReview(
                dealership=dealer_review.get("dealership", ""),
                name=dealer_review.get("name", ""),
                purchase=dealer_review.get("purchase", False),
                review=dealer_review.get("review", ""),
                id=dealer_review.get("id", ""),
                purchase_date=dealer_review.get("purchase_date", ""),
                car_make=dealer_review.get("car_make", ""),
                car_model=dealer_review.get("car_model", ""),
                car_year=int(dealer_review.get("car_year", "").split()[0])
            )

            sentiment = analyze_review_sentiments(review_obj.review)
            review_obj.sentiment = sentiment
            results.append(review_obj)

    except requests.exceptions.RequestException as e:
        print("Network exception occurred:", str(e))

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


def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
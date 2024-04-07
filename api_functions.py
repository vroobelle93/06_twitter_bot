# Imports
import json
import requests
from requests_oauthlib import OAuth1Session

lines = "---------------------"


def get_airly_data():
    """
    Gets air quality data using airly.org API. Currently the air quality is obtained for Warsaw.
    Return: dict object with 
        {
        'value': <caqi index value> - float
        'description': <text descirption of current air quality in Warsaw> - str
        }
    """

    # Define reqest parameters
    consumer_key = open("secrets/airly_api_key.txt").read()
    url = 'https://airapi.airly.eu/v2/measurements/point'
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'pl',
        'apikey': consumer_key
    }
    params = {
        'lat': '52.25353625902821',
        'lng': '20.978990723318343'
    }

    # Make request and 
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        print(f"\n{lines}\nData collected successfully!\n{lines}\n")
    else:
        print(f"\n{lines}\nRequest error! Status code: {response.status_code}\n{lines}\n")

    # Get result values
    response_dict = response.json()
    value = response_dict['current']['indexes'][0]['value']
    description = response_dict['current']['indexes'][0]['description']
    result = {'value': value, 'description': description}

    return result



def print_airly_data():
    """
    Prints air quality data for Warsaw
    Returns: None
    """
    airly_data = get_airly_data()
    print(f"\n{lines}\nToday's report for air quality in Warsaw using airly.org data:")
    print(f" - CAQI index: {airly_data['value']}")
    print(f" - {airly_data['description']}")
    print(f"{lines}\n")

    return None



def connect_to_twitter():
    """
    Connects to twitter API.
    Returns: an oauth object needed to post a tweet.
    """

    # Get api secrets
    print("Getting secrets")
    consumer_key = open("secrets/twitter_api_key.txt").read()
    consumer_secret = open("secrets/twitter_api_key_secret.txt").read()
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    # Check api keys validity
    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        print(
            "There may have been an issue with the consumer_key or consumer_secret you entered."
        )

    # Get keys from response
    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    print("Got OAuth token: %s" % resource_owner_key)

    # Get authorization
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    print("Please go here and authorize: %s" % authorization_url)
    verifier = input("Paste the PIN here: ")

    # Get the access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )

    # Fetch access tokens
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    print(f"{lines}\nConnection succesful!\n{lines}")
    # print(f"\nType: {type(oauth)}") # TODO: Connection validation

    return oauth



def post_tweet(oauth_object, text):

    """
    Posts a tweet if connection is already established
    Returns: null
    """

    # Define request parameters
    payload = {"text": text}

    # Make request
    response = oauth_object.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    # Print result
    print("Response code: {}".format(response.status_code))
    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )
    else: print(f"\n{lines}\nTweet posted successfully!\n{lines}\n")

    return None

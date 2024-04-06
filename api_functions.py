lines = "---------------------"

def connect_to_twitter():
    """
    Connects to twitter API.
    Returns: an oauth object needed to post a tweet.
    """
    
    # Imports 
    from requests_oauthlib import OAuth1Session
    import os

    # Get api secrets
    print("Getting secrets")
    consumer_key = open("secrets/api_key.txt").read()
    consumer_secret = open("secrets/api_key_secret.txt").read()
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        print(
            "There may have been an issue with the consumer_key or consumer_secret you entered."
        )

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
    print(f"\nType: {type(oauth)}")
    # print(f"Length: {len(oauth)}\n")

    return oauth


def post_tweet(oauth_object, text):

    """
    Posts a tweet if connection is already established
    """

    payload = {"text": text}
    response = oauth_object.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    print("Response code: {}".format(response.status_code))
    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )
    else: print(f"\n{lines}\nTweet posted successfully!\n{lines}\n")

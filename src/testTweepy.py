import webbrowser

import tweepy

"""
    Query the user for their consumer key/secret
    then attempt to fetch a valid access token.
"""

if __name__ == "__main__":

    #consumer_key = input('Consumer key: ').strip()
    #consumer_secret = input('Consumer secret: ').strip()
    consumer_key = 'lSjQ9ctPFYbN4UwAAKPJ2PLIh'
    consumer_secret = 'BQaeK9KkTC2giAwVsZbo4yfwgyByBvjdI50PnsxFTWAe7gxWOL'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # Open authorization URL in browser
    webbrowser.open(auth.get_authorization_url())

    # Ask user for verifier pin
    pin = input('Verification pin number from twitter.com: ').strip()

    # Get access token
    token = auth.get_access_token(verifier=pin)

    # Give user the access token
    print ('Access token:', token)
    #print ('  Key: %s' % token.key)
    #print ('  Secret: %s' % token.secret)
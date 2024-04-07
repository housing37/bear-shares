# # from twitter import Twitter, OAuth
# # from twitter import OAuth
# import twitter

# # Authenticate to Twitter
# consumer_key = 'ufotTV5H0BMXgCS9p1Hf9LOM6'
# consumer_secret = 'Cped9xDs4T0gpC0guq9CVETAMryB6jqTMhyHmb0f3wfLorBKKX'
# access_token = '1754679966657056768-9PKkUuNWKvpTBuPjTh8q9r9LBmX14w'
# access_token_secret = 'CLw7QEu83Y7NI0lXTOMXGBRMErDgb9nxO9rSPJUY8A8bo'

# # oauth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret)

# # Create Twitter API object
# # twitter_api = Twitter(auth=oauth)
# twitter_api = twitter.Api(consumer_key=consumer_key,
#                   consumer_secret=consumer_secret,
#                   access_token_key=access_token,
#                   access_token_secret=access_token_secret)
# # Post a tweet
# tweet_text = "Hello from Python-Twitter!"
# twitter_api.statuses.update(status=tweet_text)
# print("Tweet posted successfully!")


import tweepy, requests, os
import requests

# Authenticate to Twitter
USE_BEAR_SHARES = False 
if not USE_BEAR_SHARES:
    # *** WARNING *** _ SAVE THESE KEYS BEFORE DELETING!
    # @SolAudits 
    # BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAA2FsQEAAAAAMQbDq1ye%2FCVB8WhHhiK%2FLI5gHnk%3DoAlPyP7Aef1nhtQsVRtitde8zUtaOuqXzEXsWbpal34vM0OBaH'
    # CLIENT_ID = 'cEp3SWhCSFlOWnBCRm81dEc2MDE6MTpjaQ'
    # CLIENT_SECRET = 'ypu_utp8dSHIdf8eaHVXeRK9ajyZIF9qgc2cap3GaTbv1ZEQpq'
    CONSUMER_KEY = 'ufotTV5H0BMXgCS9p1Hf9LOM6'
    CONSUMER_SECRET = 'Cped9xDs4T0gpC0guq9CVETAMryB6jqTMhyHmb0f3wfLorBKKX'
    ACCESS_TOKEN = '1754679966657056768-9PKkUuNWKvpTBuPjTh8q9r9LBmX14w'
    ACCESS_TOKEN_SECRET = 'CLw7QEu83Y7NI0lXTOMXGBRMErDgb9nxO9rSPJUY8A8bo'
else:
    # *** WARNING *** _ SAVE THESE KEYS BEFORE DELETING!
    # @BearSharesX
    # BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAAWFsQEAAAAAUUWby7USFVAw4q7afJ9nogg1eqE%3DfJKRgoyT6QmKyx0I2fFfgeozryxg6goSftwyaCJuzGzNEp1HIG'
    # CLIENT_ID = 'aEdic09QQV9HQ0xqZU5qMmJCM046MTpjaQ'
    # CLIENT_SECRET = 'woh8CPR8Fuezm6DcBdAGyjQjkhm1LJ1uTL4AEcBMYcJueM4y_u'
    CONSUMER_KEY = 'HdZLxkPGZNAzWOzFlVNEqxIeP'
    CONSUMER_SECRET = 'f2yUKDkLniQKEwouoheUbcJxFNPR2brieGQPq6t0gFGFGdV2dJ'
    ACCESS_TOKEN = '1756813801020596224-UBAFOB3xtW6xrVykGBPKAovZ6kDiMd'
    ACCESS_TOKEN_SECRET = 'qKNnDiSZrRFGbR4WCey2MXpG3XNLpmfTDa2jzeSMZxq1P'

# Authenticate to Twitter
client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)
auth = tweepy.OAuth1UserHandler(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET,
)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)

# # Create tweet
# message = " MESSAGE "

# # Upload image
# media = api.media_upload("tweet_img.png")

# # Post tweet with image
# client.create_tweet(text=message, media_ids=[media.media_id])
# print("Tweeted!")

# Post Tweet
# message = " MESSAGE "

# tweet_text = "Hello from Tweepy!"
# client.create_tweet(text=tweet_text)
# print("Tweeted!")

# Download the image
img_url = 'https://tse4.mm.bing.net/th/id/OIG1.7wE2IMsijJKr5ZD3McvA'
img_file = 'image.jpg'
response = requests.get(img_url)
if response.status_code == 200:
    with open(img_file, 'wb') as image_file:
        image_file.write(response.content)
else:
    print("Failed to download image.")

# Upload the image to Twitter
media = api.media_upload(img_file)

# Post Tweet with the attached image
tweet_text = "Test from Tweepy\n w/ image!"
response = client.create_tweet(text=tweet_text, media_ids=[media.media_id])
# Extract the tweet data from the response
tweet_data = response.data

# Extract the tweet text from the tweet data
tweet_text = tweet_data['text']
idx_start = tweet_text.find('http')
url = tweet_text[idx_start::]
print(f'response: {response}')
print(f'tweet_data: {tweet_data}')
print(f'tweet_text: {tweet_text}')
print(f'idx_start: {idx_start}')
print(f'\nresponse: {response}')
print(f'\nurl: {url}')
# api.update_status(status=tweet_text, media_ids=[media.media_id])
print("Tweeted with image!")

# Delete the image file
os.remove(img_file)
print("Image file deleted.")

# # auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# # Create API object
# api = tweepy.API(auth)
# try:
#     api.verify_credentials()
#     print("Authentication OK")
# except:
#     print("Error during authentication")

# # Post a tweet
# tweet_text = "Hello from Tweepy!"
# api.update_status(tweet_text)
# print("Tweet posted successfully!")

import tweepy
from django.conf import settings

def get_twitter_api(access_token, access_token_secret):
    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET
    )
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Try a basic check
    try:
        api.verify_credentials()
        print("✅ Twitter credentials verified")
    except Exception as e:
        print("❌ Invalid credentials:", e)

    return api


def fetch_user_tweets_v2(username):
    client = tweepy.Client(bearer_token=settings.TWITTER_BEARER_TOKEN)

    # Get user ID from username
    user = client.get_user(username=username)
    user_id = user.data.id

    # Fetch tweets using v2
    response = client.get_users_tweets(id=user_id, max_results=5)

    return response.data if response.data else []


from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
import tweepy
from django.conf import settings
from django.urls import reverse
from .models import UserProfile
from .utils.twitter_api import get_twitter_api
from django.contrib.auth.decorators import login_required
from .utils.twitter_api import get_twitter_api, fetch_user_tweets_v2
from .forms import RegisterForm, TweetForm

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('dashboard_home')
    else:
        form = RegisterForm()
    return render(request, 'dashboard/register.html', {'form': form})

@login_required
def dashboard_home(request):
    user_profile = request.user.userprofile
    tweets = []
    twitter_username = None
    tweet_form = TweetForm()  # 👈 this should always be passed

    if user_profile.twitter_access_token and user_profile.twitter_access_token_secret:
        try:
            api = get_twitter_api(
                user_profile.twitter_access_token,
                user_profile.twitter_access_token_secret
            )
            twitter_user = api.verify_credentials()
            twitter_username = twitter_user.screen_name

            # ✅ Fetch tweets
            tweets = fetch_user_tweets_v2(twitter_username)

            # ✅ Handle tweet form
            if request.method == 'POST':
                tweet_form = TweetForm(request.POST)
                if tweet_form.is_valid():
                    tweet_text = tweet_form.cleaned_data['tweet']
                    api.update_status(status=tweet_text)
                    print("✅ Tweet posted successfully")
                    return redirect('dashboard_home')

        except Exception as e:
            print("❌ Error:", e)

    return render(request, 'dashboard/home.html', {
        'twitter_username': twitter_username,
        'tweets': tweets,
        'tweet_form': tweet_form,  # 👈 make sure this is passed
    })


# Redirect to Twitter
@login_required
def twitter_login(request):
    try:
        auth = tweepy.OAuth1UserHandler(
            settings.TWITTER_API_KEY,
            settings.TWITTER_API_SECRET,
            callback=request.build_absolute_uri(reverse('twitter_callback'))
        )

        redirect_url = auth.get_authorization_url()
        request.session['request_token'] = auth.request_token  # ✅ set session
        print("✅ Stored request_token in session:", auth.request_token)

        return redirect(redirect_url)

    except Exception as e:
        print("❌ Twitter login error:", e)
        return redirect('dashboard_home')



@login_required
def twitter_callback(request):
    try:
        request_token = request.session.get('request_token')
        verifier = request.GET.get('oauth_verifier')

        print("🌀 request_token from session:", request_token)

        if not request_token:
            print("⚠️ request_token missing in session.")
            return redirect('twitter_login')

        auth = tweepy.OAuth1UserHandler(
            settings.TWITTER_API_KEY,
            settings.TWITTER_API_SECRET
        )

        # ✅ Critical: set manually
        auth.request_token = request_token

        access_token, access_token_secret = auth.get_access_token(verifier)

        profile = request.user.userprofile
        profile.twitter_access_token = access_token
        profile.twitter_access_token_secret = access_token_secret
        profile.save()

        print("✅ Tokens saved for:", request.user.username)
        return redirect('dashboard_home')

    except Exception as e:
        print("❌ Twitter callback error:", e)
        return redirect('dashboard_home')

def get_twitter_api(access_token, access_token_secret):
    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET
    )
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api


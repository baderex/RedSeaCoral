from Scweet.scweet import scrape
from Scweet.user import get_user_information, get_users_following, get_users_followers



data = scrape(words=["debries","plastic"], since="2021-09-30", from_account = None, interval=1, 
              headless=True, display_type="Latest", save_images=True, 
              resume=False, filter_replies=False, proximity=False)

data.to_csv("latest_tweets.csv")
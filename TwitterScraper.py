import tweepy
import pandas as pd
import warnings
import json
warnings.filterwarnings("ignore")

# Opening credentials file
f = open('credentials.json')  
data = json.load(f)

# Authorize to tweepy
authorization = tweepy.OAuth2AppHandler(data['consumer_key'], data['consumer_secret'])
api = tweepy.API(authorization,wait_on_rate_limit=True)

#create a twitter cursor obj
tweets_obj = tweepy.Cursor(api.search_tweets,q="austin", lang = "en", tweet_mode='extended').items(5000)

#fetch only required columns
tweets_list = [[tweet.full_text, tweet.user, tweet.retweet_count] for tweet in tweets_obj]
graph_df = pd.DataFrame()
entire_data_df = pd.DataFrame()


# converting json data to dataframe
for tweet in tweets_list:
  dict1 = tweet[1]._json
  dict2 = {'Tweet': tweet[0],'Retweet_count': tweet[2] }
  merged_dict = {**dict1,**dict2}
  entire_data_df = entire_data_df.append(merged_dict, ignore_index = True)
  temp_df = {'Tweeter': '@'+tweet[1].screen_name, 'Tweet': tweet[0]}
  graph_df = graph_df.append(temp_df, ignore_index = True)

# Dump tweets data
graph_df.to_csv('df_for_graph.csv')
entire_data_df.to_csv('entire_data_df.csv')
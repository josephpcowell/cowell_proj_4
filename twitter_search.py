from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream, API

keywords = ["vegan", "veganism"]

access_token = "1921879345-ZWORqpOrCvBNlYarCaJucUrwYK5kDGP9eckgMHI"
access_token_secret = "ucVJX0dkXywIDsRNBa2VfQlY7oZCLk0zlrVSVbOPA7vDv"
consumer_key = "vkkBaYfbVIx6PFvYT3uFH3tXh"
consumer_secret = "7h7owpn6rrzhHqxNQHjcYn3etCew8CqanLCQxkhSyELMvBDX6S"


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)
search_results = api.search(q="vegan", count=100)

# COMMAND LINE
# Set max tweets
# Set search information
snscrape --jsonl --max-results 5000 twitter-search "#vegan since:2016-08-01 until:2016-10-01" > tw2016.txt
snscrape --jsonl --max-results 5000 twitter-search "#vegan since:2020-08-01 until:2020-10-01" > tw2020.txt
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

keywords = ["vegan", "veganism"]

access_token = "1921879345-ZWORqpOrCvBNlYarCaJucUrwYK5kDGP9eckgMHI"
access_token_secret = "ucVJX0dkXywIDsRNBa2VfQlY7oZCLk0zlrVSVbOPA7vDv"
consumer_key = "vkkBaYfbVIx6PFvYT3uFH3tXh"
consumer_secret = "7h7owpn6rrzhHqxNQHjcYn3etCew8CqanLCQxkhSyELMvBDX6S"


class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":

    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    stream.filter(track=keywords)

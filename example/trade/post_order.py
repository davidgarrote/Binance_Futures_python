from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
import pyotp
import pprint
import tweepy
import secrets

#Uses Tweetpy to access Twitter API
print("Logging in Twitter's API...")
auth = tweepy.OAuthHandler(secrets.API_Key, secrets.API_Secret_Key)
auth.set_access_token(secrets.Access_Token, secrets.Token_Secret)
api = tweepy.API(auth)
print("Success!")
print("Waiting for a match...")


#Filters out mentions and RTs
def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True

#Listens for Musk writing about Doge and opens a DOGEUSDTPERP position on Binance Futures of a defult 1000 Dogges
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if from_creator(status):
            tweet = status.text.lower()
            if "doge" in tweet:
                request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
                result = request_client.post_order(symbol="DOGEUSDT", side=OrderSide.BUY, ordertype=OrderType.MARKET, quantity=1000)
                print ("Elon Musk just tweeted about DOGE!!")
                print("Rushing to buy a bag od doggies")
                PrintBasic.print_obj(result)
            return True
        return True


    def on_error(self, status_code):
        if status_code == 420:
            print("Error 420")
            #returning False in on_error disconnects the stream
            return False
    
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)   
myStream.filter(follow=['44196397'])  


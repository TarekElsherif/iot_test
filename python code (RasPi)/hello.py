import sys
from pubnub import Pubnub

pubnub = Pubnub(publish_key='pub-c-df137065-b5ca-4b1d-841a-3f547ec9b6f0',
                subscribe_key='sub-c-875a6a50-d26d-11e5-b684-02ee2ddab7fe')

channel = 'hello'

data = {
  'username': 'Tarek',
  'message': 'Hello World from Pi!'
}

def callback(m):
  print(m)

pubnub.publish(channel, data, callback=callback, error=callback)

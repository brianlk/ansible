import os
import sys
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "AC53a1fac3761853d650fa80617b98e4e0"
auth_token = "494535703e1161e7ed53a3214d4bdfae"
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body=sys.argv[1],
                     from_='+18562812766',
                     to='+85260184719'
                 )

print(message.status)

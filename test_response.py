#!/bin/python3

import time
import os
from slackclient import SlackClient

# request hostname
BOT_NAME = 'cads_north'

# needs to be hidden!
# TODO follow these instructions: https://www.fullstackpython.com/blog/build-first-slack-bot-python.html to hide the key
# token = os.environ.get('SLACK_TOKEN')
token = "not valid"

slack_client = SlackClient(token)



if __name__ == "__main__":
    print(slack_client.api_call("api.test"))
    print(slack_client.api_call("channels.info", channel="1234567890"))
    print(slack_client.api_call(
        "chat.postMessage", channel="#mp_testbed", text="Hello from Python! :tada:",
        username='cads_north', icon_emoji=':point_up_2:'))

    print("Other Test! \n\n")
    if slack_client.rtm_connect():
        while True:

            text_in = slack_client.rtm_read()
            # print("incoming" + str(text_in) + str(type(text_in)))
            for text in text_in:
                if text['type'] == 'message' and 'subtype' not in dict(text).keys():
                    # print("text: " + str(text))
                    if text['text'].find("<@U2N9FT1GQ>", 0, len(text['text'])) != -1:
                        print(slack_client.api_call(
                            "chat.postMessage", channel="#mp_testbed", text="Hello again! :tada:",
                            username='cads_north', icon_emoji=':point_up_2:'))


            time.sleep(1)
            #print(slack_client.api_call(
           #     "chat.postMessage", channel="#mp_testbed", text="test",
           #     username='cads_north', icon_emoji=':point_up_2:'))
            #json_obj = json.load(text_in)
            #if json_obj['message']['subtype'] != 'bot_message':
            #    print(text_in['message']['text'])

    else:
        print("Connection Failed, invalid token?")


def send_message(channel_name, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='pythonbot',
        icon_emoji=':robot_face:'
    )

# Different way to read messages. This way is without message polling!
# TODO more information on https://realpython.com/blog/python/getting-started-with-the-slack-api-using-python-and-flask/

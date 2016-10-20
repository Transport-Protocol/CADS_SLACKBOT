#!/bin/python3

import time
import json
from slackclient import SlackClient

# request hostname
BOT_NAME = 'cads_north'

# needs to be hidden!
# TODO follow these instructions: https://www.fullstackpython.com/blog/build-first-slack-bot-python.html to hide the key
# token = os.environ.get('SLACK_TOKEN')
f = open('slackbot_information.json', 'r')
string_bot_information = f.read()

### parse jsonFile
json_bot_information = json.loads(string_bot_information)
slack_client = SlackClient(json_bot_information["token"])

if __name__ == "__main__":
    print(slack_client.api_call("api.test"))
    print(slack_client.api_call("channels.info", channel="1234567890"))
    print(slack_client.api_call(
        "chat.postMessage", channel="#mp_testbed", text="Hello from Python! :tada:",
        username='cads_north', icon_emoji=':point_up_2:'))

    bot_id = 0
    api_call = slack_client.api_call("users.list")
    users = api_call.get('members')
    for user in users:
        if 'name' in user and user.get('name') == json_bot_information['bot_name']:
            bot_id = user.get('id')
            print("Bot ID for '" + user['name'] + "' is " + user.get('id'))

    print("Other Test! \n\n")
    if slack_client.rtm_connect():
        while True:

            text_in = slack_client.rtm_read()
            # print("incoming" + str(text_in) + str(type(text_in)))
            for text in text_in:
                print(text)
                if text['type'] == 'message' and 'subtype' not in dict(text).keys():
                    # print("text: " + str(text))
                    if text['text'].find("<@" + str(bot_id) + ">", 0, len(text['text'])) != -1:
                        if text['text'].find("/status"):
                            print(slack_client.api_call(
                                "chat.postMessage", channel="#mp_testbed", text="This is my status",
                                username='cads_north', icon_emoji=':point_up_2:'))

            time.sleep(1)
            # print(slack_client.api_call(
            #     "chat.postMessage", channel="#mp_testbed", text="test",
            #     username='cads_north', icon_emoji=':point_up_2:'))
            # json_obj = json.load(text_in)
            # if json_obj['message']['subtype'] != 'bot_message':
            #    print(text_in['message']['text'])

    else:
        print("Connection Failed, invalid token?")


def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='pythonbot',
        icon_emoji=':robot_face:'
    )

# Different way to read messages. This way is without message polling!
# TODO more information on https://realpython.com/blog/python/getting-started-with-the-slack-api-using-python-and-flask/

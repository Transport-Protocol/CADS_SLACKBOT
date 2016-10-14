#!/usr/bin/python

import sys
import json
from slackclient import SlackClient


print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

if len(sys.argv) == 2:
    # for easier bot customizing, a json file is supported
    ### read jsonFile
    f = open('slackbot_information.json', 'r')
    string_bot_information = f.read()

    ### parse jsonFile
    json_bot_information = json.loads(string_bot_information)

    # TODO follow these instructions: https://www.fullstackpython.com/blog/build-first-slack-bot-python.html to hide the key
    # token = os.environ.get('SLACK_TOKEN')

    message = sys.argv[1]

    slack_client = SlackClient(json_bot_information["token"])

    slack_client.api_call("chat.postMessage",
                          channel=json_bot_information["default_channel_send"],
                          text=message,
                          username=json_bot_information["bot_name"],
                          icon_emoji=json_bot_information["avatar"])

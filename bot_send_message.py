#!/usr/bin/python

import sys
import json

from slackclient import SlackClient


def transmit_message(json_bot_information, message):
    transmit_message(json_bot_information["token"], json_bot_information["default_channel_send"],
                     json_bot_information["bot_name"], json_bot_information["avatar"], message)


def transmit_message(token, transmit_channel, bot_name, avatar, message):
    slack_client = SlackClient(token)
    slack_client.api_call("chat.postMessage",
                          channel="#" + str(transmit_channel),
                          text=message,
                          username=bot_name,
                          icon_emoji=avatar)


if __name__ == '__main__':
    file_name = sys.argv[0].split("/")[-1]
    path_name = sys.argv[0].split(file_name)[0]

    if len(sys.argv) == 2:
        f = open((path_name + 'slackbot_information.json'), 'r')
        string_bot_information = f.read()

        json_bot_information = json.loads(string_bot_information)

        # TODO follow these instructions: https://www.fullstackpython.com/blog/build-first-slack-bot-python.html to hide the key

        message = sys.argv[1]

        transmit_message(json_bot_information, message)

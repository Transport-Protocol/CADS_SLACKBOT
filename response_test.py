#!/bin/python3
import time
import json
import argparse

from slackclient import SlackClient
import bot_send_message as message_transmitter


parser = argparse.ArgumentParser()
parser.add_argument("--poll_time", type=int, default=1, help="Interval for the message polling")
args = parser.parse_args()

if __name__ == "__main__":
    poll_time = args.poll_time


    # read bot information
    f = open('slackbot_information.json', 'r')
    string_slack_bot_information = f.read()
    f.close()

    # read response information
    f = open('slackbot_response.json', 'r')
    string_slack_bot_response = f.read()
    f.close()

    # parse bot information
    json_slack_bot_information = json.loads(string_slack_bot_information)

    # parse response information
    json_slack_bot_response = json.loads(string_slack_bot_response)
    print(json_slack_bot_response)

    # create SlackClient
    slack_client = SlackClient(json_slack_bot_information["token"])

    # Get Bot ID
    bot_id = 0
    api_call = slack_client.api_call("users.list")
    users = api_call.get('members')
    for user in users:
        if 'name' in user and user.get('name') == json_slack_bot_information['bot_name']:
            bot_id = user.get('id')
            print("Bot ID for '" + user['name'] + "' is " + user.get('id'))

    # Get Channel List
    requested_channels_list = json_slack_bot_information['channels_to_read']
    channel_id_list = []
    channel_name_dict = {}

    api_call = slack_client.api_call("channels.list")
    channels = api_call.get('channels')

    for channel in channels:
        if channel['name'] in requested_channels_list:
            channel_id_list.append(channel['id'])
            channel_name_dict[channel['id']] = channel['name']

    print(channel_id_list)

    print("Other Test! \n\n")

    # Poll messages
    if slack_client.rtm_connect():
        while True:

            text_in = slack_client.rtm_read()
            # print("incoming" + str(text_in) + str(type(text_in)))
            for text in text_in:
                print(text)
                if text['type'] == 'message' and 'subtype' not in dict(text).keys():
                    if 'channel' in text and text['channel'] in channel_id_list:
                        # print("text: " + str(text))
                        if text['text'].find("<@" + str(bot_id) + ">", 0, len(text['text'])) != -1:
                            if text['text'].find("/status"):
                                print("Got here! 3")
                                message_transmitter.transmit_message(json_slack_bot_information["token"],
                                                                     channel_name_dict[text['channel']],
                                                                     json_slack_bot_information["bot_name"],
                                                                     json_slack_bot_information["avatar"],
                                                                     "This is my status")

            time.sleep(poll_time)

    else:
        print("Connection Failed, invalid token?")

# Different way to read messages. This way is without message polling!
# TODO more information on https://realpython.com/blog/python/getting-started-with-the-slack-api-using-python-and-flask/

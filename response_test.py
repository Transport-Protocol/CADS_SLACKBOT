#!/bin/python3
import time
import json
import argparse
import os

from slackclient import SlackClient
import bot_send_message as message_transmitter


parser = argparse.ArgumentParser()
parser.add_argument("--poll_time", type=int, default=1, help="Interval for the message polling")
args = parser.parse_args()


def evaluate_slack_text_and_react(text, responses, json_slack_bot_information):
    to_send = ""
    if text['text'].find("help") != -1:
        to_send = "************* Help *************\n"
        for key in responses.keys():
            to_send += "Key: " + key + " \t,HelpText: " + responses[key]["help"] +"\n"

        message_transmitter.transmit_message(json_slack_bot_information["token"],
                                             channel_name_dict[text['channel']],
                                             json_slack_bot_information["bot_name"],
                                             json_slack_bot_information["avatar"],
                                             to_send)
        return "test"

    # find keywords
    for key in responses.keys():
        if text['text'].find(key) != -1:
            output = os.popen(responses[key]["command"]).read()
            print("************* " + responses[key]["command"] + "*************")
            to_send = "************* " + responses[key]["command"] + " *************\n" + output

            message_transmitter.transmit_message(json_slack_bot_information["token"],
                                                 channel_name_dict[text['channel']],
                                                 json_slack_bot_information["bot_name"],
                                                 json_slack_bot_information["avatar"],
                                                 to_send)


def is_relevant_message(text):
    return text['type'] == 'message' and 'subtype' not in dict(text).keys()


def channel_is_relevant(text, channel_id_list):
    return 'channel' in text and text['channel'] in channel_id_list


def bot_tag_found(text, bot_id):
    return text['text'].find("<@" + str(bot_id) + ">", 0, len(text['text'])) != -1


def create_channel_lists(channels):
    channel_id_list = []
    channel_name_dict = {}

    for channel in channels:
        if channel['name'] in requested_channels_list:
            channel_id_list.append(channel['id'])
            channel_name_dict[channel['id']] = channel['name']

    return channel_id_list, channel_name_dict


def get_bot_id(slack_client, json_slack_bot_information):
    bot_id = -1
    api_call = slack_client.api_call("users.list")
    users = api_call.get('members')
    for user in users:
        if 'name' in user and user.get('name') == json_slack_bot_information['bot_name']:
            bot_id = user.get('id')
            print("Bot ID for '" + user['name'] + "' is " + user.get('id'))

    return bot_id


def read_json_file(file_path):
    f = open(file_path, 'r')
    json_string = f.read()
    f.close()

    return json_string

if __name__ == "__main__":
    poll_time = args.poll_time

    # read bot information
    string_slack_bot_information = read_json_file('slackbot_information.json')

    # read response information
    string_slack_bot_response = read_json_file('slackbot_response.json')

    # parse bot information
    json_slack_bot_information = json.loads(string_slack_bot_information)

    # parse response information
    responses = json.loads(string_slack_bot_response)
    #print(responses)

    # create SlackClient
    slack_client = SlackClient(json_slack_bot_information["token"])

    # Get Bot ID
    bot_id = get_bot_id(slack_client, json_slack_bot_information)

    requested_channels_list = json_slack_bot_information['channels_to_read']
    channel_id_list = []
    channel_name_dict = {}

    api_call = slack_client.api_call("channels.list")
    channels = api_call.get('channels')

    channel_id_list, channel_name_dict = create_channel_lists(channels)

    # Poll messages
    if slack_client.rtm_connect():
        while True:
            # read all inputs
            text_in = slack_client.rtm_read()

            for text in text_in:
                #print(text)

                if is_relevant_message(text):
                    if channel_is_relevant(text, channel_id_list):
                        # is message for bot
                        if bot_tag_found(text, bot_id):
                            #print(text['text'])
                            evaluate_slack_text_and_react(text, responses, json_slack_bot_information)

            time.sleep(poll_time)

    else:
        print("Connection Failed, invalid token?")

# Different way to read messages. This way is without message polling!
# TODO more information on https://realpython.com/blog/python/getting-started-with-the-slack-api-using-python-and-flask/

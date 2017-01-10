from slackclient import SlackClient
import json
import sys

import slackbot_send_message as message_transmitter

file_name = sys.argv[0].split("/")[-1]
path_name = sys.argv[0].split(file_name)[0]
slackbot_info_file = path_name + 'slackbot_information.json'

f = open(slackbot_info_file, 'r')
string_bot_information = f.read()
f.close()

### parse jsonFile
json_slack_bot_information = json.loads(string_bot_information)

slack_client = SlackClient(json_slack_bot_information["token"])
response = slack_client.api_call("api.test")

if response["ok"]:
    bot_id = 0
    api_call = slack_client.api_call("users.list")
    users = api_call.get('members')
    found_user = False

    for user in users:
        if 'name' in user and user.get('name') == json_slack_bot_information['bot_name']:
            bot_id = user.get('id')
            # print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
            # get bot id and write id in config.
            json_slack_bot_information["bot_id"] = user.get('id')
            f = open(slackbot_info_file, 'w')
            f.write(json.dumps(json_slack_bot_information))
            found_user = True

    if not found_user:
        print("Username not found: " + str(json_slack_bot_information['bot_name']))

    api_call = slack_client.api_call("channels.list")
    found_send = False
    found_read = 0
    channels_to_read = json_slack_bot_information["channels_to_read"]
    channel_to_send = json_slack_bot_information["default_channel_send"]

    for channel in api_call["channels"]:
        channel_name = channel["name"]

        if channel_name == channel_to_send:
            found_send = True

        for read_channel in channels_to_read:
            if read_channel == channel_name:
                found_read += 1

    if not found_send:
        print("Default send channel is not correct: " + str(channel_to_send))

    if len(channels_to_read) != found_read:
        print("Not all channels to read were found" + str(channels_to_read))

    if found_user and found_send and len(channels_to_read) == found_read:
        message_transmitter.transmit_message(json_slack_bot_information["token"],
                                             json_slack_bot_information["default_channel_send"],
                                             json_slack_bot_information["bot_name"],
                                             json_slack_bot_information["avatar"],
                                             "Test successful passed!")

else:
    print("Token is not correct!")

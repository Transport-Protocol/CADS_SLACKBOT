from slackclient import SlackClient
import json

f = open('slackbot_information.json', 'r')
string_bot_information = f.read()
f.close()

### parse jsonFile
json_bot_information = json.loads(string_bot_information)

slack_client = SlackClient(json_bot_information["token"])
response = slack_client.api_call("api.test")
print(response)
print(response["ok"])

bot_id = 0
api_call = slack_client.api_call("users.list")
users = api_call.get('members')
for user in users:
    if 'name' in user and user.get('name') == json_bot_information['bot_name']:
        bot_id = user.get('id')
        print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
        # get bot id and fil
        json_bot_information["bot_id"] = user.get('id')
        f = open('slackbot_information.json', 'w')
        f.write(json.dumps(json_bot_information))


slack_client.api_call("chat.postMessage",
                      channel=json_bot_information["default_channel_send"],
                      text="test message!",
                      username=json_bot_information["bot_name"],
                      icon_emoji=json_bot_information["avatar"])


# CADS_SLACKBOT
This is CADS_SLACKBOT!

## First Steps
First goal is to provide basic services, such as sending messages to a Slack channel.  
Be sure that your bot is a member of the specified channel.

## How to Configure
Use the slackbot_information_example.json to setup your own slackbot_information.json file.  
The bot is using the information specified in the json file to get the wanted behaviour.

## Attention
Make sure that you **not upload** your token! 

## Examples

Sending a message with the specified SlackBot.
```
python3 bot_send_message.py "hello from python script"
```
This posts a hello to the specified channel.

## Install Guide

+ install python3
+ install pip
+ install SlackClient, with the following command:
````
pip3 install SlackClient
````
+ Clone the repository
+ Fill your information in a file named: "slackbot_information.json" inside of the repository. The field bot_id will be set later.
+ Run the configuration test.
````
python3 test_your_bot_configuration.py
````
+ If the configuration was correct, the bot writes a message in the configured channel.
+ Now you can use the bot. Have a look at the example above.


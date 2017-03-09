import os
import time
from slackclient import SlackClient
import question_handler

def get_bot_id(slack_client, bot_name):
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == bot_name:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                return user.get('id')
    else:
        print("could not find bot user with the name " + bot_name)

# instantiate Slack & Twilio clients
with open("api.token", "r") as token:
    slack_client = SlackClient(token.read().strip())
    BOT_ID = get_bot_id(slack_client, "advisorbot")
    AT_BOT = "<@" + BOT_ID + ">"


def handle_command(command, channel):
    response = question_handler.handle(command)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("AdvisorBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

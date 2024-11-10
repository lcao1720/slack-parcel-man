import os
import requests
from datetime import datetime, timedelta
from slack_sdk import WebClient
from collections import defaultdict
from enum import StrEnum
import re


USER_MAPPING = {
    "U07U8GZNN1M": "Lina",
    "U07U90DGGFR": "LinaBot",
}

CHANNEL_MAPPING = {
    "brainstorming": "C07UGEVAXRC",
    "social": "C07UL7TFHJR",
    "all-en-zone": "C07UP0UCPEF",
    "help-weekly-summary": "C07UP3S5WLA",
    "help-daily-idea": "C07VBT7UHDE",
}

class MESSAGE_SUBTYPE(StrEnum):
    CHANNEL_CONVERT_TO_PUBLIC = "channel_convert_to_public"
    CHANNEL_JOIN = "channel_join"


# Slack client setup
slack_token = os.environ["SLACK_TOKEN"]
client = WebClient(token=slack_token)
[[record['id'], record['name']] for record in client.conversations_list().data['channels']]
# [['C07UGEVAXRC', 'brainstorming'], ['C07UL7TFHJR', 'social'], ['C07UP0UCPEF', 'all-en-zone'], ['C07UP3S5WLA', 'help-weekly-summary'], ['C07VBT7UHDE', 'help-daily-idea']]
# read all messages from the  channel

# response = client.conversations_history(channel="C07VBT7UHDE", limit=100)

# get channel id
# client.conversations_list()




# Replacement function
def replace_match(match):
    user_id = match.group(1) 
    return f"<@{USER_MAPPING.get(user_id, user_id)}>" 

def replace_userid_in_text(text):
    # regex pattern to match msg like <@U07U90DGGFR>
    pattern = r"<@([\w]+)>"
    return re.sub(pattern, replace_match, text)


# Function to fetch messages from Slack channel 1
def fetch_weekly_notes(channel_name):
    channel_id = CHANNEL_MAPPING[channel_name]
    one_week_ago = (datetime.now() - timedelta(days=8)).strftime("%s")
    response = client.conversations_history(channel=channel_id, oldest=one_week_ago)

    if response["ok"]:
        messages = response["messages"]
        user_messages = defaultdict(list)
        for msg in messages:
            if "text" in msg and ("subtype" not in msg or msg["subtype"] not in [cat.value for cat in MESSAGE_SUBTYPE]):
                user_name = USER_MAPPING.get(msg["user"], "User X")
                msg_text =  msg["text"]
                # add message after modify the @user pattern
                user_messages[user_name].append(replace_userid_in_text(msg_text))
    return user_messages

channel_id_1 = "help-daily-idea"
weekly_notes = fetch_weekly_notes(channel_id_1)


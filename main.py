#!/usr/bin/env python3

from datetime import datetime
import json
import hashlib
import sys
from unidecode import unidecode
from config import es
from config import INDEX_PREFIX
from config import MAPPING

MESSAGES = {}

def process_message(message, participants, title):
    global MESSAGES

    if not "content" in message:
        return

    try:
        message["content"] = message["content"].encode('latin1').decode('utf8')
    except:
        print("Error processing message {str(message)}")
        return

    if 'reactions' in message:
        for reaction in message['reactions']:
            for key, val in reaction.items():
                reaction[key] = val.encode("latin1").decode("utf-8")

    message["participants"] = participants
    message["title"] = title
    message["sender_name"] = message["sender_name"].encode('latin1').decode('utf8')

    try:
        id_to_hash = (message["sender_name"] + str(message["timestamp_ms"]) + message.get("content", "media")).encode("utf-8")
    except KeyError as e:
        print(message)
        raise KeyError(f"failed to ID + {e}")

    id_ = hashlib.sha256(id_to_hash).hexdigest()
    MESSAGES[id_] = json.dumps(message)

def process_json_file(path):
    with open(path, "r") as f:
        content = json.loads(f.read())

    try:
        participants = [participant["name"].encode('latin1').decode('utf8') for participant in content["participants"]]
        print(" - ".join(participants))
    except KeyError:
        print(f"{path} has no members")
        if content["is_still_participant"]:
            raise KeyError("Participants empty")
    except UnicodeEncodeError as e:
        print(f"Unicode error : {e}")
        print(content["participants"])
        raise e
    print("Processing " + content.get("title", participants).encode("latin1").decode("utf-8") + f" / {len(content['messages'])} messages")
    for message in content["messages"]:
        process_message(message, participants, content["title"].encode("latin1").decode("utf-8"))

def create_index():
    try:
        #es.indices.delete(index=INDEX_PREFIX + "-conv")
        pass
    except:
        pass
    try:
        r = es.indices.create(index=INDEX_PREFIX + '-conv', body=MAPPING, )
    except:
        pass

def bulk_send_messages():
    global MESSAGES
    def send(body):
        if body == "":
            return
        r = es.bulk(body=body)
        #print(r)

    i = 0
    body = ""
    for key, val in MESSAGES.items():
        body += '{"index":{"_index":"' + INDEX_PREFIX + '-conv","_id":"' + key + '"}}\n'
        body += val + "\n"
        i += 1
        if i == 1000:
            i = 0
            send(body)
            body = ""
    send(body)

create_index()
for path in sys.argv[1:]:
    process_json_file(path)
    bulk_send_messages()

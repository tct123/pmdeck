
import json

settings = {}


def read_settings():
    with open('settings.json') as f:
        settings = json.load(f)
    return

def write_settings():
    f = open("settings.json","w")
    f.write(json.dump(settings))
    f.close()
    return

def get_actions_for_folder(deck_id, folder_id):
    return settings[deck_id]["Folders"][folder_id]

def get_action_settings(deck_id, action_id):
    return settings[deck_id]["Actions"][action_id]



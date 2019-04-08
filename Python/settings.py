
import json

class Settings:

    def __init__(self):
        self.settings = {}

    def read_settings(self):
        with open('settings.json') as f:
            self.settings = json.load(f)
        return

    def write_settings(self):
        f = open("settings.json","w")
        f.write(json.dump(self.settings))
        f.close()
        return

    def get_actions_for_folder(self, deck_id, folder_id):
        return self.settings[deck_id]["Folders"][folder_id]

    def get_action_settings(self, deck_id, action_id):
        return self.settings[deck_id]["Actions"][action_id]

    def set_action_for_folder(self, deck_id, folder_id, key_index, action_id):
        self.settings[deck_id]["Folders"][folder_id][key_index]["action_id"] = action_id;
        self.write_settings()
        return true


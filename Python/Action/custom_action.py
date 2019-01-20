
from Action.AHK.autohotkey_action import AutoHotkeyAction
import os


def create_custom_action(deck, action_id):

    # check if its a Autohotkey or Python Action
    custom_action_folder_path = "Action/CustomActions/"
    action_folder_path = custom_action_folder_path + action_id + "/"
    if os.path.isfile(action_folder_path + "Action.ahk"):
        return AutoHotkeyAction(deck, action_id)
    else:
        return

    return

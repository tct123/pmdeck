
from Action.AHK.autohotkey_action import AutoHotkeyAction
from Action.Python3.python3_action import Python3Action
import os


def create_custom_action(deck, action_id, action_config):

    # check if its a Autohotkey or Python Action
    custom_action_folder_path = "Action/CustomActions/"
    action_folder_path = custom_action_folder_path + action_id + "/"
    if os.path.isfile(action_folder_path + "AutoHotkeyAction.ahk"):
        return AutoHotkeyAction(deck, action_id)
    elif os.path.isfile(action_folder_path + "Python3Action.py"):
        return Python3Action(deck, action_id)

    return

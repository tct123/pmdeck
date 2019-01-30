
from Action.action import Action
from Action.custom_action import create_custom_action


class Folder:

    def __init__(self, settings, deck, folder_id):
        
        # List of Actions
        # self.actions = [Action(deck)] * 15
        self.deck = deck
        self.id = folder_id
        # read settings, get button id's with that deck and folder id
        self.actions = []
        acts = settings.get_actions_for_folder(deck.id, folder_id)
        for a in acts:
            config = settings.get_action_settings(deck.id, a)
            self.actions.append(create_custom_action(deck, a, config))

        return

    def set_action(self, space_index: int, action):
        if not 14 >= space_index >= 0:
            print("Space index error: " + space_index)
            return
        # TODO save it in settings.json

        settings.set_action_for_folder(self.deck.id, self.id, space_index, action.id)
        self.actions[space_index] = action

    def open(self):
        if hasattr(self.deck, "current_folder"):
            self.deck.current_folder.close()

        # for each action in actions, draw action
        for i in range(0, len(self.actions)):
            if self.actions[i]:
                self.actions[i]._set_visible(i)
        # hook layout as current folder
        self.deck.current_folder = self
        return

    def close(self):
        for i in range(0, len(self.actions)):
            if self.actions[i]:
                self.actions[i]._set_invisible(i)
        for i in range(0, len(self.actions)):
            if self.actions[i]:
                self.actions[i].on_exit()
        return

    def button_pressed(self, space_index:int):
        if self.actions[int(space_index)]:
            self.actions[int(space_index)]._pressed()

    def button_released(self, space_index:int):
        if self.actions[int(space_index)]:
            self.actions[int(space_index)]._released()



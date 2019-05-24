import curses
from random import randrange, choice
from collections import defaultdict
import kivy
kivy.require('1.0.6') # replace with your current kivy version !
from kivy.app import App
from kivy.uix.label import Label

class MyApp(App):

    def __init__(self):
        super().__init__()
        self.actions = ['Up', 'Down', 'Left', 'Right', 'Restart', 'Exit']
        self.letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
        self.actions_dict = dict(zip(self.letter_codes, self.actions * 2))
        self.state_actions = {
            'Init': self.init,
            'Win': lambda : self.not_game('Win'),
            'Gameover': lambda: self.not_game('Gameover'),
            'Game': self.game
        }

    def init(self):
        return 'Game'

    def not_game(self, state):
        responses = defaultdict(lambda: state)
        responses['Restart'], responses['Exit'] = 'Init', 'Exit'
        #return responses[action]

    def game(self, action):
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'

    def build(self):
        return Label(text='Hello world')


if __name__ == '__main__':
    MyApp().run()





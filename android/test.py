from kivy.app import App
from kivy.uix.button import Button
import gettext

class MainWindow(App):
    def build(self):
        _ = gettext.gettext
        self.title = _('Duplicate File Removal')
        self.
        gettext.bindtextdomain('myapplication', '/path/to/my/language/directory')
        gettext.textdomain('myapplication')

        test = _('This is a translatable string.')
        return Button(text=test)

MainWindow().run()
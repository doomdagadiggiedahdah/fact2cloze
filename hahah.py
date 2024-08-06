from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

class MyTextInput(TextInput):

    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'enter' and 'ctrl' in modifiers:
            self.on_submit()
            return True
        else:
            return super(MyTextInput, self)._keyboard_on_key_down(window, keycode, text, modifiers)

    def on_submit(self):
        print(f"Ctrl + Enter was pressed, current text: {self.text}")

class MyApp(App):

    def build(self):
        return MyTextInput(hint_text='Type here...', multiline=False)

if __name__ == '__main__':
    MyApp().run()

import grab_text
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window  # To catch keyboard events
import connect
import openai
openai.api_key_path="/home/mat/Documents/ProgramExperiments/openAIapiKey"


prePrompt1 = """
I want you to create a cloze deletion card for an Anki Deck out of a string of text I pass. A cloze deletion is a single or group of words enclosed like follows.
{{c1::interesting fact}}. The goal of the clozes is to withhold the important pieces of info so that I'm tested on recalling them.
Example 1:
String: A large language model (LLM) is a neural network with many parameters
Result: A {{c1::large language model (LLM)}} is a {{c2::neural network}} with {{c3::many parameters}}

Instructions:
Keep the amount of words inside the clozes to no more than 4 words. 
Only make one cloze for approx every five words, but only make one for important concepts of the sentence.

Input:
"""


def textFromAI(text):
    res = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": prePrompt1},
            {"role": "user", "content": text}
        ])
    story = res["choices"][0]["message"]["content"]
    return str(story)


class TextApp(App):

    def build(self):

        # Main layout
        self.layout = BoxLayout(orientation='vertical')
        
        # Keyboard binding
        Window.bind(on_key_down=self.on_key_down)
        
        # Label
        self.label = Label(text=grab_text.URL, size_hint_y=None, height=30)
        self.layout.add_widget(self.label)
        
        # Text input (multi-line)
        self.text_input = TextInput(hint_text="Type here", multiline=True, size_hint_y=1)
        self.text_input.text = grab_text.og_article_text
        self.layout.add_widget(self.text_input)
        self.text_input.focus = True

        # Submit button
        self.submit_button = Button(text="Submit", size_hint_y=None, height=50)
        self.submit_button.bind(on_press=self.on_submit)
        self.layout.add_widget(self.submit_button)
        
        return self.layout

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 13 and 'ctrl' in modifiers:  # 13 is the keycode for Enter
            self.on_submit()
            print("it workd")
        else:
            print("didn't work")


    def on_submit(self, instance):
        user_edited_text = self.text_input.text.strip()


        if user_edited_text:
            title = "You entered"
            cloze_return = textFromAI(user_edited_text)

            note = {
                "deckName": "Big Daddy::fact2cloze",
                "modelName": "Cloze",
                "fields": {"Text": cloze_return, 
                            "Extra": grab_text.og_article_text,
                            "Source": grab_text.URL
                            },
                "tags": ["fact2cloze"]
            }
            connect.invoke('addNote', note=note)



        else:
            title = "Cancelled"
            user_edited_text = "Text editing cancelled."
        

        # Idea: have a popup that says "good!" and then drops away after a second.


        # Popup to show message
        # popup = Popup(title=title,
        #               content=Label(text=user_edited_text),
        #               size_hint=(None, None),
        #               size=(400, 400),
        #               auto_dismiss=True)
        # popup.bind(on_dismiss=self.quit_app)
        # popup.open()

    def quit_app(self, *args):
        App.get_running_app().stop()

if __name__ == '__main__':
    TextApp().run()

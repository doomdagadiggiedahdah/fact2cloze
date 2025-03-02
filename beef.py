import os
import sys
import time
from openai import OpenAI
import connect
import pyperclip
import tkinter    as tk
import pyautogui  as pya
import subprocess as s
from dotenv  import load_dotenv
from tkinter import messagebox

prePrompt1 = """
I want you to create a cloze deletion card for an Anki Deck out of a string of text I pass. A cloze deletion is a single or group of words enclosed like follows.
{{c1::interesting fact}}. The goal of the clozes is to withhold the important pieces of info so that I'm tested on recalling them.
Example 1:
String: A large language model (LLM) is a neural network with many parameters
Result: A {{c1::large language model (LLM)}} is a {{c2::neural network}} with {{c3::many parameters}}

Instructions:
Keep the amount of words inside the clozes to no more than 4 words. 
Only make one cloze for approx every five words, but only make one for important concepts of the sentence.
Reply with only the cloze_card content, only what will be shown on the card.

Input:
"""

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    # Handle missing key - either use a default or raise an error
    print("API key not found in environment", file=sys.stderr)
    sys.exit(1)

client = OpenAI(api_key=api_key)

def copy_text():
    time.sleep(.2)
    pya.hotkey('ctrl', 'c')
    return pyperclip.paste().replace("\n", " ")

def grab_link():
    pya.hotkey('i') # added for vimium
    pya.hotkey('ctrl', 'l')
    pya.hotkey('ctrl', 'c')
    pya.hotkey('F6')
    pya.hotkey('Esc')
    return pyperclip.paste().strip()

def textFromAI(text):
    res = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role": "system", "content": "you are a world class learning coach, taking given facts and creating flash cards for your student."},
            {"role": "assistant", "content": prePrompt1},
            {"role": "user", "content": text}
        ])
    story = res.choices[0].message.content
    return str(story)


# sub this out for appropriate submit functions
def on_submit():
    cloze_input  = text_box.get("1.0", tk.END).strip()
    cloze_return = textFromAI(cloze_input)

    #Anki note contents
    #articleLink in the Source
    anki_deck_name = os.environ["ANKI_DECK_NAME"]

    note = {
        "deckName": anki_deck_name ,
        "modelName": "Cloze",
        "fields": {"Text": cloze_return , 
                   #"Extra": "<br><br>OG text: " + og_article_text,
                   "Source": og_article_text + "\n\n\n" + URL
                   },
        "tags": ["fact2cloze"]
    }

    if not cloze_input:
        print("no prompt")
        s.call(['notify-send', '-t', '2000', 'fact2cloze', 'empty prompt!'])
    else:
        print("got a prompt...")
        try:
            connect.invoke('addNote', note=note)
        except Exception:
            print(cloze_return + "\n\n")
            print("did this have a cloze in it?")
        s.call(['notify-send', '-t', '2000', 'fact2cloze', cloze_return])

        root.destroy()

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"


# calling these quickly before craziness starts
og_article_text = copy_text()
URL = grab_link()


### Tkinter code
# main window
root = tk.Tk()
root.title("Knowledge Hack")

# Label with URL 
label = tk.Label(root, text=URL)
label.pack()

# Text box
text_box = tk.Text(root, wrap='word', width=40, height=10)
text_box.pack()

# paste buffer into text box 
text_box.insert(tk.END, og_article_text)
text_box.focus_set() #puts cursor in the text box

# Create a Button to submit the text
text_box.bind('<Tab>', focus_next_widget)
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.bind('<Return>', lambda event=None: on_submit())
submit_button.pack()


submit_button.bind('<Return>', lambda event=None: on_submit())
root.mainloop()

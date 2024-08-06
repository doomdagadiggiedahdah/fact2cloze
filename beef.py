import time
import connect
import pyperclip
import openai
import pyautogui as pya
import subprocess as s
import tkinter as tk
from tkinter import messagebox

openai.api_key_path="/home/mat/Documents/ProgramExperiments/openAIapiKey"

# calling these quickly before craziness starts
og_article_text = copy_text()
URL = grab_link()


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
    res = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prePrompt1},
            {"role": "user", "content": text}
        ])
    story = res["choices"][0]["message"]["content"]
    return str(story)


# sub this out for appropriate submit functions
def on_submit():
    entered_text = text_box.get("1.0", tk.END).strip()
    clozeReturn = textFromAI(entered_text)

    #Anki note contents
    #articleLink in the Source
    note = {
        "deckName": "Big Daddy::fact2cloze",
        "modelName": "Cloze",
        "fields": {"Text": clozeReturn, 
                   #"Extra": "<br><br>OG text: " + og_article_text,
                   "Source": og_article_text + "\n\n\n" + URL
                   },
        "tags": ["fact2cloze"]
    }

    if not entered_text:
        print("no prompt")
        s.call(['notify-send', '-t', '2000', 'fact2cloze', 'empty prompt!'])
    else:
        print("got a prompt...")
        try:
            connect.invoke('addNote', note=note)
        except Exception:
            print(clozeReturn + "\n\n")
            print("did this have a cloze in it?")
        s.call(['notify-send', '-t', '2000', 'fact2cloze', clozeReturn])

        root.destroy()

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"



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
submit_button.pack()

# Bind the Enter key to the Submit button
submit_button.bind('<Return>', lambda event=None: on_submit())

root.mainloop()

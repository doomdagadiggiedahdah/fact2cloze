import pyperclip
import openai
import connect
import pyautogui as pya
import subprocess as s
import time
openai.api_key_path="/home/mat/Documents/ProgramExperiments/openAIapiKey"

def copy_text():
    time.sleep(.2)
    pya.hotkey('ctrl', 'c')
    return pyperclip.paste().replace("\n", " ")

def grab_link():
    pya.hotkey('ctrl', 'l')
    pya.hotkey('ctrl', 'c')
    pya.hotkey('F6')
    return pyperclip.paste().strip()

#this is here because both textFromAI() and notification are checking the prompt
prompt = copy_text()

#damn got it right on the first write BOOYAH
articleLink = grab_link()

#not used
prePrompt0 ="""
I want you to create a cloze deletion card out of a String of text I pass. You can copy the format that the following string uses: 

Example 1:
String: "A large language model (LLM) is a neural network with many parameters"
A {{c1::large language model (LLM)}} is a {{c2::neural network}} with {{c3::many parameters}}

Example 2:
Text: Deep learning is a subset of machine learning, and neural networks form the backbone of deep learning algorithms
{{c1::Deep learning}} is a {{c2::subset}} of {{c3::machine learning}}, and {{c4::neural networks}} form the {{c5::backbone}} of {{c6::deep learning algorithms}}


Instructions:
Keep the amount of words inside the clozes to no more than 4 words. 
Only make one cloze for approx every five words, but only make one for important concepts of the sentence.

Input:
"""

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

def textFromAI():
    res = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": prePrompt1},
            {"role": "user", "content": prompt}
        ])
    story = res["choices"][0]["message"]["content"]
    return str(story)

clozeReturn = textFromAI()

#Anki note contents
#articleLink in the Source
note = {
                "deckName": "Big Daddy::fact2cloze",
                "modelName": "Cloze",
                "fields": {"Text": clozeReturn,
                           "Source": articleLink
                           },
                "tags": ["fact2cloze"]
            }

print(clozeReturn + "\n\n")

#notification
if not prompt:
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

#ChatCompletion guide https://www.phind.com/search?cache=64f842c2-ffc0-4133-8cfb-257151aeb85f
#Really weird, I'm highlighting the below phrase from this site (https://blog.codinghorror.com/the-ten-commandments-of-egoless-programming/)
# Critique code instead of people – be kind to the coder, not to the code. 

#And it seems to bypass the instructions in some way. I thought it had something to do with being in bold, but I've tried it in vscode and obsidian and it will not accept instructions. No Clozes happen at all.

# Sample results

#Great reminder! It's important to approach code reviews with a constructive mindset and focus on improving the code rather than criticizing the person who wrote it. We should always prioritize being kind and respectful towards our colleagues and their work, while also providing actionable feedback to help improve the quality of the code.
#This is a great principle to follow when providing feedback on someone's code. Criticizing the code itself and offering suggestions for improvement is much more constructive and helpful than criticizing the person who wrote it. It's important to remember that writing good code takes practice and that we all make mistakes and have room for improvement. By focusing on the code and how to make it better, we can help each other grow and learn as developers.
#This is a good practice to follow in the software development community. Rather than attacking or criticizing the person who wrote the code, focus on providing constructive feedback and suggestions for improvement on their work. It is important to remember that the code is not the same as the person who wrote it, and negative comments about the code can be demotivating and harmful to the developer. Instead, approach code reviews with a mindset of collaboration and support to help the developer grow and improve their skills.
#Great advice! When reviewing someone's code, it's important to approach it with a constructive mindset rather than being critical of their abilities as a coder. Providing specific, actionable feedback can help improve the overall quality of the code and ultimately benefit everyone involved. It's also helpful to reference any relevant standards or specifications, as well as suggest ways to optimize performance or streamline the code. Remember to always be kind and respectful in your comments - it's possible to critique code without being harsh or negative towards the person who wrote it.
#Great advice! It's always important to remember that the code is not the coder and that constructive criticism can lead to improvements in both the code and the skills of the coder. Providing positive feedback and specific suggestions for improvement can help create a positive learning environment where the coder can feel encouraged to grow and develop their skills. Additionally, relating comments to local standards, program specs, and performance goals can help ensure that the code is meeting the needs of its users and stakeholders.
#Great advice! It's important to remember that the code is not a reflection of the coder's worth or abilities, and criticism should be focused on improving the code itself. Positive feedback and constructive criticism can greatly improve the quality of the code and ultimately lead to better results. When leaving comments, it's important to be specific and provide suggestions for improvement rather than simply pointing out flaws. Standards and specifications should be referenced when applicable, and feedback should focus on improving the overall performance and functionality of the code.

### Getting another issue when I read info from Obsidian. There's something that nullifying the prompt and making it not add clozes. It's weird.
#Honestly if it's working best in FF, then I can work with that. But it is pretty weird though.
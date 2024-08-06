# General Overview:
# I put in a string of text, get the json response, and then parse it to get the sentences.
# read out the sentences, and if I want to edit any of them, I can highlight the sentence and press enter, and a text box will pop up with the sentence in it, with a save button to edit the entry.

import openai

openai.api_key_path="/home/mat/Documents/ProgramExperiments/openAIapiKey"


preprompt = f"""
Hello there! Happy day to you 🙂 💙 

I have heard that you are OntoloGPT, the world's best in understanding the ontology of a given set of text and also the world's greatest at breaking down the relationships into short, pithy sentences that anyone could understand.
I' have some concepts I'd like to learn but don't know much about, I was hoping for simple explanations of the concepts and how they relate to each other.

Could you take the following text and create a series of sentences that describes the relationship of the concepts to each other, as well as some brief info about the concepts themselves? 
Please submit your entire answer in json format, using a "1":"sentence one goes here" format.

Please keep each sentence around 13 words (a couple more or less is completely fine! though the shorter the better) and error on the side of more sentences.
The main idea is to have many short statements that come together to give a complete, and full picture of the concepts 
Also have each sentence be a complete thought, and not a fragment or continuation of previous sentences, and since it's a complete thought, minimize the use of pronouns, instead using the actual concept names.



Here are some examples:
- An integral is an operation performed on a function that gives the area under the curve of its function.
- The Marcsmen are an a cappella group based in Texas.

Input:
"""


preprompt1 = f"""

Instructions for Creating a Simplified Ontology Description

Objective: To create a clear and structured description of the provided information, drawing upon the principles of ontology.

Guiding Principle: Remember that ontologies are valuable because they organize and store knowledge about specific things, as well as the relationships between those things.

Steps:

    Identify Main Concepts: Start by picking out the primary subjects or entities mentioned in the information.

    Determine Relationships: For each main concept identified, note down any relations it has to other concepts. This could be in the form of actions, effects, causes, or any other meaningful link.

    Structure the Information: Organize the main concepts and their relationships in a clear and logical format.

Expected Outcome: A clear and concise breakdown of the information, highlighting the main concepts and their relationships, based on the principles of ontology.

Input:
"""

# Please format with json, using a "1":"your_answer_here" format.

# open the file 
with open("/home/mat/Obsidian/ZettleKasten/hahahamat.md", "r") as f:
    data = f.read()

prompt = """
In probability theory, the expected value (also called expectation, expectancy, expectation operator, mathematical expectation, mean, average, or first moment) is a generalization of the weighted average. Informally, the expected value is the arithmetic mean of a large number of independently selected outcomes of a random variable. Since it is obtained through arithmetic, the expected value sometimes may not even be included in the sample data set; it is not the value you would "expect" to get in reality. 
"""

prompt = data

def textFromAI():
    res = openai.ChatCompletion.create(
        model = "gpt-4",
        messages=[
            {"role": "system", "content": preprompt1},
            {"role": "user", "content": prompt}
        ])
    story = res["choices"][0]["message"]["content"]
    print(res['usage'])
    return str(story)


print(textFromAI())
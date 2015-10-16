main.py
This is the main module of our project. To run our tests, use the command "python main.py <test data>" where test data is a text file with sentences you want to test. The wikipedia test for example would be "python main.py simple_test_1.py"

anaphora.py
This module controls all of the anaphora resolution. It parses text and finds references to named entities and replaces the anaphors.

analysis.py
This module contains the rules that define our fact-structures. Feel free to add your own if you want to test more complex grammars.

model.py
This module contains the definitions of each fact-structure (not the grammar that matches it). It explains how to handle each case.

text2int.py
Text2int is a snippet from Stackoverflow that translates text into numbers.

import os
import ujson
import time
#import tkinter as ttk
from tkinter import scrolledtext
import tkinter as tk
from tkinter import ttk  # Import ttk from tkinter
import threading
from datadump import alpha_sort, push_to_disk
from bs4 import BeautifulSoup
from helper_funcs import retrieve_word, get_url, find_the_best_docs
# doc:  https://www.crummy.com/software/BeautifulSoup/bs4/doc/

from spellchecker import SpellChecker 
# pip install pyspellchecker

import wordninja
import re
import nltk
from nltk.stem import PorterStemmer

dark_background = "#2D2D2D"
light_text = "#FFFFFF"
button_color = "#5F5F5F"
entry_bg = "#3C3C3C"
entry_fg = "white"

# doc: https://www.nltk.org/, and class
# from spellchecker import SpellChecker

#this is the function to process the html files 
#as of right now it grabs the important text BUT DOESNT DO ANYTHING WITH it
#for now its just returning all the text not including the important ones)
#later we might use the important ones for something


# pre-compile for efficiency
clean_query = re.compile(r"[^\w\s'-]")

def validate_query(query):
    # setup for spellchecker
    spell = SpellChecker()
    # clean the query to remove unwanted characters
    cleaned_query = clean_query.sub('', query)

    # if the query is a single word or seems to be a concatenated string
    if len(cleaned_query.split()) <= 1:
        # query is all caps so we want to keep it the same -> "COMPUTER"
        if cleaned_query.isupper(): 
            return [cleaned_query.lower()]
        # check if the word is unknown (misspelled or concatenated) -> "computre"
        elif spell.unknown([cleaned_query]):
            # Correct the query if it's misspelled "computre" -> "computer"
            corrected_query = spell.correction(cleaned_query)
            # if correction is different from the original, then misspell has been resolved
            if corrected_query and corrected_query.lower() != cleaned_query.lower():
                return [corrected_query.lower()]
            # if query is a concatenation of words -> "computerscience"
            else:
                # split the words by meaning using wordninja 
                split_words = wordninja.split(cleaned_query)
                refined_tokens = []

                for token in split_words:
                    # Correct each part if it seems misspelled
                    if  spell.unknown([token]):
                        corrected_token = spell.correction(token)
                        refined_tokens.append(corrected_token)
                    else:
                        refined_tokens.append(token.lower())
        else:
            # if query does not need any modification return it as is -> "computer"
            return [cleaned_query.lower()]
    else:
        # tokenize each query if its more than two words
        query_tokens = nltk.word_tokenize(cleaned_query)
        refined_tokens = []

        for token in query_tokens:
            # If the token starts with a capital letter, treat it as a proper noun
            if token[0].isupper():
                refined_tokens.append(token.lower())
            else:
                # Correct misspelled words
                if spell.unknown([token]):
                    corrected_token = spell.correction(token)
                    # Check if corrected_token is None and use the original token as a fallback
                    corrected_token = corrected_token if corrected_token is not None else token
                    refined_tokens.append(corrected_token.lower())
                else:
                    refined_tokens.append(token.lower())
                    
    # limit the number of tokens to 4 for faster search
    if len(refined_tokens) > 4:

        # hold the highest frequency score for each token
        token_scores = {}

        for token in refined_tokens:
            # get the highest score for each token
            token_data = retrieve_word(token)
            if token_data:
                highest_score = max(token_data.items(), key=lambda x: x[1][0])[1][0]
                token_scores[token] = highest_score
            else:
            # assign a default score if the token is not found
                token_scores[token] = 0

        # Sort tokens by their highest score in descending order
        sorted_tokens = sorted(refined_tokens, key=lambda token: token_scores.get(token, 0), reverse=True)

        # Limit to the top 4 tokens
        return sorted_tokens[:4]
    else:
        return refined_tokens


#wrapper class for the GUI
def run_search():
    user_query = entry.get()
    valid_token = validate_query(user_query)
    empty_dict = {}
    stemmer = PorterStemmer()
    for token in valid_token:
        stem_token = stemmer.stem(token)
        dicts_word = retrieve_word(stem_token)
        
        if dicts_word is not None:
            empty_dict[stem_token] = dicts_word

    web_ranks = find_the_best_docs(empty_dict)

    result_area.delete('1.0', tk.END)
    result_area.insert(tk.END, "Top Results For Query : \n")
    result_area.insert(tk.END, "---------------------- \n\n")
    for number, item in enumerate(web_ranks):
        result_area.insert(tk.END, number + 1)
        result_area.insert(tk.END, ") ")
        result_area.insert(tk.END, f"{get_url(item)}\n\n")



if __name__ == "__main__":
    # Tkinter GUI setup
    root = tk.Tk()
    root.title("Search Application")

    #init the style
    style = ttk.Style()
    style.theme_use('clam')  #use clam

    # color scheme
    style.configure('TFrame', background='#333333')
    style.configure('TLabel', background='#333333', foreground='white')
    style.configure('TEntry', background='#1e1e1e', foreground='white', fieldbackground='#1e1e1e')
    style.configure('TButton', background='#333333', foreground='white')
    style.configure('TScrolledText', background='#1e1e1e', foreground='white')
    
    #frame it
    frame = ttk.Frame(root, style='TFrame')
    frame.pack(padx=10, pady=10)

    entry_label = ttk.Label(frame, text="Enter your search query:", style='TLabel')
    entry_label.pack()

    entry = ttk.Entry(frame, style='TEntry', width=50)
    entry.pack()

    search_button = ttk.Button(frame, text="Search", command=lambda: threading.Thread(target=run_search).start(), style='TButton')
    search_button.pack()

    result_area = scrolledtext.ScrolledText(frame, background='#1e1e1e', foreground='white')
    result_area.pack()

    root.mainloop()
                    

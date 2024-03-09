import os
import ujson
import time
import tkinter as tk
from tkinter import scrolledtext
import threading
from datadump import alpha_sort, push_to_disk
from bs4 import BeautifulSoup
from helper_funcs import retrieve_word, get_url
# doc:  https://www.crummy.com/software/BeautifulSoup/bs4/doc/

import nltk
from nltk.stem import PorterStemmer
# doc: https://www.nltk.org/, and class
# from spellchecker import SpellChecker

#this is the function to process the html files 
#as of right now it grabs the important text BUT DOESNT DO ANYTHING WITH it
#for now its just returning all the text not including the important ones)
#later we might use the important ones for something

def find_the_best_docs(tokens_dict):
    #tokens dict is
    #{term : { docid : (termfreq , [pos] ) } }
    returnable = []
    
    if len(tokens_dict.keys()) == 1: # sort by frequency if there is just one token
        onlykey = list(tokens_dict.keys())[0] # makes a key of the only token
        returnable = sorted(tokens_dict[onlykey], key=lambda x: tokens_dict[onlykey][x][0], reverse=True) #sorts in order of most frequent to least frequent
    else:
        new_tokens_dict = dict()
        for token in tokens_dict.keys(): #for each key
            docids = sorted(tokens_dict[token], key=lambda x: tokens_dict[token][x][0], reverse=True) #sorts in order of most frequent to least frequent
            new_tokens_dict[token] = docids #add the docids


        concat_urls = []

        for token in new_tokens_dict.keys(): #compiles all the docids into one list
            concat_urls += new_tokens_dict[token]

        #sorts based on most docid hits. if they are the same, then the frequency sorting from above takes precedent.
        concat_urls = sorted(concat_urls, key=lambda x: concat_urls.count(x), reverse=True)
        # for loop is for unqiue docIDs
        for docid in concat_urls:
            if docid not in returnable:
                returnable.append(docid)

    return returnable

def validate_query(query):
    # spelling check initialization
    # spell = SpellChecker()
    # tokenize user input
    query_tokens = nltk.word_tokenize(query)
    
    refined_tokens = []

    for token in query_tokens:
        # Handle acronyms (fully upper case tokens)
        if token.isupper():
            refined_tokens.append(token.lower())
            continue
        # check for capitalized tokens
        # lowercasing capitalized tokens might not be desirable in all cases especially for proper nouns
        if token[0].isupper():
            refined_tokens.append(token.lower())
            continue
        else:
            # spelling correction 
            # corrected = spell.correction(token)
            refined_tokens.append(token)
            # now lemmatize term using WordNet
            # this works for for some inputs that are miss typed but it also affects correct input so this requires more work
            #synonyms = wordnet.synsets(corrected)
            #if synonyms:
            #    # get the most general word
            #    lemma_names = synonyms[0].lemma_names()
            #    if lemma_names:
            #        corrected = lemma_names[0]  # Taking the first synonym as the corrected term

            # refined_tokens.append(refined_tokens)
            
    return refined_tokens


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

    result_area.delete('1.0', tk.END)
    for key, item in empty_dict.items():
        for tup in item:
            result_area.insert(tk.END, f"{tup}\n")


if __name__ == "__main__":
    # Tkinter GUI setup
    root = tk.Tk()
    root.title("Search Application")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    entry_label = tk.Label(frame, text="Enter your search query:")
    entry_label.pack()

    entry = tk.Entry(frame, width=50)
    entry.pack()

    search_button = tk.Button(frame, text="Search", command=lambda: threading.Thread(target=run_search).start())
    search_button.pack()

    result_area = scrolledtext.ScrolledText(frame, width=60, height=15)
    result_area.pack()

    root.mainloop()
                    

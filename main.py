import os
import ujson
import time
from datadump import alpha_sort, push_to_disk
from bs4 import BeautifulSoup
from helper_funcs import retrieve_word, get_url
# doc:  https://www.crummy.com/software/BeautifulSoup/bs4/doc/
import math
import nltk
from nltk.stem import PorterStemmer
# doc: https://www.nltk.org/, and class
# from spellchecker import SpellChecker

#this is the function to process the html files 
#as of right now it grabs the important text BUT DOESNT DO ANYTHING WITH it
#for now its just returning all the text not including the important ones)
#later we might use the important ones for something
def find_the_best_docs(tokens_dict): # SCORING AND ORDERING

    td_to_w = dict()
# { token : [ (docID, [position, position2, ..., positionx])] }
    N = 40000 # CHANGE FROM HARDCODE TODO
    for term in tokens_dict.keys():
        df_t = len(tokens_dict[term])
        for docinfo in tokens_dict[term]:
            docid = docinfo[0]
            tf_td = len(docinfo[1])
            w_td = (1 + math.log10(tf_td)) * math.log10(N / df_t) #Equation from lectures
            td_to_w [(term,docid)] = w_td
    if len(tokens_dict) == 1:
        final_rank = sorted(list(td_to_w.keys()), key=lambda x: td_to_w [x], reverse = True)
        last_web_rank = []
        for f in final_rank:
            last_web_rank.append(f[1])
    else:
        combin_weights = dict()
        for term, docid in td_to_w.keys():
            if docid in combin_weights:
                combin_weights [docid] += td_to_w[(term, docid)]
            else:
                combin_weights [docid] = td_to_w[(term, docid)]
        last_web_rank = sorted(list(combin_weights.keys()), key=lambda x: combin_weights [x], reverse = True)
        #print(combin_weights)


    return last_web_rank
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

if __name__ == "__main__":
    while True:
            user_query = input("Enter your search query (or type exit to quit): ").strip()
            if user_query.lower() == "exit":
                break
            # start = time.time()
            valid_token = validate_query(user_query)
# iftekhar ahmed
            print(f"Valid token: {valid_token}")
            empty_dict = dict()
            stemmer = PorterStemmer()
            for token in valid_token:
                stem_token = stemmer.stem(token)
                dicts_word = retrieve_word(stem_token)
                if dicts_word != None:
                    empty_dict[stem_token] = retrieve_word(stem_token)
            for docID in find_the_best_docs(empty_dict)[0:5]:
                print(get_url(docID))

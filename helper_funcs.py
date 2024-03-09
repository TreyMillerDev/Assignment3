import pickle
import json
import math
import os
import ujson
import time
from datadump import alpha_sort, push_to_disk
from bs4 import BeautifulSoup
# doc:  https://www.crummy.com/software/BeautifulSoup/bs4/doc/
import nltk
from nltk.stem import PorterStemmer
# from main import clear_directory



# EVERYTHING UNDER HERE IS FOR INFO RETRIEVAL FROM REVERSE INDEX AND DATA SORTING RESULTING QUEIRES 
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

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
        for docid in concat_urls:
            if docid not in returnable:
                returnable.append(docid)

    return returnable

def sort_JSONS_into_pickle(): #sort pkl files into more managable lists 
    for letter in alphabet:
        replacement_dict = dict()

        with open(f"Inverted_index/{letter}.pkl", 'rb') as fp:
            data = pickle.load(fp) # that speicifc letter.json file 

            # token : [ (freq, docID, position), (freq, docID, position2)] will become underneath
            # token : [ (docID, freq, [position, position2])]
            new_data = dict()
            for token in sorted(data.keys()): # seperate the key from the value 
                list_tups = data[token] # lsit_tups is a list of tuples related to that token 
                new_list_tups = []
                replacement_dict = dict()
             # list_tups = [(3, 15),( 3, 16),(3, 17) ]
                for item in list_tups:
                    if item[0] not in replacement_dict:
                        replacement_dict[item[0]] = [item[1]]
                    else:
                        replacement_dict[item[0]].append(item[1])

                # take the items in replace_dict and place them as a combined tuple inside of the new_list_tuple 
                # replacement_dict = { docID: (freq, [position position2]) }
                for key in sorted(replacement_dict.keys()):
                    new_list_tups.append( (key, sorted(replacement_dict[key]))  )
                new_data[token] = new_list_tups
                

            with open(f"Inverted_index/{letter}.pkl", 'wb') as fj: # rewrite the file with the new information 
                pickle.dump(new_data,fj)

# def visualize_into_jsons(): # conver thte pkls into visual json file MUST CREATE DIRECTORY: visuals
#     for letter in alphabet:
#         with open(f"alphaJSON/{letter}.pkl", 'rb') as fp:
#             data = pickle.load(fp) # the dictionary kinda of nightmare 
#             with open(f"visuals/{letter}.json", 'w') as fj:
#                 json.dump(data,fj, indent= 1)

def get_url(docID):
    with open(f"DocID.pkl", 'rb') as fp:
            data = pickle.load(fp) # the dictionary kinda of nightmare 
    return data[docID]

def find_file(url, directory): # given url and directory find thtat speicifc json folder with that url 
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as json_file:
                    data = ujson.load(json_file)
                    if (data['url'] == url):
                        print(file)
                        return
    return

def checkSum_Hash(words_only):
    sums = set()

    for word in range(len(words_only)):
        if (word + 4) < len(words_only): # 0-4, 1-5, 2-6, making sure its in the range 
            checksum = 0 # sum the the 4-word-sub
            N_GRAM = ''.join(words_only[word:word+4])
            for i in N_GRAM: # iterate through words adding the ASCII values of the char 
                for let in i:
                    checksum += ord(let)

            sums.add(checksum)
            checksum = 0

    return tuple(set([num for num in sums if num % 15 == 0]))

def retrieve_word(word):
    letter = word[0] # gets the first letter 
    with open(f"Inverted_index/{letter}.pkl", 'rb') as fp:
            data = pickle.load(fp) # the dictionary kinda of nightmare 
    if word in data.keys():
        return data[word] # assume word is in the data file 

def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                # If you also want to remove subdirectories, uncomment the next line
                # shutil.rmtree(file_path)
                pass
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# EVERYTHING UNDER HERE IS FOR FILE READING AND JSON CONTENT RETREIVAL FROM DEV FOLDERS 

def process_html(content):
    soup = BeautifulSoup(content, 'html.parser')

    #find and flag important text
    important_words = set()
    for tag in soup.find_all(['b', 'strong', 'h1', 'h2', 'h3', 'title']):
        important_words.update(tag.get_text().split())

    #then just grab all the text (including important ones)
    all_text = soup.get_text()

    #return tuple of all text and a set of important words
    return all_text, important_words

def tokenize(text: str) -> list:
    tokenList = []  # Initialize the list of tokens
    word = ""  # Init a placeholder string
    for cha in text:  # For each character in the text
        # If it is an uppercase letter, make the character lowercase
        if 65 <= ord(cha) <= 90:
            cha = chr(ord(cha) + 32)
            word += cha
        # If it is a lowercase letter or number
        elif (97 <= ord(cha) <= 122):
            word += cha
        else:  # If it is a divider
            if word != "":  # If the word is not an empty string
                tokenList.append(word)  # Add the word to the token list
                word = ""  # Reset the word
    # Add the last word if not empty (for cases when text does not end with a divider)
    if word != "":
        tokenList.append(word)
    
    return tokenList

def stem_text(text):
    # Initialize a stemmer
    stemmer = PorterStemmer()

    # Tokenize using the custom tokenize function instead of NLTK
    tokens = tokenize(text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    return stemmed_tokens

def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                # If you also want to remove subdirectories, uncomment the next line
                # shutil.rmtree(file_path)
                pass
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

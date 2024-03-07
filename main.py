import os
import ujson
import time
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

#Deploy if we are supposed to process only unique tokens in a url
def indexify(data_list):
    start = time.time()
    total = dict()
    for dat in data_list:
        unique_tokens = list(set(dat['stemmed_content'].split()))
        for token in unique_tokens:
            if token not in total.keys():
                total[token] = [dat['url']]
            else:
                total[token].append(dat['url'])
        if len(total) > 500:
            total_sorted = alpha_sort(total)
            push_to_disk(total_sorted)
            total.clear()
            total_sorted.clear()
    end = time.time()
    processing_time = (end - start) 
    print(f"Processing Time: {processing_time}s")
    return total   

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


def file_processor(directory="DEV"):
    # Initialize list to store data from json file
    num = 0
    # Calculate the time taken to process all json files in the DEV folder
    start = time.time()

    #create variables to track the number of files the tokens and the unique tokens
    num_files = 0
    total_tokens = 0
    unique_tokens = set()
    total = {}

    # Loop through folders in DEV folder
    for root, dirs, files in os.walk(directory):
        # Loop through json files in folder
        for file in files:
            if num < 10000 and file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as json_file:
                    data = ujson.load(json_file)

                    if 'content' in data and data['content'].startswith('<'):
                        # there is stuff we can check
                        all_text, _ = process_html(data['content'])

                        # Apply stemming to all_text
                        stemmed_text = stem_text(all_text)

                        # keep track and increment
                        total_tokens += len(stemmed_text)
                        unique_tokens.update(stemmed_text)

                        for token in stemmed_text:
                            if token not in total.keys():
                                total[token] = [data['url']]
                            else:
                                total[token].append(data['url'])
                            if len(total) > 1000:
                                print('Just cleared, moving onto next set: ', data['url'], num)
                                total_sorted = alpha_sort(total)
                                push_to_disk(total_sorted)
                                total.clear()
                                total_sorted.clear()
                        # data_list.append({'url': data['url'], 'stemmed_content': "".join(stemmed_text)})

                        num_files += 1
                        num += 1

    end = time.time()

    # Calculate metrics
    processing_time = (end - start) * 1000
    avg_doc_length = total_tokens / num_files if num_files > 0 else 0

    # now print the important metrics
    print(f"Processed {num_files} files")
    print(f"Total tokens: {total_tokens}")
    print(f"Unique tokens: {len(unique_tokens)}")
    print(f"Average document length: {avg_doc_length} tokens")
    print(f"Processing time: {processing_time:.03f}ms")

# here is the simple loop that ask user for query (typing exit to exit)
# once web GUI is implemented we will replace this with web GUI

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
                    # print(len(dicts_word))
            
            for docID in find_the_best_docs(empty_dict)[0:5]:
                print(get_url(docID))

            # end = time.time()
            # print((end - start))
                    # print(get_url(docID))
                    # for id in list(dicts_word.keys())[0:5]:
                    #     print(get_url(id))
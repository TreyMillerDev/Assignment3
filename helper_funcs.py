import pickle
import json
import ujson
import os
import math
# from main import clear_directory
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

        with open(f"alphaJSON/{letter}.pkl", 'rb') as fp:
            data = pickle.load(fp) # that speicifc letter.json file 

            # token : [ (freq, docID, position), (freq, docID, position2)] will become underneath
            # token : [ (docID, freq, [position, position2])]
            new_data = dict()
            for token in data.keys(): # seperate the key from the value 
                list_tups = data[token] # lsit_tups is a list of tuples related to that token 
                new_list_tups = []
                replacement_dict = dict()
             # list_tups = [(.00124, 3, 15),(.00124, 3, 16),(.00124, 3, 17) ]
                for item in list_tups:
                    if item[1] not in replacement_dict:
                        replacement_dict[item[1]] = (item[0], [item[2]])
                    else:
                        replacement_dict[item[1]][1].append(item[2])

                # take the items in replace_dict and place them as a combined tuple inside of the new_list_tuple 
                # replacement_dict = { docID: (freq, [position position2]) }
                for key, item in replacement_dict.items():
                    new_list_tups.append((key,item[0],item[1]))

                new_data[token] = new_list_tups
                

            with open(f"sortedJSON/{letter}.pkl", 'wb') as fj:
                pickle.dump(new_data,fj)

def visualize_into_jsons(): # conver thte pkls into visual json file MUST CREATE DIRECTORY: visuals
    for letter in alphabet:
        with open(f"sortedJSON/{letter}.pkl", 'rb') as fp:
            data = pickle.load(fp) # the dictionary kinda of nightmare 
            with open(f"visuals/{letter}.json", 'w') as fj:
                json.dump(data,fj, indent= 1)

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
def retrieve_word(word):
    letter = word[0] # gets the first letter 
    with open(f"sortedJSON/{letter}.pkl", 'rb') as fp:
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


if __name__ == "__main__":
    clear_directory(f'sortedJSON/')
    clear_directory(f'visuals/')
    sort_JSONS_into_pickle()
    visualize_into_jsons()

    # print(retrieve_word("machi"))
    # {22728: (0.0020408163265306124, [104]), 3674: (0.0040650406504065045, [73]), 3842: (0.0040650406504065045, [73])}
    # print(get_url(22728))
    # print(get_url(3674))
    # print(get_url(3842))

# https://www.ics.uci.edu/~kkask/Fall-2014%20CS271/index.html
# https://iasl.ics.uci.edu/people/ahmedn/#levorato-ahmed-2014-smartgridcomm
# http://iasl.ics.uci.edu/people/ahmedn/
    # find_file("https://www.ics.uci.edu/~iftekha/publication/applying-mutation-analysis-on-kernel-test-suites-an-experience-report/", 'DEV/www_ics_uci_edu/')
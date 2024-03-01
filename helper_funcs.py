import pickle
import json
import ujson
import os
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
 
def sort_JSONS_into_pickle(): #sort pkl files MUST CREATE A DIRECTORY : sortedJSON
    for letter in alphabet:
        replacement_dict = dict()

        with open(f"alphaJSON/{letter}.pkl", 'rb') as fp:
            data = pickle.load(fp) # the dictionary kinda of nightmare 
            # print(data)
            for token, list_tups in data.items(): # seperate the key from the value 
                replacement_dict[token] = dict()
            #     # token = word 
            #     # list_tups = [(.00124, 3, 15),(.00124, 3, 15),(.00124, 3, 15) ]
            # for item in list_tups:
                for item in list_tups:
                    if item[1] not in replacement_dict[token]:
                        replacement_dict[token][item[1]] = (item[0], [item[2]])
                    else:
                        replacement_dict[token][item[1]][1].append(item[2])

                # data = pickle.load(fp) # the dictionary kinda of nightmare
            with open(f"sortedJSON/{letter}.pkl", 'wb') as fj:
                pickle.dump(replacement_dict,fj)

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

if __name__ == "__main__":
    # sort_JSONS_into_pickle()
    # print(retrieve_word("ahmedn"))
    # {22728: (0.0020408163265306124, [104]), 3674: (0.0040650406504065045, [73]), 3842: (0.0040650406504065045, [73])}
    # print(get_url(22728))
    # print(get_url(3674))
    # print(get_url(3842))

# https://www.ics.uci.edu/~kkask/Fall-2014%20CS271/index.html
# https://iasl.ics.uci.edu/people/ahmedn/#levorato-ahmed-2014-smartgridcomm
# http://iasl.ics.uci.edu/people/ahmedn/
    find_file("http://iasl.ics.uci.edu/people/ahmedn/", 'DEV/iasl_ics_uci_edu/')
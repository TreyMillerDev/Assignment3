import pickle
import threading
import os

def alpha_sort(random_dict):
    alpha_sorted_dict = {}
    starting_letter = 'a'
    for key, value in random_dict.items():
        if key[0] == starting_letter and starting_letter not in alpha_sorted_dict: # we havent hit that letter yet
            alpha_sorted_dict[starting_letter] = {key:value}
        elif key[0] == starting_letter: # letter already exists 
            alpha_sorted_dict[starting_letter][key] = value
        else: # we have a different letter 
            starting_letter = key[0] # update the letter 
            if key[0] == starting_letter and starting_letter not in alpha_sorted_dict: # we havent hit that letter yet
                alpha_sorted_dict[starting_letter] = {key:value}
            elif key[0] == starting_letter: # letter already exists 
                alpha_sorted_dict[starting_letter][key] = value
    random_dict = {} # empty our old container 
    return alpha_sorted_dict # return the newly sorted containr 

def push_to_disk(id, sorted_dict, lock):

    invalid_key_names = { ":" : "colon", "/": "backslash", "\\": "forwardslash", "." : "period" }
    lock.acquire()
    # print(f"worker {id}, has locked and is modifying json file")
    while (len(sorted_dict) != 0):
        key, val = sorted_dict.popitem() # pop the first dict in our sorted_dict 
        if key in invalid_key_names:
                key = invalid_key_names[key]
            
        file_path = f'alphaJSON/{key}.pkl'
         # CRITICAL SECTION ##########

        try:
                
            subsection = dict(sorted(val.items())) # we take our subsection dict and sort that small sub
                # inorder = [sorted(sorted_dict[key])] # store and sort the dict that contains just the letter 
            with open(file_path, 'rb') as json_file:
                data = pickle.load(json_file) # retrieve the file info


                # data dict is already sorted
                # our letter dict is also sorted 
            combined_dict = {}
            for key in sorted(set(subsection.keys()).union(data.keys())):
                if key in subsection and key in data: # both dicts share a key 
                    combined_dict[key] = sorted(set(subsection[key] + data[key])) # take both lists and combine them
                elif key in subsection: # the key is in one or the other but not both 
                    combined_dict[key] = sorted(set(subsection[key]))
                else:
                    combined_dict[key] = sorted(set(data[key]))

            with open(file_path, 'wb') as json_file:
                pickle.dump(combined_dict, json_file) # update the new json file 

        except (FileNotFoundError):
            with open(file_path, 'wb') as json_file:
                pickle.dump(subsection, json_file)
        
    lock.release()        
    # print(f"worker {id} has finisehd modifying json file ")

def save_docID(docID, lock):
    lock.acquire()
    try:
        with open("DocID.pkl", 'rb') as json_file:
            data = pickle.load(json_file) # retrieve the file info
        data.update(docID)

        with open("DocID.pkl", 'wb') as json_file:
                pickle.dump(data, json_file) # update the new json file 
        
    except (FileNotFoundError):
        with open("DocID.pkl", 'wb') as json_file:
            pickle.dump(docID, json_file)

    lock.release() 



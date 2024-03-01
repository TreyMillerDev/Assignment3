import pickle
import json

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
 
def sort_JSONS_into_pickle():
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

def visualize_into_jsons():
    for letter in alphabet:
        with open(f"sortedJSON/{letter}.pkl", 'rb') as fp:
            data = pickle.load(fp) # the dictionary kinda of nightmare 
            with open(f"visuals/{letter}.json", 'w') as fj:
                json.dump(replacement_dict,fj)
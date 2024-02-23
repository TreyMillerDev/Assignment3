import json

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


def push_to_disk(sorted_dict):
    # print(sorted_dict)
    for key, val in sorted_dict.items():
        try:
            file_path = f'alphaJSON/{key}.json'
            subsection = dict(sorted(val.items())) # we take our subsection dict and sort that small sub
            # inorder = [sorted(sorted_dict[key])] # store and sort the dict that contains just the letter 
            with open(file_path, 'r') as json_file:
                data = json.load(json_file) # retrieve the file info


            # do some data modification magic here 

            # data.append(subsection) # add the sorted dict of just that letter to our json list




            with open(file_path, 'w') as json_file: # update our json file 
                json.dump(data, json_file, indent = 2)

        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Creating a new JSON file at '{file_path}'.")
            with open(file_path, 'w') as json_file:
                json.dump(subsection, json_file, indent = 1)
            print("New JSON file created.")

    sorted_dict = {} # empty container


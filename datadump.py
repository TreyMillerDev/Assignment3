import json

x = {'Serendipity': [98, 9, 2, 62, 30], 'Aplomb': [22, 35, 76, 75, 95], 
'Quixotic': [62, 23, 86, 28, 44], 'Obfuscate': [80, 69, 14, 50, 11], 
'Perfidious': [89, 51, 30, 6, 79], 'Sycophant': [46, 13, 32, 56, 65], 
'Belligerent': [78, 38, 89, 85, 48], 'Ephemeral': [66, 48, 46, 26, 46], 
'Mellifluous': [42, 61, 8, 3, 39], 'Nefarious': [19, 7, 46, 94, 78], 
'Pernicious': [71, 70, 77, 96, 49], 'Ubiquitous': [19, 9, 24, 28, 96], 
'Quagmire': [27, 29, 36, 58, 100], 'Juxtapose': [37, 54, 7, 97, 21],
 'Ebullient': [36, 13, 3, 3, 64], 'Sanguine': [48, 10, 26, 62, 66], 
 'Cacophony': [90, 23, 25, 5, 6], 'Serendipitous': [81, 58, 59, 22, 11],
  'Lethargic': [46, 16, 76, 11, 53], 'Plethora': [68, 71, 84, 45, 90], 
  'Nascent': [64, 65, 56, 84, 6], 'Halcyon': [26, 9, 2, 77, 78], 
  'Pulchritudinous': [76, 94, 86, 15, 94], 'Quizzical': [100, 32, 67, 1, 88], 
  'Disparate': [43, 65, 99, 52, 54], 'Ephemeralize': [15, 24, 2, 25, 22], 
  'Recalcitrant': [35, 85, 26, 72, 35], 'Xenophile': [4, 31, 58, 39, 47],
   'Zeitgeist': [70, 87, 69, 52, 7], 'Supercilious': [58, 85, 10, 36, 36], 
   'Quintessential': [52, 84, 67, 77, 43], 'Ineffable': [48, 55, 55, 45, 17], 
   'Vorfreude': [77, 62, 65, 11, 21], 'Sesquipedalian': [30, 78, 18, 31, 41], 
   'Ubiquity': [43, 16, 99, 15, 63], 'Lugubrious': [37, 58, 71, 78, 87], 
   'Perfunctory': [62, 14, 89, 21, 8], 'Quotidian': [58, 97, 60, 98, 19], 
   'Munificent': [55, 41, 32, 93, 6], 'Ephemeron': [78, 68, 45, 71, 73], 
   'Indefatigable': [75, 74, 37, 73, 67], 'Nomenclature': [85, 93, 8, 79, 39],
    'Serendipitously': [83, 81, 13, 87, 7], 'Discombobulate': [63, 30, 22, 79, 99],
     'Obstreperous': [97, 74, 73, 96, 20], 'Pulchritude': [39, 7, 1, 60, 40], 
     'Sycophantic': [92, 58, 52, 91, 40], 'Ineffability': [12, 92, 12, 69, 63], 
     'Quinquagenarian': [52, 56, 18, 100, 10], 'Vivacious': [70, 62, 81, 11, 80], 
     'Zephyr': [41, 48, 3, 77, 47], 'Ostentatious': [38, 88, 71, 40, 41], 
     'Rambunctious': [70, 70, 65, 40, 55], 'Esoteric': [36, 31, 44, 41, 65], 
     'Idiosyncrasy': [44, 6, 51, 33, 6], 'Labyrinthine': [100, 40, 62, 21, 27], 
     'Peculiar': [85, 8, 21, 23, 25], 'Querulous': [86, 82, 36, 90, 65], 
     'Ephemeralizing': [80, 79, 52, 35, 15], 'Noctilucent': [57, 28, 65, 13, 77], 
     'Ebullience': [90, 11, 56, 20, 45], 'Sycophantism': [13, 20, 84, 2, 41],
      'Mellifluously': [6, 49, 49, 77, 50], 'Nefariousness': [7, 25, 85, 29, 54], 
      'Perniciousness': [70, 66, 13, 67, 83], 'Ubiquitously': [49, 94, 23, 4, 92]}

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
    while (len(sorted_dict) != 0):
        key, val = sorted_dict.popitem() # pop the first dict in our sorted_dict 
        try:
            file_path = f'alphaJSON/{key}.json'
            subsection = dict(sorted(val.items())) # we take our subsection dict and sort that small sub
            # inorder = [sorted(sorted_dict[key])] # store and sort the dict that contains just the letter 
            with open(file_path, 'r') as json_file:
                data = json.load(json_file) # retrieve the file info


            # data dict is already sorted
            # our letter dict is also sorted 
            combined_dict = {}
            for key in sorted(set(subsection.keys()).union(data.keys())):
                if key in subsection and data: # both dicts share a key 
                    combined_dict[key] = sorted(subsection[key] + data[key]) # take both lists and combine them
                elif key in subsection: # the key is in one or the other but not both 
                    combined_dict[key] = sorted(subsection[key])
                else:
                    combined_dict[key] = sorted(data[key])

            with open(file_path, 'w') as json_file:
                json.dump(combined_dict, json_file, indent = 1) # update the new json file 

        except (FileNotFoundError, json.JSONDecodeError):
            with open(file_path, 'w') as json_file:
                json.dump(subsection, json_file, indent = 1)


x = alpha_sort(x)
push_to_disk(x)

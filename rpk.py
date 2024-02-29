import pickle
import json

with open("DocID.pkl", 'rb') as json_file:
            data = pickle.load(json_file) # retrieve the file info
            with open('tmp.json', 'w') as js:
                json.dump(data,js,indent=1)
                # if val == "http://xtune.ics.uci.edu/":
                
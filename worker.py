from threading import Thread
import ujson
from datadump import alpha_sort, push_to_disk, save_docID
from main import stem_text, process_html
import os
import json

class Worker(Thread):

    def __init__(self, worker_id, crawl_range, Lock, counter):

        # need a dict reverse index 
        # NOTE: Each worker will handle their OWN dictionary, 
        # collisions should be focused on the json files not the dicts themselves 
        super().__init__()
        self.list_of_directories = crawl_range 
        self.id = worker_id
        # print(self.id, self.list_of_directories)

        self.lock = Lock
        self.counter = counter

        self.total = dict()
        self.main_dir = 'DEV/' # main directory we are working in  
        self.freq_dict = dict() # this dict will be used to calc tf-idf score 
        self.DocID = dict() # dict to keep track of urls and their IDs


    def get_freq(self, stemmed_text):
        for word in stemmed_text:
            if word not in self.freq_dict:
                self.freq_dict[word] = 1 # word doesn't exist, minus one 
            else:
                self.freq_dict[word] += 1 # word exists add plus one


    def run(self):
        """ We run the file and parsing and stuff
            
            class wide variables:
                set of unique urls
                count of total tokens
                number files
                
            private class variables:
                reverse index dictionary"""

        # print(self.list_of_directories)
        for dir in self.list_of_directories: # this access all the files in the sub directory
            dir_path = os.path.join(self.main_dir,dir)
            
            for file in os.listdir(dir_path):
                acc_file = os.path.join(dir_path,file)
                # os.path.join(dir_path,file)
               
                with open(acc_file, 'r') as json_file:
                    data = ujson.load(json_file)
                    
                    if 'content' in data and data['content'].startswith('<'):
                         # there is stuff we can check
                        all_text, _ = process_html(data['content'])
                        # Apply stemming to all_text
                        stemmed_text = stem_text(all_text)
                        self.get_freq(stemmed_text) # count the freq of words 

                        self.counter.inc_files(len(stemmed_text), data['url'])
                        curr_doc_id = self.counter.get_files()
                        self.DocID[curr_doc_id] = data['url'] # add that docID to ur own personal dict 

                        if len(self.DocID) > 3000:
                            save_docID(self.DocID, self.lock)
                            self.DocID.clear()

                        for token in range(len(stemmed_text)):
                            if stemmed_text[token] not in self.total.keys():
                                self.total[stemmed_text[token]] = [((self.freq_dict[stemmed_text[token]] / len(stemmed_text)) ,curr_doc_id, token+1)] 
                                # we pass in a tuple, (int, int, int)
                                # (tf-tdf score, docID , position of that word )
                            else:
                                self.total[stemmed_text[token]].append(((self.freq_dict[stemmed_text[token]] / len(stemmed_text)) ,curr_doc_id, token+1)) # add that url to that token
                        
                        if len(self.total) > 4000:
                            self.total = alpha_sort(self.total)
                            push_to_disk(self.id, self.total,self.lock)
                            self.total.clear()
                            print(f"worker no {self.id} finished loading data, {data['url']} doc id {curr_doc_id}")

                        self.freq_dict.clear() # empty our dict for new set of words 

        if len(self.DocID) != 0: # not empty 
            save_docID(self.DocID, self.lock)
            self.DocID.clear()
            print(f"worker {self.id} has published the rest of his docIDs")


        if (len(self.total) != 0):
            self.total = alpha_sort(self.total)
            push_to_disk(self.id, self.total,self.lock)
            self.total.clear()
        print(f"worker no {self.id} has finished, putting to sleep, good night :)")

#DEV/i-sensorium_ics_uci_edu/3e0c766607091d03548116d270df672dbe0f63a3d8191b5b158402f2448f72ea.json
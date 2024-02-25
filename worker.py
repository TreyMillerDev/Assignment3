from threading import Thread
import ujson
from datadump import alpha_sort, push_to_disk
from main import stem_text, process_html
import os




class Worker(Thread):

    def __init__(self, worker_id, crawl_range, Lock, counter):

         # need a dict reverse index 
        # NOTE: Each worker will handle their OWN dictionary, 
        #collisions should be focused on the json files not the dicts themselves 
        super().__init__()
        self.list_of_directories = crawl_range 

        self.id = worker_id
        self.lock = Lock
        self.counter = counter

        self.total = dict()
        self.main_dir = 'DEV/' # main directory we are working in  

        


    def run(self):
        """ We run the file and parsing and stuff
            
            class wide variables:
                set of unique urls
                count of total tokens
                number files
                
            private class variables:
                reverse index dictionary"""

        for subdir in self.list_of_directories:
            file_path = os.path.join(self.main_dir, subdir)
            for file in os.listdir(file_path): # this access all the files in the sub directory
                acc_file = os.path.join(file_path,file)
                # if (self.counter.get_files() > 10000):
                #     break
                with open(acc_file, 'r') as json_file:
                    data = ujson.load(json_file)

                    if 'content' in data and data['content'].startswith('<'):
                        # there is stuff we can check
                        all_text, _ = process_html(data['content'])

                        # Apply stemming to all_text
                        stemmed_text = stem_text(all_text)
                        self.counter.inc_files(len(stemmed_text), data['url'])
                        for token in stemmed_text:
                            if token not in self.total.keys():
                                self.total[token] = [data['url']]
                            else:
                                self.total[token].append(data['url'])
                            if len(self.total) > 4000:
                                print(f'worker no {self.id} full cleared, moving onto next set: ', acc_file,self.counter.get_files())
                                self.total = alpha_sort(self.total)
                                push_to_disk(self.id, self.total,self.lock)
                                self.total.clear()
        if (len(self.total) != 0):
            self.total = alpha_sort(self.total)
            push_to_disk(self.id, self.total,self.lock)
            self.total.clear()
        print(f"worker no {self.id} has finished, putting to sleep, good night :)")

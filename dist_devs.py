import os 
import math
from worker import Worker
import threading
from helper_funcs import clear_directory, sort_JSONS_into_pickle, visualize_into_jsons
import time

def create_paritions(thread_count, directory_path = 'DEV/')-> list:
    """ Goes into the DEV folder and distributes each sub folder into different lists
    
    Returns a nested list with thread_count number of sublists 
    [ [some subfolders ], [some subfolders], [some subfolders], [some subfolders]]
    """
    subs = []
    for x in range(thread_count):
        subs.append([])
    x = 0   
    for dirs in os.listdir(directory_path):
            subs[x].append(dirs)
            x += 1

            if x == thread_count:
                x = 0
    return subs

class Count:
    """ Use to keep consistency in the counting of docs/files when threading. 
    Mainly to avoid overlapping or improper access to variables """
    def __init__(self):
        self.num_files = 0 # total number of files 
        self.total_tokens = 0 # total number of tokens 
        self.lock = threading.Lock() # a thread lock to prevent bad access

    def inc_files(self, total_tokens, url):
        """ This is where values are updated by the workers, only 1 worker can access these variables at a time"""
        with self.lock:
            self.num_files += 1
            self.total_tokens += total_tokens
    
    def get_files(self):
        return self.num_files

    def get_tokens(self):
        return self.total_tokens



class Create_workers:

    def __init__(self,count, main_dev = 'DEV/'):
        
        self.items = os.listdir(main_dev) # gets a list of all the sub-directories 
        self.workers = list([])
        self.thread_count = 8
        self.subs = create_paritions(self.thread_count)
        print("finished partitions")

        self.lock = threading.Lock()
        # uniques, total_tokens, num_files
        self.counter = count
        

    def create_workers(self):
        """ Breaks the list if sub directories into sections that each crawler will handle"""
        for x in range(self.thread_count):
            self.workers.append(Worker(x,self.subs[x], self.lock, self.counter))

        # This starts the threading 
        for worker in self.workers:
            worker.start()

    def start(self):
        self.create_workers()
        self.join()

    def join(self):
        for worker in self.workers:
            worker.join()

def main():
    start = time.time()
    count = Count()
    clear_directory(f'alphaJSON/')
    if os.path.exists("DocID.pkl"):
        os.remove("DocID.pkl")

    working = Create_workers(count)
    working.start()

    # avg_doc_length = count.get_tokens() / count.get_files() if count.get_files() > 0 else 0
    # print(f"Processed {count.get_files()} files")
    # print(f"Total tokens: {count.get_tokens()}")
    # # print(f"Unique tokens: {count.get_urls()}")
    # print(f"Average document length: {avg_doc_length} tokens")
    sort_JSONS_into_pickle()

    end = time.time()
    processing_time = (end - start) * 1000
    print(f"Processing time: {processing_time:.03f}ms")

if __name__== "__main__":
    # main()
    sort_JSONS_into_pickle()
    # clear_directory("visuals/")
    # visualize_into_jsons()

    

import os 
import math
from worker import Worker
import threading
from main import clear_directory
import time

def create_paritions(thread_count, directory_path = 'DEV/'):
    subs = []
    # print(sorted(file_in_dir))
    for x in range(thread_count):
        subs.append([])
    x = 0
    for dirs in os.listdir(directory_path):
            # Loop through json files in folder
            # if file.endswith(".json"):
            # file_path = os.path.join(directory_path, dirs)
            subs[x].append(dirs)
            x += 1

            if x == thread_count:
                x = 0
    return subs

class Count:

    def __init__(self):
        self.num_files = 0
        self.total_tokens = 0
        self.unq_url = set()
        self.lock = threading.Lock()

    def inc_files(self, total_tokens, url):
        with self.lock:
            self.num_files += 1
            self.total_tokens += total_tokens
            self.unq_url.add(url)
    
    def get_files(self):
        return self.num_files

    def get_tokens(self):
        return self.total_tokens

    def get_urls(self):
        return len(self.unq_url)


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
        """ Breaks the list if sub directories into sections that each crawler will handle , 
            size of sub = 22 sub directory folders """

        # dist_factor = math.floor(len(self.items) / self.thread_count)
         # split our data set into smaller parts 
        for x in range(self.thread_count):
            self.workers.append(Worker(x,self.subs[x], self.lock, self.counter))
            # if x == self.thread_count - 1:
            #     subdir_section = self.items[x*dist_factor: len(self.items)]
            #     self.workers.append(Worker(x,subdir_section, self.lock, self.counter))
            # else:
            #     subdir_section = self.items[x * dist_factor: (x+1)* dist_factor]
            #     self.workers.append(Worker(x,subdir_section, self.lock, self.counter))

        # self.subs = [] # empty that so we don't hold the urls no more 

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
    end = time.time()
    processing_time = (end - start) * 1000
    avg_doc_length = count.get_tokens() / count.get_files() if count.get_files() > 0 else 0
    print(f"Processed {count.get_files()} files")
    print(f"Total tokens: {count.get_tokens()}")
    print(f"Unique tokens: {count.get_urls()}")
    print(f"Average document length: {avg_doc_length} tokens")
    print(f"Processing time: {processing_time:.03f}ms")

if __name__== "__main__":
    main()
    

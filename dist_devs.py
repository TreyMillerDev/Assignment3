import os 
import math
from worker import Worker
import threading
from main import clear_directory

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


class Create_workers:

    def __init__(self, main_dev = 'DEV/'):
        
        self.items = os.listdir(main_dev) # gets a list of all the sub-directories 
        self.workers = list([])
        self.lock = threading.Lock()
        # uniques, total_tokens, num_files
        self.counter = Count()


    def create_workers(self):
        """ Breaks the list if sub directories into sections that each crawler will handle , 
            size of sub = 22 sub directory folders """

        dist_factor = math.floor(len(self.items) / 4)
        for x in range(4):
            if x == 3:
                subdir_section = self.items[x*dist_factor: len(self.items)]
                self.workers.append(Worker(x,subdir_section, self.lock, self.counter))
            else:
                subdir_section = self.items[x * dist_factor: (x+1)* dist_factor]
                self.workers.append(Worker(x,subdir_section, self.lock, self.counter))

        for worker in self.workers:
            worker.start()

    def start(self):
        self.create_workers()
        self.join()

    def join(self):
        for worker in self.workers:
            worker.join()



if __name__== "__main__":
    clear_directory(f'alphaJSON/')
    working = Create_workers()
    working.start()

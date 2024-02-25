import os 
import math
from worker import Worker
import threading
from main import clear_directory

class Create_workers:

    def __init__(self, main_dev = 'DEV/'):
        
        self.items = os.listdir(main_dev) # gets a list of all the sub-directories 
        self.workers = list([])
        self.lock = threading.Lock()
        # uniques, total_tokens, num_files
        self.uniques = set()
        self.total_tokens = 0
        self.num_files = 0


    def create_workers(self):
        """ Breaks the list if sub directories into sections that each crawler will handle , 
            size of sub = 22 sub directory folders """

        dist_factor = math.floor(len(self.items) / 4)
        for x in range(4):
            if x == 3:
                subdir_section = self.items[x*dist_factor: len(self.items)]
                self.workers.append(Worker(x,subdir_section, self.lock, self.uniques, self.total_tokens, self.num_files))
            else:
                subdir_section = self.items[x * dist_factor: (x+1)* dist_factor]
                self.workers.append(Worker(x,subdir_section, self.lock, self.uniques, self.total_tokens, self.num_files))

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

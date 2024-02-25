import os 


# thread_count = 4 # 4 workers 

# items = os.listdir('DEV')
# # equal lengths 
# file_in_dir = [] 

# worker_subs = []

# for x in range(thread_count):
#     worker_subs.append([0])
#      # the zero is to keep track of the number of files in the subsection, we will be comparing it often 

# largest = 0
# # print(items)(
# for dir in items:
#     file_in_dir.append((len(os.listdir(f'DEV/{dir}')),dir))

# # for x in range(len(file_in_dir)):
# #     # keep track the subsection with the largest file count, ignoring the list with the largest file count 
# #     if worker_subs[x][0] == largest # check the first index 
def create_paritions(thread_count, directory_path = 'DEV'):
    subs = []
    # print(sorted(file_in_dir))
    for x in range(thread_count):
        subs.append([])
    x = 0
    for root, dirs, files in os.walk(directory_path):
            # Loop through json files in folder
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    subs[x].append(file_path)
                    x += 1

                    if x == thread_count:
                        x = 0
    return subs
    
                
y = create_paritions(8)

for num in y:
    print(num)



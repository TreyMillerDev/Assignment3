import os
import ujson
import time


def file_processor(directory="DEV"):
    # Initialize list to store data from json file
    data_list = []
    num = 0
    # Calculate the time taken to process all json files in the DEV folder
    start = time.time()

    # Loop through folders in DEV folder
    for root, dirs, files in os.walk(directory):
        # Loop through json files in folder
        for file in files:
            if num < 10 and file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as json_file:
                    data = ujson.load(json_file)
                    data_list.append(data)
                    num += 1
    end = time.time()

    # Print the time taken to process all json files in the DEV folder
    print(f"Time taken: {(end-start)*10**3:.03f}ms")

    # Return the list of data from json files
    return data_list

if __name__ == "__main__":

    processed_data = file_processor()
    # processed_data can be used to identify url, content, encoding of each json file.

    #for data in processed_data:
    #   print(f"URL: {data.get('url')}")
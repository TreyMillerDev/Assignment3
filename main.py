import os
import ujson
import time
from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer

#this is the function to process the html files 
#as of right now it grabs the important text BUT DOESNT DO ANYTHING WITH it
#for now its just returning all the text not including the important ones)
#later we might use the important ones for something
def process_html(content):
    soup = BeautifulSoup(content, 'html.parser')

    #find and flag important text
    important_words = set()
    for tag in soup.find_all(['b', 'strong', 'h1', 'h2', 'h3', 'title']):
        important_words.update(tag.get_text().split())

    #then just grab all the text (including important ones)
    all_text = soup.get_text()

    #return tuple of all text and a set of important words
    return all_text, important_words


#Stems and tokenize the text 
def stem_text(text):
    #init a stemmer
    stemmer = PorterStemmer()

    #tokenize and stem
    tokens = nltk.word_tokenize(text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    return ' '.join(stemmed_tokens)

def file_processor(directory="DEV"):
    # Initialize list to store data from json file
    data_list = []
    num = 0
    # Calculate the time taken to process all json files in the DEV folder
    start = time.time()

    #create variables to track the number of files the tokens and the unique tokens
    num_files = 0
    total_tokens = 0
    unique_tokens = set()
    
    # Loop through folders in DEV folder
    for root, dirs, files in os.walk(directory):
        # Loop through json files in folder
        for file in files:
            if num < 1000 and file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as json_file:
                    data = ujson.load(json_file)

                    if 'content' in data and data['content'].startswith('<'):
                        all_text, _ = process_html(data['content'])

                        # Apply stemming to all_text
                        stemmed_text = stem_text(all_text)

                        # Tokenize and update counts
                        tokens = nltk.word_tokenize(stemmed_text)
                        total_tokens += len(tokens)
                        unique_tokens.update(tokens)

                        data_list.append({'url': data['url'], 'stemmed_content': stemmed_text})
                        num_files += 1
                        num += 1

    end = time.time()

    # Calculate metrics
    processing_time = (end - start) * 1000
    avg_doc_length = total_tokens / num_files if num_files > 0 else 0

    # now print the important metrics
    print(f"Processed {num_files} files")
    print(f"Total tokens: {total_tokens}")
    print(f"Unique tokens: {len(unique_tokens)}")
    print(f"Average document length: {avg_doc_length} tokens")
    print(f"Processing time: {processing_time:.03f}ms")

    # Return the list of data from json files
    return data_list

if __name__ == "__main__":
    processed_data = file_processor()
    # Now processed_data contains the url and stemmed content of each HTML file.

    # Example to display processed data
    #for data in processed_data[:3]:  # Display first 3 entries
     #   print(f"URL: {data.get('url')}")
     #   print(f"Stemmed Content: {data.get('stemmed_content')[:100]}...")  # Display first 100 characters

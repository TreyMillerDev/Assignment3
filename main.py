import os
import ujson
import time
from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer

# Ensure NLTK components are downloaded
nltk.download('punkt')

def process_html(content):
    soup = BeautifulSoup(content, 'html.parser')

    # Extract important text with specific tags
    important_text = []
    for tag in soup.find_all(['b', 'strong', 'h1', 'h2', 'h3', 'title']):
        important_text.append(tag.get_text())

    # Combine important text with overall text
    combined_text = ' '.join(important_text) + ' ' + soup.get_text()

    return combined_text

def stem_text(text):
    # Initialize the Porter Stemmer
    stemmer = PorterStemmer()

    # Tokenize and stem the text
    tokens = nltk.word_tokenize(text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    return ' '.join(stemmed_tokens)

def file_processor(directory="DEV"):
    data_list = []
    num = 0
    start = time.time()

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as json_file:
                    data = ujson.load(json_file)

                    # Process only if content is HTML
                    if 'content' in data and data['content'].startswith('<'):
                        # HTML Parsing
                        text = process_html(data['content'])

                        # Stemming
                        stemmed_text = stem_text(text)

                        # Append processed data
                        data_list.append({'url': data['url'], 'stemmed_content': stemmed_text})
                        num += 1

    end = time.time()
    print(f"Time taken: {(end-start)*10**3:.03f}ms")
    return data_list

if __name__ == "__main__":
    processed_data = file_processor()
    # Now processed_data contains the url and stemmed content of each HTML file.

    # Example to display processed data
    for data in processed_data[:3]:  # Display first 3 entries
        print(f"URL: {data.get('url')}")
        print(f"Stemmed Content: {data.get('stemmed_content')[:100]}...")  # Display first 100 characters

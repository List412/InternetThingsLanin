import csv
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from collections import Counter

nltk.download('wordnet')

file_name = 'set.csv'
count = 0
movies_tokenize = []
movies_lemmy = []
movies_token_frequency = []
skip = True
with open(file_name, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if skip:
            skip = False  # skip title
            continue
        split = row[1].split()
        movies_tokenize.append((row[0], split))
        movies_lemmy.append((row[0],  [WordNetLemmatizer().lemmatize(word) for word in split]))
        movies_token_frequency.append((row[0], sorted([Counter(split)], key=lambda x: x[1], reverse=True)))

print(movies_token_frequency)


def computeTF(dict, b):
    result = {}
    count_b = len(b)
    for word, freq in dict.items():
        result[word] = freq/float(count_b)
    return result




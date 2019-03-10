import scipy.spatial
import numpy as np
import csv
import pandas as pd
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import csr_matrix
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

# def cos_distance():


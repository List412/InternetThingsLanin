import math
import re
import collections
from nltk.stem import PorterStemmer
from collections import Counter
from nltk import ngrams
import scipy.spatial
import pandas as pd
import numpy as np
import os.path
from flask import Flask, jsonify, make_response, request, abort, Response
app = Flask(__name__)


def compute_tf(text):
    tf_text = Counter(text)
    for i in tf_text:
        tf_text[i] = tf_text[i] / float(len(text))
    return tf_text


def compute_idf(word, corpus):
    return math.log10(len(corpus) / sum([1.0 for i in corpus if word in i]))


def compute_tf_idf(computed_tf, computed_idf):
    computed_tf_idf = collections.Counter()
    for lemmatized_word in computed_tf.keys():
        computed_tf_idf[lemmatized_word] = computed_tf[lemmatized_word] * computed_idf[lemmatized_word]
    return computed_tf_idf


def read_xlss(file_name, sheet_name, column_name):
    file = pd.ExcelFile(file_name)
    sheet = file.parse(sheet_name)
    data = sheet[column_name]
    return data


def process_data(raw_data, lemmatized_sentences, lemmatized_words):
    porter = PorterStemmer()
    for readSentence in raw_data:
        tokens = filter(None, re.split('\W+', readSentence.lower()))
        sentence = []
        for word in tokens:
            stemmed_word = porter.stem(word).encode('utf-8')
            lemmatized_words.append(str(stemmed_word, 'utf-8'))
            sentence.append(str(stemmed_word, 'utf-8'))
        lemmatized_sentences.append(sentence)


def fill_vectors_array(lemmatized_sentences, base_vector, vectors_array):
    for lemmatized_sentence in lemmatized_sentences:
        vector = dict()
        for item in base_vector.keys():
            vector[item] = 0
        for word in lemmatized_sentence:
            if word in vector:
                vector[word] += 1
        vectors_array.append(vector.values())


@app.route('/chat', methods=['POST'])
def run():
    file_name = "data.xlsx"
    sheet_name = "Sheet1"
    lemmatized_sentences = []
    lemmatized_words = []

    raw_data = read_xlss(file_name, sheet_name, "overview")
    # fill sentences and words from raw data
    process_data(raw_data, lemmatized_sentences, lemmatized_words)

    computed_tf = compute_tf(lemmatized_words)
    lemmatized_words_dictionary_sorted = Counter(sorted(lemmatized_words))

    computed_idf = collections.Counter()

    for lemmatized_word in lemmatized_words_dictionary_sorted.keys():
        computed_idf[lemmatized_word] = compute_idf(lemmatized_word, lemmatized_sentences)

    computed_tf_idf = compute_tf_idf(computed_tf, computed_idf)

    term_freq_dict = Counter(computed_tf_idf)

    Q1, Q2, Q3 = np.percentile(list(term_freq_dict.values()), [25, 50, 80])
    IQR = Q3 - Q1
    lower_inner_fence = Q1 - (1.5 * IQR)
    upper_inner_fence = Q3 + (1.5 * IQR)

    cleaned_dict = dict()
    for tfidfScore in dict(computed_tf_idf).keys():
        if lower_inner_fence <= computed_tf[tfidfScore] <= upper_inner_fence:
            cleaned_dict[tfidfScore] = computed_tf[tfidfScore]

    base_word_vector = dict()
    for key in cleaned_dict.keys():
        base_word_vector[key] = 0

    all_vectors = []
    fill_vectors_array(lemmatized_sentences, base_word_vector, all_vectors)

    data_http = request.get_json()
    message = [data_http['message']]

    lemmatized_message = []
    process_data(message, lemmatized_message, lemmatized_words)

    question_vectors_array = []
    fill_vectors_array(lemmatized_message, base_word_vector, question_vectors_array)

    min_value = 1
    answer = 'не знаю'
    for j, vector in enumerate(all_vectors):
        value = scipy.spatial.distance.cosine(list(question_vectors_array[0]), list(all_vectors[j]))
        if value < min_value:
            min_value = value
            answer = raw_data[j]

    return make_response(jsonify({'message': answer}), 200)


@app.route('/', methods=['GET'])
def main():  # take files from ./static folder
    return app.send_static_file('index.html')

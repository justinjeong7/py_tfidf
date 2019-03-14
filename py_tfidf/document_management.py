import json
import re

class DocManagement:
    """
    manages documents to be searched against and stores summary of documents as TF form
    """

    def __init__(self):
        self.document_count = 0
        self.document_summary = {}


    def __doc_count_increase(self):
        self.document_count += 1

    def get_terms(self, string):
        terms = re.findall(r'\w+', string.lower())

        return terms

    def get_tf(self, string):
        tf = {}
        words = self.get_terms(string)

        term_count = len(words)

        for term in set(words):
            tf[term] = words.count(term) / term_count

        return tf

    def add_document(self, string):

         self.document_summary[self.document_count] = {
            'document': string,
            'type': 'str',
            'tf': self.get_tf(string)
         }

         self.__doc_count_increase()

    def add_document_file(self, filename):

        with open(filename, 'r') as f:
            text = f.read()


        self.document_summary[self.document_count] = {
        'document': filename,
        'type': 'file',
        'tf': self.get_tf(text)
        }

        self.__doc_count_increase()


    def save(self, filename = '.documents.json'):

        with open(filename, 'w') as f:
            json.dump(self.document_summary, f)


    def load(self, filename = '.documents.json'):

        with open(filename, 'r') as f:
            self.document_summary = json.loads(f.read())

        self.document_count = len(self.document_summary)

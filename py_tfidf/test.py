from py_tfidf.document_management import DocManagement
from py_tfidf.tfidf import TFIDF
import unittest
import logging
import re, os

class DocManagementTests(unittest.TestCase):

    def setUp(self):
        self.d = DocManagement()
        self.filename = '.test_docs.json'
        self.test_string = "this is a test"
        self.test_filename = '.test.json'

    def test_get_terms(self):

        result = self.d.get_terms(self.test_string)
        expected = ['this', 'is', 'a', 'test']
        self.assertEqual(result, expected)

    def test_doc_tf(self):

        tf = self.d.get_tf(self.test_string)

        expected = {
            'this': 0.25,
            'is': 0.25,
            'a': 0.25,
            'test': 0.25
        }

        self.assertEqual(tf, expected)

        tf = self.d.get_tf(self.test_string + ' test')

        expected = {
            'this': 0.2,
            'is': 0.2,
            'a': 0.2,
            'test': 0.4
        }
        self.assertEqual(tf, expected)

    def test_add_doc(self):

        self.d.add_document(self.test_string)
        self.assertEqual(self.d.document_count, 1)

    def test_add_file(self):

        self.d.add_document_file('test_document.txt')
        self.assertEqual(self.d.document_count, 1)

    def test_save(self):

        self.d.add_document(self.test_string)
        self.d.add_document_file('test_document.txt')
        self.d.save(filename = self.test_filename)

        self.assertTrue(os.path.exists(self.test_filename))


    def test_load(self):

        self.d.add_document(self.test_string)
        self.d.add_document_file('test_document.txt')
        self.d.save(filename = self.test_filename)

        new_obj = DocManagement()

        new_obj.load(filename = self.test_filename)

        self.assertEqual(new_obj.document_count,2)

    def tearDown(self):

        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)


class TFIDFTests(unittest.TestCase):

    def setUp(self):
        self.tfidf = TFIDF()
        self.filename = '.test_docs.json'
        self.test_string = "this is a test"
        self.test_filename = '.test.json'

        self.tfidf.add_document(self.test_string)
        self.tfidf.add_document_file('test_document.txt')


    def test_idf(self):

        search_term = 'test'
        results = self.tfidf.get_idf(query=search_term)
        self.assertEqual({'test':0.0}, results)

        search_term = 'tdd'
        results = self.tfidf.get_idf(query=search_term)
        self.assertEqual({'tdd':0.6931471805599453}, results)

    def test_simple_search(self):
        search_term = 'tdd'
        results = self.tfidf.search(query=search_term)
        expected = [
        {'document': 'test_document.txt', 'tfidf_score': 0.012836058899258245, 'rank': 1},
        ]
        self.assertEqual(results, expected)

    def test_no_score_limit_search(self):
        search_term = 'tdd'
        results = self.tfidf.search(query=search_term, min_score = 0)
        expected = [
        {'document': 'test_document.txt', 'tfidf_score': 0.012836058899258245, 'rank': 1},
        {'document': 'this is a test', 'rank': 2, 'tfidf_score': 0}
        ]
        self.assertEqual(results, expected)

    def test_limit_result_search(self):
        search_term = 'tdd'
        results = self.tfidf.search(query=search_term, min_score = 0, result_count = 1)
        expected = [
        {'document': 'test_document.txt', 'tfidf_score': 0.012836058899258245, 'rank': 1},
        ]
        self.assertEqual(results, expected)

    def test_search_history_lookup(self):
        search_term = 'tdd'
        _ = self.tfidf.search(query=search_term, min_score = 0, result_count = 1)
        _ = self.tfidf.search(query=search_term, min_score = 0, result_count = 1)
        result = self.tfidf.search(query=search_term, min_score = 0, result_count = 1)

        self.assertEqual(len(self.tfidf.query_history), 1 )

        expected = [
        {'document': 'test_document.txt', 'tfidf_score': 0.012836058899258245, 'rank': 1},
        ]
        self.assertEqual(result, expected)

        _ = self.tfidf.search(query='test', min_score = 0, result_count = 1)
        self.assertEqual(len(self.tfidf.query_history), 2)



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

import math
from document_management import DocManagement

class TFIDF(DocManagement):

    def __init__(self):
        DocManagement.__init__(self)
        self.query = None
        self.query_history = {}


    def search(self, query, result_count = 5, min_score = 0.001):

        self.__set_query(query)

        if query in self.query_history:
            results = self.query_history[query]

        else:
            idf = self.get_idf()
            results = self.__tfidf_score()
            results = sorted(results.items(), key=lambda x: x[1])[::-1]
            self.__store_search_history(results)

        results = self.__limit_result_count(results, result_count, min_score)

        return results

    def __limit_result_count(self, results, result_count, min_score = 0.001):

        output = []
        rank = 1
        for cnt in range(min(result_count,len(results))):

            if results[cnt][1] >= min_score:

                output.append(
                    {
                    'document':self.document_summary[results[cnt][0]]['document'],
                    'tfidf_score': results[cnt][1],
                    'rank': rank
                    }
                )
                rank += 1

        return output

    def __store_search_history(self, results):

        self.query_history[' '.join(self.query)] = results

    def __set_query(self, query):
        self.query = query.split(' ')

    def get_idf(self, query = None):

        if query:
            self.__set_query(query)

        idf = {}

        for word in self.query:
            count = 0

            for _, v in self.document_summary.items():
                if word in v['tf']:
                    count += 1

            if count ==0:
                idf[word] = 0
            else:
                idf[word] = math.log(self.document_count / count)

        self.idf = idf

        return self.idf

    def __tfidf_score(self):

        results = {}

        for n, doc in self.document_summary.items():
            score = 0
            for word in self.query:
                if word in doc['tf']:
                    score += doc['tf'][word] * self.idf[word]

            results[n] = score

        return results

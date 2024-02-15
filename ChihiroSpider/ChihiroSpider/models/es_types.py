from elasticsearch_dsl import Document, Text, Completion, Keyword
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from typing import Dict

connections.create_connection(hosts="http://elasticsearch:9200")


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self) -> Dict:
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class ArticleType(Document):
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer='ik_max_word')
    url = Keyword()
    content = Text(analyzer='ik_max_word')
    author = Text(analyzer='ik_max_word')
    #
    # def clean(self):
    #     """
    #     Automatically construct the suggestion input and weight by taking all
    #     possible permutation of Person's name as ``input`` and taking their
    #     popularity as ``weight``.
    #     """
    #     self.suggest = {
    #         'input': [' '.join(p) for p in permutations(self.name.split())],
    #         'weight': self.popularity
    #     }

    class Index:
        name = 'chihiro'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }


class QuotesType(Document):
    suggest = Completion(analyzer=ik_analyzer)
    url = Keyword()
    text = Text(analyzer='ik_max_word')
    author = Text(analyzer='ik_max_word')
    #
    # def clean(self):
    #     """
    #     Automatically construct the suggestion input and weight by taking all
    #     possible permutation of Person's name as ``input`` and taking their
    #     popularity as ``weight``.
    #     """
    #     self.suggest = {
    #         'input': [' '.join(p) for p in permutations(self.name.split())],
    #         'weight': self.popularity
    #     }

    class Index:
        name = 'quotes'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }


if __name__ == "__main__":
    ArticleType.init()
    QuotesType.init()

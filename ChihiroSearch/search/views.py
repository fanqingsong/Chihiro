import json
from django.shortcuts import render
from django.views.generic.base import View
from .models import ArticleType, QuotesType
from django.http import HttpResponse, HttpRequest
from elasticsearch import Elasticsearch
from datetime import datetime
from typing import List

client = Elasticsearch([
    {'host': 'elasticsearch', 'port': 9200},
])


# Create your views here.
class SearchSuggest(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        key_words = request.GET.get('s', '')
        re_datas: List[str] = []
        if key_words:
            s = QuotesType.search()
            s = s.suggest('my_suggest', key_words, completion={
                "field": "suggest", "fuzzy": {
                    "fuzziness": 2
                },
                "size": 10
            })
            suggestions = s.execute_suggest()
            for match in suggestions.my_suggest[0].options:
                source = match._source
                re_datas.append(source["title"])
        return HttpResponse(json.dumps(re_datas), content_type="application/json")


class SearchView(View):
    def get(self, request: HttpRequest) -> render:
        key_words = request.GET.get('q', '')
        page = request.GET.get('p', '')
        try:
            page = int(page)
        except:
            page = 1

        start_time: datetime = datetime.now()
        response = client.search(
            index="quotes",
            body={
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["author", "text"]
                    }
                },
                "from": (page-1) * 10,
                "size": 10,
                "highlight": {
                    "pre_tags": ['<span class="keyWord">'],
                    "post_tags": ['</span>'],
                    "fields": {
                        "author": {},
                        "text": {},
                    }
                }
            }
        )
        end_time: datetime = datetime.now()
        last_seconds: float = (end_time - start_time).total_seconds()
        total_nums = response["hits"]["total"]
        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            # if "title" in hit["highlight"]:
            #     hit_dict["title"] = "".join(hit["highlight"]["title"])
            # else:
            #     hit_dict["title"] = hit["_source"]["title"]
            if "text" in hit["highlight"]:
                hit_dict["text"] = "".join(hit["highlight"]["text"][:100])
            else:
                hit_dict["text"] = hit["_source"]["text"][:100]
            hit_dict["url"] = hit["_source"]["url"]
            hit_dict["author"] = hit["_source"]["author"]
            hit_dict["score"] = hit["_score"]
            hit_list.append(hit_dict)

        return render(request, "result.html",
                      {"all_hits": hit_list,
                       "key_words": key_words,
                       "page": page,
                       "total_nums": total_nums,
                       "last_seconds": last_seconds})
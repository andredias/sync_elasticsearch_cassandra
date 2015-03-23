#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from elasticsearch import Elasticsearch
from datetime import datetime
from uuid import UUID, uuid4

es = Elasticsearch()

index = 'desafio'
doc_type = 'simbiose'
dateformat = '%Y-%m-%d %H:%M:%S.%f'


def insert_update(document, id=None):
    document.setdefault('timestamp', datetime.now())
    id = id or uuid4()
    es.index(index=index, doc_type=doc_type, id=id, body=document)
    return id


def get(id):
    '''
    Obtém registro a partir do id.

    Não é necessário para a aplicação,
    mas sim para os testes
    '''
    return es.get_source(index=index, doc_type=doc_type, id=id)


def search(from_timestamp):
    query = {
        "query": {
            "filtered": {
                "query": {
                    "match_all": {}
                },
                "filter": {
                    "range": {
                        "timestamp": {"from": from_timestamp}
                    }
                }
            }
        }
    }
    date_format = lambda x: '%Y-%m-%dT%H:%M:%S' if len(x) < 20 else '%Y-%m-%dT%H:%M:%S.%f'
    return {UUID(hit['_id']):
            {'mensagem': hit['_source']['mensagem'],
             'timestamp': datetime.strptime(hit['_source']['timestamp'],
                                            date_format(hit['_source']['timestamp']))}
            for hit in es.search(index=index, doc_type=doc_type, body=query)['hits']['hits']}

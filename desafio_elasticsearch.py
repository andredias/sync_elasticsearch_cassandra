#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from elasticsearch import Elasticsearch
from datetime import datetime
from uuid import uuid4

es = Elasticsearch()

index = 'desafio_simbiose'
doc_type = 'mensagem'


def insert(document, id=None):
    document.setdefault('timestamp', datetime.now())
    id = id or uuid4()
    es.index(index=index, doc_type=doc_type, id=id, body=document)
    return id


def update(document, id, timestamp=None):
    return insert(document, id, timestamp)


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

    return {hit['_id']: hit['_source']
            for hit in es.search(index=index, doc_type=doc_type, body=query)['hits']['hits']}

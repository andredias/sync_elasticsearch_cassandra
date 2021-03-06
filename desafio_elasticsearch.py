#!/usr/bin/env python

from elasticsearch import Elasticsearch
from datetime import datetime
from uuid import UUID, uuid4

es = None

index = 'desafio'
doc_type = 'simbiose'
dateformat = '%Y-%m-%d %H:%M:%S.%f'


def connect(index_=None, doc_type_=None):
    global es
    global index
    global doc_type
    index = index_ or index
    doc_type = doc_type_ or doc_type
    es = Elasticsearch()


def drop(index=index):
    es.indices.delete(index=index)


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
    try:
        return es.get_source(index=index, doc_type=doc_type, id=id)
    except:
        return {}


def search(from_timestamp):
    query = {
        "query": {
            "filtered": {
                "query": {
                    "match_all": {}
                },
                "filter": {
                    "range": {
                        "timestamp": {"gt": from_timestamp}
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

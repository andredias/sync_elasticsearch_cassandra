#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import desafio_elasticsearch as de


def setup():
    de.index = 'teste'
    de.doc_type = 'elasticsearch'


def teardown():
    de.es.indices.delete(index=de.index)


def test_insert():
    doc = {'mensagem': 'Olá mundo'}
    id = de.insert(doc)
    assert de.get(id)


def test_search():
    doc1 = {'mensagem': 'Parabéns, André', 'timestamp': datetime(1973, 2, 12)}
    id1 = de.insert(doc1)
    doc2 = {'mensagem': '42 anos', 'timestamp': datetime(2015, 2, 12)}
    id2 = de.insert(doc2)
    # bizarro, mas o teste não passa sem o sleep(1) abaixo!
    from time import sleep
    sleep(1)
    s = de.search(from_timestamp=datetime(2014, 1, 1))
    assert str(id2) in s and str(id1) not in s

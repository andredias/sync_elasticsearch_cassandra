#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import desafio_cassandra as dc


def setup():
    dc.connect(keyspace='teste', tablename='simbiose')


def teardown():
    dc.drop('teste')


def test_insert():
    doc = {'mensagem': 'Olá mundo'}
    id = dc.insert_update(doc)
    assert dc.get(id)


def test_update():
    doc = {'mensagem': 'test_update'}
    id = dc.insert_update(doc)
    doc['mensagem'] = 'Mudei'
    dc.insert_update(doc, id=id)
    doc2 = dc.get(id)
    assert doc['mensagem'] == doc2['mensagem']


def test_search():
    doc1 = {'mensagem': 'Parabéns, André', 'timestamp': datetime(1973, 2, 12)}
    id1 = dc.insert_update(doc1)
    doc2 = {'mensagem': '42 anos', 'timestamp': datetime(2015, 2, 12)}
    id2 = dc.insert_update(doc2)
    s = dc.search(from_timestamp=datetime(2014, 1, 1))
    assert id2 in s and id1 not in s

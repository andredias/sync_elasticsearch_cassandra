#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import desafio_elasticsearch as de


def setup():
    de.connect('teste', 'elasticsearch')


def teardown():
    de.drop('teste')


def test_insert():
    doc = {'mensagem': 'Olá mundo'}
    id = de.insert_update(doc)
    assert de.get(id)


def test_update():
    doc = {'mensagem': 'Olá mundo'}
    id = de.insert_update(doc)
    doc['mensagem'] = 'Mudei'
    de.insert_update(doc, id=id)
    doc2 = de.get(id)
    assert doc['mensagem'] == doc2['mensagem']


def test_search():
    doc1 = {'mensagem': 'Parabéns, André', 'timestamp': datetime(1973, 2, 12)}
    id1 = de.insert_update(doc1)
    doc2 = {'mensagem': '42 anos', 'timestamp': datetime(2015, 2, 12)}
    id2 = de.insert_update(doc2)
    # bizarro, mas o teste não passa sem o sleep(1) abaixo!
    from time import sleep
    sleep(1)
    s = de.search(from_timestamp=datetime(2014, 1, 1))
    assert id2 in s and id1 not in s

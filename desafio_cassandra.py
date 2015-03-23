#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
referência: http://planetcassandra.org/getting-started-with-cassandra-and-python/
'''

from __future__ import unicode_literals, print_function
from cassandra.cluster import Cluster
from datetime import datetime
from uuid import uuid4


keyspace = 'desafio'
tablename = 'simbiose'
session = None


def connect(keyspace_=None, tablename_=None):
    global session
    global keyspace
    global tablename
    keyspace = keyspace_ or keyspace
    tablename = tablename_ or tablename
    cluster = Cluster()
    session = cluster.connect()
    result = session.execute('select * from system.schema_keyspaces where keyspace_name=%s', (keyspace, ))
    if not result:
        session.execute("create keyspace if not exists %s with replication = {'class':'SimpleStrategy', "
                        "'replication_factor':1}" % keyspace)
        session.execute('''create table {0}.{1} (
            id uuid,
            mensagem text,
            timestamp timestamp,
            primary key (id, timestamp)
    )'''.format(keyspace, tablename))
    session.set_keyspace(keyspace)
    return


def drop(keyspace=keyspace):
    session.execute('drop keyspace ' + keyspace)
    return


def insert_update(document, id=None):
    document.setdefault('timestamp', datetime.now())
    id = id or uuid4()
    query = 'insert into {} (id, mensagem, timestamp) values (%s, %s, %s)'.format(tablename)
    session.execute(query, (id, document['mensagem'], document['timestamp']))
    return id


def get(id):
    query = 'select id, mensagem, timestamp from {} where id = %s allow filtering'.format(tablename)
    try:
        rows = session.execute(query, (id, ))
        return {'mensagem': rows[0].mensagem, 'timestamp': rows[0].timestamp}
    except:
        return {}


def search(from_timestamp):
    query = 'select id, mensagem, timestamp from {} where timestamp > %s ' \
            'allow filtering'.format(tablename)
    result = session.execute(query, (from_timestamp, ))
    return {id: {'mensagem': mensagem, 'timestamp': timestamp}
            for (id, mensagem, timestamp) in result}

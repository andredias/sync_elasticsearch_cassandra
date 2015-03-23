#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
import daemon
import random
import desafio_cassandra as dc
import desafio_elasticsearch as de
from uuid import uuid4
from time import sleep
from syslog import syslog


ids = [uuid4() for i in range(5)]
destinos = (dc, de)
with open('especificacao.rst', 'r') as f:
    especificacao = [linha.strip() for linha in f.readlines() if linha.strip()]


def lerolero():
    return {'mensagem': random.choice(especificacao)}


def generate():
    id = random.choice(ids)
    doc = lerolero()
    dest = random.choice(destinos)
    dest.insert_update(doc, id)
    dest_name = 'cassandra' if dest == dc else 'elasticsearch'
    syslog('dest: %s, id: %s, timestamp: %s, mensagem: %s' %
           (dest_name, id, doc['timestamp'], doc['mensagem']))


def main(intervalo):
    with daemon.DaemonContext():
        dc.connect()
        de.connect()
        syslog('pid: %s' % os.getpid())
        while True:
            generate()
            sleep(intervalo)


if __name__ == '__main__':
    intervalo = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    main(intervalo)

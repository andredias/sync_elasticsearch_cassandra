#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
referências:
    * https://www.python.org/dev/peps/pep-3143/
    * http://stackoverflow.com/questions/4637420/efficient-python-daemon
'''

from __future__ import unicode_literals

import os
import signal
import daemon
import time
import desafio_cassandra as dc
import desafio_elasticsearch as de
from syslog import syslog
from os.path import isfile
from datetime import datetime

intervalo = 5
config_filename = '/tmp/config.txt'


def load_configuration(signum, frame):
    '''
    Tenta carregar novo intervalo de sincronização a partir do arquivo de configuração.
    Essa rotina é disparada pelo sinal SIGUSR1 enviado ao daemon
    '''

    global intervalo
    if isfile(config_filename):
        with open(config_filename, 'r') as f:
            linha = f.readline().strip()
        try:
            intervalo = float(linha)
        except ValueError:
            syslog('Erro na conversão do intervalo')
    else:
        syslog('Arquivo %s não encontrado' % config_filename)
    syslog('intervalo = %ss' % intervalo)
    return


class Sincronizador(object):

    def __init__(self, config_filename=None):
        self.from_timestamp = datetime.now()
        de.connect()
        dc.connect()

    def run(self):
        '''
        Realiza a sincronização das duas bases de dados.

        Usa operações de conjuntos baseados nos ids de cada documento para
        determinar quais os comuns e os que devem ser transferidos para a outra base de dados.
        '''

        syslog('Início da sincronização: ' + str(self.from_timestamp))
        doc_cassandra = dc.search(self.from_timestamp)
        doc_elasticsearch = de.search(self.from_timestamp)
        # maior timestamp será referência da próxima busca
        timestamps = {doc['timestamp'] for doc in doc_cassandra.values()}
        timestamps.update({doc['timestamp'] for doc in doc_elasticsearch.values()})
        timestamps.add(self.from_timestamp)  # garante que há pelo menos um
        self.from_timestamp = max(timestamps)
        syslog('maior timestamp: ' + str(self.from_timestamp))
        # conjuntos com ids mais recentes de cada base de dados
        cassandra_set = {id for id in doc_cassandra.keys()}
        elasticsearch_set = {id for id in doc_elasticsearch.keys()}
        cassandra_to_elastic = cassandra_set - elasticsearch_set
        elastic_to_cassandra = elasticsearch_set - cassandra_set
        comum = cassandra_set & elasticsearch_set
        for id in comum:
            timestamp_cassandra = doc_cassandra[id]['timestamp']
            timestamp_elasticsearch = doc_elasticsearch[id]['timestamp']
            syslog('comum: ' + str(id))
            syslog('    cassandra:     ' + str(timestamp_cassandra))
            syslog('    elasticsearch: ' + str(timestamp_elasticsearch))
            if timestamp_cassandra > timestamp_elasticsearch:
                cassandra_to_elastic.add(id)
                syslog('    cassandra > elasticsearch')
            else:
                elastic_to_cassandra.add(id)
                syslog('    elasticsearch > cassandra')
        # sincronização propriamente dita
        for id in cassandra_to_elastic:
            syslog('cassandra > elasticsearch: ' + str(id))
            de.insert_update(doc_cassandra[id], id)
        for id in elastic_to_cassandra:
            syslog('elasticsearch > cassandra: ' + str(id))
            dc.insert_update(doc_elasticsearch[id], id)
        syslog('Fim da sincronização')
        return cassandra_to_elastic, elastic_to_cassandra  # para fins de teste


def main():
    context = daemon.DaemonContext()
    context.signal_map = {
        signal.SIGUSR1: load_configuration,
    }
    with context:
        sinc = Sincronizador()
        syslog('pid: %s' % os.getpid())
        while True:
            sinc.run()
            time.sleep(intervalo)


if __name__ == "__main__":
    print('''Aplicação está rodando como daemon...

Para mudar o intervalo de execução:
1. crie um arquivo %s com o intervalo desejado (em segundos). Ex.: 0.7
2. envie um sinal SIGUSR1 ao processo para recarregar as configurações
3. Confirme o recarregamento em /var/log/syslog
''' % config_filename)
    main()

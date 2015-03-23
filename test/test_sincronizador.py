#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gerador_lero_lero import generate
from app import Sincronizador, dc, de
from uuid import uuid4
from time import sleep
from datetime import datetime


class TestSincronizador(object):
    '''
    Variáveis usadas nos testes

    c2e: documentos que vão do cassandra para o elasticsearch
    e2c: inverso
    '''

    def __init__(self):
        self.sincronizador = Sincronizador()
        self.ids = [uuid4() for i in range(2)]

    def setup(self):
        self.sincronizador.from_timestamp = datetime.now()
        sleep(0.1)

    def test_sem_registros(self):
        c2e, e2c = self.sincronizador.run()
        assert len(c2e) == len(e2c) == 0

    def test_c2e(self):
        id1 = generate(dest=dc)
        c2e, e2c = self.sincronizador.run()
        assert id1 in c2e
        assert len(e2c) == 0

    def test_e2c(self):
        id1 = generate(dest=de)
        sleep(1)  # outro erro bizarro. Sem o sleep não funciona
        c2e, e2c = self.sincronizador.run()
        assert len(c2e) == 0
        assert id1 in e2c

    def test_um_para_cada_lado(self):
        ide = generate(id=self.ids[0], dest=de)
        sleep(1)  # outro erro bizarro. Sem o sleep não funciona
        idc = generate(id=self.ids[1], dest=dc)
        c2e, e2c = self.sincronizador.run()
        assert len(c2e) == 1
        assert len(e2c) == 1
        assert ide in e2c
        assert idc in c2e

    def test_mais_recente_cassandra(self):
        id = generate(id=self.ids[0], dest=de)
        sleep(0.5)
        generate(id=self.ids[0], dest=dc)
        c2e, e2c = self.sincronizador.run()
        assert len(c2e) == 1
        assert len(e2c) == 0
        assert id in c2e

    def test_mais_recente_elasticsearch(self):
        id = generate(id=self.ids[0], dest=dc)
        sleep(0.1)
        generate(id=self.ids[0], dest=de)
        sleep(1)  # outro erro bizarro. Sem o sleep não funciona
        c2e, e2c = self.sincronizador.run()
        assert len(c2e) == 0
        assert len(e2c) == 1
        assert id in e2c

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gerador_lero_lero import generate, connect, dc, de


def setup():
    connect('teste', 'simbiose')


def test_generate():
    id = generate()
    assert de.get(id) or dc.get(id)

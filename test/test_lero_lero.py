#!/usr/bin/env python

from gerador_lero_lero import generate, connect, dc, de


def setup():
    connect('teste', 'simbiose')


def test_generate():
    id = generate()
    assert de.get(id) or dc.get(id)

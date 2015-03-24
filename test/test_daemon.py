#!/usr/bin/env python

import sh
from os.path import abspath, dirname, join
from nose.tools import nottest


def get_pid(name):
    pid = sh.grep(sh.ps('ax'), name, _ok_code=range(3))
    return pid and int(pid.split()[0])


@nottest
def test_app():
    '''
    pid não é obtido corretamente quando o teste é executado,
    mas funciona durante depuração
    '''
    app_filename = abspath(join(dirname(__file__), '../app.py'))
    sh.env('python', app_filename, _bg=True)
    pid = get_pid(app_filename)
    assert pid
    sh.kill('-s', 'SIGUSR1', pid)
    assert get_pid(app_filename)
    sh.kill(pid)
    assert not get_pid(app_filename)


@nottest
def test_gerador_lero_lero():
    '''
    idem ao teste anterior
    '''
    gerador_filename = abspath(join(dirname(__file__), '../gerador_lero_lero.py'))
    sh.env('python', gerador_filename, _bg=True)
    pid = get_pid(gerador_filename)
    assert pid
    sh.kill(pid)
    assert not get_pid(gerador_filename)

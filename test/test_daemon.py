#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sh
from time import sleep
from os.path import isfile, abspath, dirname, join
from nose.tools import nottest

default_interval = 0.1
config_filename = '/tmp/config.txt'
output_filename = '/tmp/current_time.txt'
app_filename = abspath(join(dirname(__file__), '../app.py'))


def get_pid():
    pid = str(sh.grep(sh.tail('-n', '40', '/var/log/syslog'), '/app.py: pid:')).split()[-1]
    return int(pid.split()[-1])


def set_interval(interval):
    with open(config_filename, 'w') as f:
        f.write(str(interval))
    return


def setup():
    if isfile(output_filename):
        os.remove(output_filename)
    set_interval(default_interval)
    out = sh.env('python', app_filename)
    assert len(out) > 0
    return


def teardown():
    pid = get_pid()
    sh.kill(pid)
    return


@nottest
class TestDaemon(object):

    def test_launch(self):
        assert isfile(output_filename)
        os.remove(output_filename)
        sleep(default_interval * 3)
        assert isfile(output_filename)

    def test_reload(self):
        set_interval(1)
        pid = get_pid()
        sh.kill('-s', 'SIGUSR1', pid)  # reload
        log = str(sh.grep(sh.tail('/var/log/syslog'), 'app.py: intervalo = 1.0s'))
        assert len(log) > 0

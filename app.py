'''
referências:
    * https://www.python.org/dev/peps/pep-3143/
    * http://stackoverflow.com/questions/4637420/efficient-python-daemon
'''

import signal
import daemon
import time


def initial_program_setup():
    pass


def do_main_program():
    while True:
        with open("/tmp/current_time.txt", "w") as f:
            f.write("The time is now " + time.ctime())
        time.sleep(5)


def program_cleanup():
    pass


def reload_program_config(signum, frame):
    with open("/tmp/reload.txt", "w") as f:
        f.write("The time is now " + time.ctime())
    return None


def run():
    context = daemon.DaemonContext()
    context.signal_map = {
        signal.SIGTERM: program_cleanup,
        signal.SIGHUP: 'terminate',
        signal.SIGUSR1: reload_program_config,
    }
    initial_program_setup()
    with context:
        do_main_program()


if __name__ == "__main__":
    run()

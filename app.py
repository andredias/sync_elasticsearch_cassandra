'''
referências:
    * https://www.python.org/dev/peps/pep-3143/
    * http://stackoverflow.com/questions/4637420/efficient-python-daemon
'''

import signal
import daemon
import time
import syslog
from os.path import isfile

intervalo = 5  # segundos
config_filename = '/tmp/config.txt'


def load_configuration():
    global intervalo
    if isfile(config_filename):
        with open(config_filename, 'r') as f:
            linha = f.readline().strip()
        try:
            intervalo = float(linha)
        except ValueError:
            syslog.syslog('Erro na conversão do intervalo')
    else:
        syslog.syslog('Arquivo %s não encontrado' % config_filename)
    syslog.syslog('intervalo = %ss' % intervalo)
    return


def reload_configuration(signum, frame):
    load_configuration()
    return


def run():
    while True:
        with open("/tmp/current_time.txt", "w") as f:
            f.write("The time is now " + time.ctime())
        time.sleep(intervalo)


def main():
    context = daemon.DaemonContext()
    context.signal_map = {
        signal.SIGUSR1: reload_configuration,
    }
    load_configuration()
    with context:
        run()


if __name__ == "__main__":
    print('''Aplicação está rodando como daemon...

Para mudar o intervalo de execução:
1. crie um arquivo %s com o intervalo desejado (em segundos). Ex.: 0.7
2. envie um sinal SIGUSR1 ao processo para recarregar as configurações
3. Confirme o recarregamento em /var/log/syslog
''' % config_filename)
    main()

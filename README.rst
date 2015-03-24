Sincronização entre ElasticSearch e Cassandra
=============================================

Este projeto é uma solução para o desafio técnico proposto pela
`Simbiose <http://www.simbioseventures.com.br/>`_,
conforme `anúncio publicado na lista o Python-Brasil <https://groups.google.com/forum/#!topic/python-brasil/f7DpZRB4VbM>`_,
cuja especificação se encontra no arquivo :code:`especificacao.rst`
localizado neste mesmo diretório.


Autor
-----

André Felipe Dias <andre.dias@pronus.io>


Pré-Requisitos
--------------

* Python 3.4
* Acesso ao Cassandra via :code:`localhost:9042`
* Acesso ao Elasticsearch via :code:`localhost:9200`


.. tip::

    Uma ótima alternativa é o uso de containers do Docker:

    .. code-block:: bash

        $ docker pull elasticsearch
        $ docker run --name elasticsearch -p 9200:9200 -d elasticsearch

        $ docker pull spotify/cassandra
        $ docker run --name cassandra -p 9042:9042 -d spotify/cassandra


Os demais pré-requisitos do projeto devem ser instalados via :code:`pip`:

.. code-block:: bash

    $ pip install -r requirements.txt


Execução
--------

.. code-block:: bash

    $ python app.py                 # daemon do sincronizador
    $ python gerador_lero_lero.py   # daemon do gerador de dados aleatórios
    $ tail -f /var/log/syslog       # para acompanhar o processamento


A configuração do intervalo de sincronização pode ser feita através do arquivo
:code:`/tmp/config.txt`.
Para que essa configuração seja carregada,
é necessário enviar um sinal :code:`SIGUSR1` ao daemon do sincronizador.
Exemplo:

.. code-block:: bash

    $ echo 3 > /tmp/config.txt
    $ pid=$(ps ax | grep 'python app.py' | head -n 1 | cut -f 1 -d ' ')
    $ kill -s SIGUSR1 $pid


Testes
------

Algumas instalações adicionais são necessárias para os testes:

.. code-block:: bash

    $ pip install nose sh


A execução dos testes automatizados:

.. code-block:: bash

    $ nosetests


Depuração
---------

A listagem abaixo mostra um exemplo de depuração das principais partes do projeto:

.. code-block:: pycon

    >>> from app import Sincronizador
    >>> s = Sincronizador()
    >>> from gerador_lero_lero import generate
    >>> generate()
    >>> generate()
    >>> generate()
    >>> s.run()
    >>> generate()
    >>> generate()
    >>> s.run()
    >>>

Acompanhe a saída do processamento através do comando:

.. code-block:: bash

    $ tail -f /var/log/syslog

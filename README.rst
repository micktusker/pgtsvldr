pgtsvldr
=========

*A command line tool for loading TSV files into a PostgreSQL table.*


Purpose
-------

Given a TSV file and a PostgreSQL URL for connection, load the TSV file into a table called *tsv_rows" in the public
schema.

This table is dropped and re-created each time the program is run.

Usage
-----

If you've cloned this project, and want to install the library (*and all
development dependencies*), the command you'll want to run is::

    $ pip install -e .[test]

If you'd like to run all tests for this project (*assuming you've written
some*), you would run the following command::

    $ python setup.py test

This will trigger `py.test <http://pytest.org/latest/>`_, along with its popular
`coverage <https://pypi.python.org/pypi/pytest-cov>`_ plugin.


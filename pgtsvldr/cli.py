"""
Load Postgres.
Usage:
  pgtsvldr tsvldr <tsv_file> <pg_host> <pg_port> <pg_user> <pg_dbname>
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import pgtsvldr.commands
    options = docopt(__doc__, version=VERSION)
    # print(options)
    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
        if hasattr(pgtsvldr.commands, k) and v:
            module = getattr(pgtsvldr.commands, k)
            pgtsvldr.commands = getmembers(module, isclass)
            command = [command[1] for command in pgtsvldr.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()

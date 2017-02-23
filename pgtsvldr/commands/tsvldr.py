
import psycopg2
from .base import Base
from datetime import datetime
import os.path

class TsvLdr(Base):
    """
    Loads the TSV data from the given file to PostgreSQL.
    """
    def _get_pg_connection(self, pg_host, pg_port, pg_user, pg_dbname):
        '''
        Return a PostgreSQL connection for the given parameters.
        Assumes presence and validity of ~/.pgpass.
        '''
        pg_connection = psycopg2.connect("dbname=%s user=%s host=%s port=%d" % (pg_dbname, pg_user, pg_host, pg_port))
        return pg_connection

    def _prepare_table(self, pg_connection):
        '''
        Drop and recreate the target table named "tsv_rows" in the schema "public".
        '''
        today = datetime.today().strftime('%Y-%m-%d')
        cur = pg_connection.cursor()
        cur.execute('DROP TABLE IF EXISTS tsv_rows')
        cur.execute('CREATE UNLOGGED TABLE tsv_rows(data_row TEXT)')
        cur.execute("COMMENT ON TABLE tsv_rows IS 'Transit table for TSV data. Created %s.'" % (today,))
        cur.close()

    def _load_data(self, tsv_file, pg_connection):
        '''
	    Takes the given TSV file and loads all the rows it contains into the table "tsv_rows"
	    in the public schema of the target PostgreSQL database.
	    '''
        line_row_count = 0
        cur = pg_connection.cursor()
        with open(tsv_file, 'rt') as fh:
            for line in fh:
                cur.execute('INSERT INTO tsv_rows(data_row) VALUES(%s)', (line,))
                line_row_count += 1
        cur.close()
        return line_row_count

    def run(self):
        '''
        The method that executes the shell command pgtsvldr tsvldr ...
        '''
        file_to_load = self.options['<tsv_file>']
        if not os.path.isfile(file_to_load):
            raise FileNotFoundError \
                ('The given file "%s" does not exist, check the file name and path!' % (file_to_load,))
        pg_host = self.options['<pg_host>']
        pg_port = int(self.options['<pg_port>'])
        pg_user = self.options['<pg_user>']
        pg_dbname = self.options['<pg_dbname>']
        pg_connection = self._get_pg_connection(pg_host, pg_port, pg_user, pg_dbname)
        self._prepare_table(pg_connection)
        line_row_count = self._load_data(file_to_load, pg_connection)
        pg_connection.commit()
        pg_connection.close()
        print("The loaded row count is %d" % (line_row_count,))


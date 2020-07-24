
import psycopg2
import psycopg2.extras
hostname = 'localhost'
username = 'niravkapoor'
password = 'password'
database = 'fruit'

class DataBase:
    # Simple routine to run a query on a database and print the results:
    def findAll( self, query ):
        print("query", query)
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database, port=5432 )
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute( query )
        r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
        # result = cur.fetchall()
        conn.close()
        # cur.connection.close()
        return r
    
    def find( self, query ):
        print("query", query)
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database, port=5432 )
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute( query )
        result = cur.fetchone()[0]
        conn.close()
        return result

    def insert( self, query ):
        print("query", query)
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database, port=5432 )
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute( query )
        count = cursor.rowcount
        conn.close()
        return count
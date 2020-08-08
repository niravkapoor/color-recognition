
import psycopg2
import psycopg2.extras
hostname = 'localhost'
username = 'niravkapoor'
password = '123456789'
database = 'test'
port = 5432

class DataBase:
    def findAll( self, query ):
        print("query", query)
        try:
            conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database, port=port )
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute( query )
            data = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
            conn.close()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                cur.close()
                conn.close()
    
    def find( self, query ):
        print("query", query)
        try:
            conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database, port=port )
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute( query )
            result = cur.fetchone()[0]
            conn.close()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                cur.close()
                conn.close()

    def insert( self, query ):
        print("query", query)
        data = None
        try:
            conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database, port=port )
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute( query )
            data = cur.fetchone()[0]
            print(data)
            conn.commit()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                cur.close()
                conn.close()
        
    
    def update( self, query ):
        print("query", query)
        data = None
        try:
            conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database, port=port )
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute( query )
            data = cur.fetchone()[0]
            conn.commit()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                cur.close()
                conn.close()
import psycopg2

"""
    File name: aa_global_database_function.py
    Description: This file contains functions to interact with a postgres database
"""

##################
# Class          #
##################

class Postgres_db:

    ##################
    # 0 - constructor 
    ##################

    def __init__(self, host, dbname, user, password, port):
        try:
            self.connection = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
            self.cursor = self.connection.cursor()
        except Exception as e:
            return e


    ##################
    # 1 - functions - verification
    ##################

    def check_table_exists(self, table_name):
        try:
            self.cursor.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", (table_name,))
            return self.cursor.fetchone()[0]
        except Exception as e:
            return e


    ##################
    # 2 - functions - creation
    ##################

    def create_table(self, table_name, columns):
        try:
            if self.check_table_exists(table_name):
                print("Table %s already exists" % (table_name))
                return False
            else :
                self.cursor.execute("CREATE TABLE IF NOT EXISTS %s (%s)" % (table_name, columns))
                self.connection.commit()
                print("Table %s created successfully" % (table_name))
                return True
        except Exception as e:
            return e


    ##################
    # 3 - functions - insertion
    ##################

    def insert_row(self, table_name, columns, values):
        try:
            self.cursor.execute("INSERT INTO %s (%s) VALUES (%s)" % (table_name, columns, values))
            self.connection.commit()
            return True
        except Exception as e:
            return e


    ##################
    # 4 - functions - selection
    ##################

    def select_rows(self, table_name, columns = "*", condition = None):
        try:
            if condition is None:
                self.cursor.execute("SELECT %s FROM %s" % (columns, table_name))
            else:
                self.cursor.execute("SELECT %s FROM %s WHERE %s" % (columns, table_name, condition))
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            return e


    ##################
    # 5 - functions - update
    ##################

    def update_row(self, table_name, update, condition):
        try:
            self.cursor.execute("UPDATE %s SET %s WHERE %s" % (table_name, update, condition))
            self.connection.commit()
            return True
        except Exception as e:
            return e

        
    ##################
    # 6 - functions - delete
    ##################

    def delete_table(self, table_name):
        try:
            if(self.check_table_exists(table_name)):
                self.cursor.execute("DROP TABLE %s CASCADE" % table_name)
                self.connection.commit()
                return True
            else:
                return False
        except Exception as e:
            return e

    def delete_row(self, table_name, condition):
        try:
            self.cursor.execute("DELETE FROM %s WHERE %s" % (table_name, condition))
            self.connection.commit()
            return True
        except Exception as e:
            return e
        

    ##################
    # 7 - functions - other
    ##################

    def reset_table(self, table_name):
        try:
            self.cursor.execute("TRUNCATE TABLE %s CASCADE" % table_name)
            self.connection.commit()
            return True
        except Exception as e:
            return e

    def close_connection(self):
        try:
            self.connection.close()
            return True
        except Exception as e:
            return e

        

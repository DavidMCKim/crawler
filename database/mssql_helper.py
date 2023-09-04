import mysql.connector

class MSSQLConnector() :
    def __init__(self) -> None:
        try:
            self.db = mysql.connector.connect(
                    host='host',
                    user='id',
                    port='portnumber',
                    password="pw",
                    database="dbname",
                    autocommit=True                
            )
            self.cursor = self.db.cursor()
        except Exception as e:
            print(e)

    def select(self, query) :
        result = None
        try :
            self.cursor.execute(query)
            res = self.cursor.fetchall()

            result = []
            for r in res :
                result.append(list(r))

        except:
            pass
        return result

    def insert(self, query) :
        result = -1
        try :
            self.cursor.execute(query)
            self.db.commit()

            result = self.cursor.rowcount

        except:
            pass
        return result

    def insert_object(self, tablename, column, value) :
        result = -1
        try :
            value_tmp = str(tuple(('%s' for i in range (0, len(column))))).replace('\'', '')
            
            query = f'''
            INSERT INTO {tablename}{str(tuple(column))}
            VALUES {value_tmp}
            '''
            self.cursor.execute(query, value)
            self.db.commit()

            result = self.cursor.rowcount

        except:
            pass
        return result

    def update(self, query) :
        result = -1
        try:
            self.cursor.execute(query)
            self.db.commit()

            result = self.cursor.rowcount
        except:
            pass
        return result
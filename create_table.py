import psycopg2
from psycopg2 import Error

try:
    
    connection = psycopg2.connect(database='postgres', user='gtripathi', password='QJdYWGAA6XqqU7bnF.PUr', host='hiring-quiz-database.cztyxuc8pfkm.ca-central-1.rds.amazonaws.com', port= '5432')

    cursor = connection.cursor()
    
    create_table_query = '''CREATE TABLE mobile
          (ID INT PRIMARY KEY     NOT NULL,
          MODEL           TEXT    NOT NULL,
          PRICE         REAL); '''
    
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

except (Exception, psycopg2.Error) as error :
    print("Failed to insert record into mobile table", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
import psycopg2

try:
   connection = psycopg2.connect(
   database='postgres', user='gtripathi', password='QJdYWGAA6XqqU7bnF.PUr', host='hiring-quiz-database.cztyxuc8pfkm.ca-central-1.rds.amazonaws.com', port= '5432')
   cursor = connection.cursor()

   postgres_insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)"""
   record_to_insert = (5, 'One Plus 6', 950)
   cursor.execute(postgres_insert_query, record_to_insert)

   connection.commit()
#    count = cursor.rowcount
#    sql ='''CREATE TABLE EMPLOYEE(
#    FIRST_NAME CHAR(20) NOT NULL,
#    LAST_NAME CHAR(20),
#    AGE INT,
#    SEX CHAR(1),
#    INCOME FLOAT)'''
#    cursor.execute(sql)
#    print("Table created successfully")
   count = cursor.rowcount

   print (count, "Record inserted successfully into mobile table")

except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to insert record into mobile table", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
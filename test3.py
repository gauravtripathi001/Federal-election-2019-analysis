import psycopg2

#Establishing the connection
conn = psycopg2.connect(
   database='postgres', user='gtripathi', password='QJdYWGAA6XqqU7bnF.PUr', host='hiring-quiz-database.cztyxuc8pfkm.ca-central-1.rds.amazonaws.com', port= '5432'
)
#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Doping EMPLOYEE table if already exists.
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

#Creating table as per requirement
sql ='''CREATE TABLE EMPLOYEE(
   FIRST_NAME CHAR(20) NOT NULL,
   LAST_NAME CHAR(20),
   AGE INT,
   SEX CHAR(1),
   INCOME FLOAT
)'''
cursor.execute(sql)
print("Table created successfully........")

#Closing the connection
conn.close()
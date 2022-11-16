import sqlite3
def create_db():
    con = sqlite3.connect(database=r'ems.db') #Making a database connection
    cur = con.cursor() #to execute any query, we have a kind of cursor which helps us execute those queries
    #cur.execute("CREATE TABLE IF NOT EXISTS employee()") # We are gonna create a table "employee" if the "employee" table doesnt exist


create_db()
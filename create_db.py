import sqlite3
def create_db():
    con = sqlite3.connect(database=r'ems.db') #Making a database connection
    cur = con.cursor() #to execute any query, we have a kind of cursor which helps us execute those queries
    
    cur.execute("CREATE TABLE IF NOT EXISTS suppliers(sid INTEGER PRIMARY KEY,name text,email text,pass text,utype text)") # We are gonna create a table "employee" if the "employee" table doesnt exist
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Category text,Supplier text,name text,qty text,Status text)") 
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS checkouts(chid INTEGER PRIMARY KEY AUTOINCREMENT,stname text,stcwid text,pname text,qty text)") 
    con.commit()
                    
                                                    
create_db()
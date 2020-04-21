import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "",
                           db = "myflaskapp")
    cur = conn.cursor()

    return cur, conn
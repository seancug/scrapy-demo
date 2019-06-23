from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

def do_upinsert(self, conn):
    print("ff")
    conn.execute("""
                 insert into Job_info(job_name, salary) values(%s, %s)""", ["hehe", "ddff"])
    print("finf")

dbargs = dict(
            host='localhost',
            db='JOB',
            user='root',
            passwd='SUNseanBO8.',
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
print("q")
dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
print("fffhhh")
dbpool.runInteraction(do_upinsert)
print("cccc")


import pymysql


class TimeDatabase:
    def __init__(self):
        self.db = None
        self.cur = None

    def connectDb(self):
        self.db = pymysql.connect(host='localhost',
                                  port=3306,
                                  user='',
                                  passwd='',
                                  db='world_db',
                                  charset='utf8')
        self.cur = self.db.cursor(pymysql.cursors.DictCursor)

    def closeDb(self):
        self.db.commit()
        self.db.close()

    def insertDb(self, year, month, day, time):
        sql = """
            INSERT INTO `world_db`.`datatime`
            (`year`,`month`,`day`,`time`)VALUES(%s, %s, %s, %s);
            """
        self.cur.execute(sql, (year, month, day, time))

    def executeAll(self):
        sql = "SELECT * FROM datatime;"
        self.cur.execute(sql)
        info = self.cur.fetchall()
        return info

    def inIt(self):
        sql = "TRUNCATE TABLE datatime;"
        self.cur.execute(sql)

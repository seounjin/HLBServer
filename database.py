import pymysql


class Database:
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

    def insertDb(self, country, totalCases, totalDeaths, totalRecovered):
        sql = """
            INSERT INTO `world_db`.`world`
            (`country`,`totalCases`,`totalDeaths`,`totalRecovered`)VALUES(%s, %s, %s, %s);
            """
        self.cur.execute(sql, (country, totalCases, totalDeaths, totalRecovered))

    def executeAll(self):
        sql = "SELECT * FROM world;"
        self.cur.execute(sql)
        worldList = self.cur.fetchall()
        return worldList

    def inIt(self):
        sql = "TRUNCATE TABLE world;"
        self.cur.execute(sql)

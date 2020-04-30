from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
import database
import timeDatabase
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)


sched = BackgroundScheduler(daemon=True)


@app.route('/world')
def world():
    db = database.Database()
    db.connectDb()
    worldInfo = db.executeAll()
    db.closeDb()

    timeDb = timeDatabase.TimeDatabase()
    timeDb.connectDb()

    timeInfo = timeDb.executeAll()
    timeDb.closeDb()

    json = {"time": timeInfo, "world": worldInfo}

    return jsonify(json)


def worldCrawling():
    doc = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(doc.text, "html.parser")
    data = soup.select("#main_table_countries_today > tbody > tr")

    worldData = []

    for datum in data:
        country = datum.find_all("td")[0].text.strip()
        totalCases = datum.find_all("td")[1].text.strip()
        newCases = datum.find_all("td")[2].text.strip()
        totalDeaths = datum.find_all("td")[3].text.strip()
        newDeaths = datum.find_all("td")[4].text.strip()
        totalRecovered = datum.find_all("td")[5].text.strip()

        if len(country) == 0:
            continue

        if country == "World" or country == "Total:":
            continue

        if len(totalCases) == 0:
            totalCases += '0'

        if len(totalDeaths) == 0:
            totalDeaths += '0'

        if len(totalRecovered) == 0:
            totalRecovered += '0'

        if len(newCases) == 0:
            newCases += "+0"

        if len(newDeaths) == 0:
            newDeaths += "+0"

        if country == "Europe" or country == "North America" or country == "Asia" or country == "South America" or country == "Africa" or country == "Oceania":
            continue

        worldData.append([country, totalCases + '\n' + newCases, totalDeaths + '\n' + newDeaths, totalRecovered])

    db = database.Database()
    db.connectDb()
    db.inIt()

    '''
    data[0] = country
    data[1] = totalCases + '\n' + newCases
    data[2] = totalDeaths + '\n' + newDeaths
    data[3] = totalRecovered
    '''

    for data in worldData:
        db.insertDb(data[0], data[1], data[2], data[3])

    db.closeDb()

    timeDb = timeDatabase.TimeDatabase()
    timeDb.connectDb()
    timeDb.inIt()

    # 실시간 정보
    dayInfo = soup.select("div.content-inner")
    dayData = dayInfo[0].find_all("div")[1].text.strip().split(' ')

    year = dayData[4][:4]
    month = monthTrans(dayData[2])
    day = dayData[3][:2]
    time = dayData[5]

    '''
    2020 04.29 10:35
    '''

    timeDb.insertDb(year, month, day, time)
    timeDb.closeDb()



# 24시간마다 실행
#sched.add_job(worldCrawling, 'interval', minutes=240)
sched.add_job(worldCrawling, 'interval', seconds=20)
sched.start()

def monthTrans(mon):
    if mon == "January":
        mon = "01"
    elif mon == "February":
        mon = "02"
    elif mon == "March":
        mon = "03"
    elif mon == "April":
        mon = "04"
    elif mon == "May":
        mon = "05"
    elif mon == "June":
        mon = "06"
    elif mon == "July":
        mon = "07"
    elif mon == "August":
        mon = "08"
    elif mon == "September":
        mon = "09"
    elif mon == "October":
        mon = "10"
    elif mon == "November":
        mon = "11"
    elif mon == "December":
        mon = "12"

    return mon


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
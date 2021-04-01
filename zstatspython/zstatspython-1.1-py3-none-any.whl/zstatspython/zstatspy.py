import mysql.connector

def connect(serverhost, username, passw, schemadatabase):
    db = mysql.connector.connect(
      host=serverhost,
      user=username,
      password=passw,
      database=schemadatabase
    )
    return db

def getStats(username, db):
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM stats.player WHERE name='%s'"%(username))
    for x in mycursor:
        uuid=x[0]
    sql="SELECT * FROM stats WHERE uuid='%s'" %(uuid)
    mycursor.execute(sql)
    stats = mycursor.fetchall()
    return stats
def getStatsfromUUID(UUID, db):
    mycursor = db.cursor()
    sql="SELECT * FROM stats WHERE uuid='%s'" %(UUID)
    mycursor.execute(sql)
    stats = mycursor.fetchall()
    return stats

def getStat(stat, username, db):
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM stats.player WHERE name='%s'"%(username))
    for x in mycursor:
        uuid=x[0]
    sql="SELECT * FROM stats WHERE uuid='%s' AND stat='%s'" %(uuid, stat)
    mycursor.execute(sql)
    stats = mycursor.fetchall()
    return stats   
    


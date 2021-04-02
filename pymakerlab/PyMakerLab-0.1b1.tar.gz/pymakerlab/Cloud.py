import pyrebase

config = {
    "apiKey": "AIzaSyAg_fo7CgCHhiXQM0CaMDlAykryglih3Ks",
    "authDomain": "chatandcloud.firebaseapp.com",
    "databaseURL": "https://chatandcloud.firebaseio.com",
    "projectId": "chatandcloud",
    "storageBucket": "chatandcloud.appspot.com",
    "messagingSenderId": "287513299386",
    "appId": "1:287513299386:web:72a0209a9ed1dbf388f583",
    "measurementId": "G-5TNSQR2HDY"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
print("WELCOME TO PYMAKERLAB CLOUD")
class PUBLIC_DB():
    def __init__():
        print("PUBLIC_DB INITIALIZED")
    def read(self, code):
        return db.child("public").child(code).get().val()
    def write(self, code, value):
        total = 0
        for i in code:
            total+=1
        if code[:2] == "P-" and total == 8:
            db.child("public").child(code).set(value)
        else:
            print("PUBLIC_DB ERROR: INVALID KEY. KEY FORMAT: P-'6 NUMBER CODE'")
        total = 0

class REGISTERED_DB():
    def __init__(self, login, password):
        try:
            check = db.child("registered").child(login).child("password").get().val()
            if check == password:
                self.user = login
                self.path = db.child("registered").child(login)
                print("REGISTERED_DB INITIALIZED")
            else:
                print("REGISTERED_DB ERROR: INCORRECT PASSWORD")
                print(password)
                print(db.child("registered").child(login).child("password").val())
        except:
            print("REGISTERED_DB ERROR: INCORRECT LOGIN")
    def read(self, code):
        return db.child("registered").child(self.user).child(code).get().val()
    def write(self, code, value):
        total = 0
        for i in code:
            total+=1
        if code[:2] == "R-" and total == 8:
            db.child("registered").child(self.user).child(code).set(value)
        else:
            print("PUBLIC_DB ERROR: INVALID KEY. KEY FORMAT: R-'6 NUMBER CODE'")
        total = 0

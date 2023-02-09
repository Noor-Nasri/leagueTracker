from pyrebase import pyrebase
from keys import firebase_config

if __name__ == "__main__":
    firebase = pyrebase.initialize_app(firebase_config)
    db = firebase.database()
    #data = {"name": "Mortimer 'Morty' Smith"}
    #db.child("users").push(data)

    print("Done")
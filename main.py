import pyrebase

config = {
  "apiKey": "apiKey",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "projectId.appspot.com"
}



if __name__ == "__main__":
    firebase = pyrebase.initialize_app(config)
    print("Hello world")
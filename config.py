from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {
        'DB': "tasks",
        'username':'task_prijindal',
        'password':'WaitForIt',
        'host':'ds059672.mongolab.com',
        'port':59672
        }
#app.config["MONGODB_SETTINGS"] = {'DB':'task'}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()

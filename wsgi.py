from flask import Flask
application = Flask(__name__)

@application.route("/<string:arg1>")
def hello(arg1):
    if arg1:
        return "Hello my main daimie! %s"%arg1
    else:
        return "Hello World!"

if __name__ == "__main__":
    application.run()

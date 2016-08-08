from flask import Flask
from flask import request
application = Flask(__name__)

# @application.route("/health")
# def health():
#     return 'working'

@application.route("/", methods=['GET'])
def hello():
    if request.args.get('q', ""):
        return "Hello my main daimie! %s"%(request.args.get('q', ""),)
    else:
        return "Hello World!"

if __name__ == "__main__":
    application.run()

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve

from Controllers.CandidatesController import CandidatesController
candidatesController = CandidatesController()

from Controllers.TablesController import TablesController
tablesController = TablesController()

from Controllers.PartiesController import PartiesController
partiesController = PartiesController()

from Controllers.ResultsController import ResultController
resultsController = ResultController()

app = Flask(__name__)
cors = CORS(app)

# Candidates
@app.route("/candidates", methods=["GET"])
def getCandidates():
    res = candidatesController.getAll()
    return jsonify(res)

@app.route("/candidates", methods=["POST"])
def createCandidate():
    data = request.get_json()
    res = candidatesController.create(data)
    return jsonify(res)

@app.route("/candidates/<string:id>", methods=["GET"])
def getCandidate(id):
    res = candidatesController.getCandidate(id)
    return jsonify(res)
@app.route("/candidates/<string:id>", methods=["PUT"])
def updateCandidate(id):
    data = request.get_json()
    res = candidatesController.update(id, data)
    return jsonify(res)

@app.route("/candidates/<string:id>", methods=["DELETE"])
def deleteCandidate(id):
    res = candidatesController.delete(id)
    return jsonify(res)

@app.route("/candidates/<string:id>/party/<string:idParty>", methods=["PUT"])
def assingidParty(id, idParty):
    res = candidatesController.assignParty(id, idParty)
    return jsonify(res)

# Parties

@app.route("/parties", methods=["GET"])
def getParties():
    res = partiesController.getAll()
    return jsonify(res)

@app.route("/parties", methods=["POST"])
def createPartie():
    data = request.get_json()
    res = partiesController.create(data)
    return jsonify(res)

@app.route("/parties/<string:id>", methods=["GET"])
def getPartie(id):
    res = partiesController.getById(id)
    return jsonify(res)
@app.route("/parties/<string:id>", methods=["PUT"])
def updatePartie(id):
    data = request.get_json()
    res = partiesController.update(id, data)
    return jsonify(res)

@app.route("/parties/<string:id>", methods=["DELETE"])
def deletePartie(id):
    res = partiesController.delete(id)
    return jsonify(res)

# Results

@app.route("/results", methods=["GET"])
def getResults():
    res = resultsController.getAll()
    return jsonify(res)

@app.route("/results/<string:id>", methods=["GET"])
def getResult(id):
    res = resultsController.getById(id)
    return jsonify(res)

@app.route("/results/<string:idTable>/candidate/<string:idCandidate>", methods=["POST"])
def newResult(idTable,idCandidate):
    data = request.get_json()
    res = resultsController.create(data, idTable, idCandidate)
    return jsonify(res)

@app.route("/results/<string:id>/table/<string:idTable>/candidate/<string:idCandidate>", methods=["PUT"])
def updateResult(id, idTable, idCandidate):
    data = request.get_json()
    res = resultsController.update(id, data, idTable, idCandidate)
    return jsonify(res)

@app.route("/results/<string:id>", methods=["DELETE"])
def deleteResult(id):
    res = resultsController.delete(id)
    return jsonify(res)

# Tables

@app.route("/tables", methods=["GET"])
def getTables():
    res = tablesController.getAll()
    return jsonify(res)

@app.route("/tables", methods=["POST"])
def createTable():
    data = request.get_json()
    res = tablesController.create(data)
    return jsonify(res)

@app.route("/tables/<string:id>", methods=["GET"])
def getTable(id):
    res = tablesController.getById(id)
    return jsonify(res)
@app.route("/tables/<string:id>", methods=["PUT"])
def updateTable(id):
    data = request.get_json()
    res = tablesController.update(id, data)
    return jsonify(res)

@app.route("/tables/<string:id>", methods=["DELETE"])
def deleteTable(id):
    res = tablesController.delete(id)
    return jsonify(res)

def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["dev"]+":" + str(dataConfig["port"]))
    serve(app,host=dataConfig["dev"], port=dataConfig["port"])

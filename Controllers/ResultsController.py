from Repositories.ResultsRepository import ResultsRepository as repository
from Models.Results import Results as Model
from Models.Tables import Tables
from Models.Candidates import Candidates
from Repositories.TablesRepository import TablesRepository
from Repositories.CandidatesRepository import CandidatesRepository

class ResultController:
    def __init__(self):
        self.repository = repository()
        self.tablesRepository = TablesRepository()
        self.candidatesRepository = CandidatesRepository()

    def getAll(self):
        return self.repository.getAll()

    def getById(self, id):
        res = Model(self.repository.findById(id))
        return res.__dict__

    def create(self, data, idTable, idCandidate):
        res = Model(data)
        table = Tables(self.tablesRepository.findById(idTable))
        candidate = Candidates(self.candidatesRepository.findById(idCandidate))
        res.table = table
        res.candidate = candidate
        return self.repository.create(res)

    def update(self, id, data, idTable, idCandidate):
        updated = Model(self.repository.findById(id))
        table = Tables(self.tablesRepository.findById(idTable))
        updated.table = table
        candidate = Candidates(self.candidatesRepository.findById(idCandidate))
        updated.candidate = candidate
        updated.elections = data['elections']
        updated.result = data['result']

        return self.repository.create(updated)

    def delete(self, id):
        return self.repository.delete(id)



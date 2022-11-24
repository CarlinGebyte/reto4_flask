from Models.Candidates import Candidates
from Models.Parties import Parties
from Repositories.CandidatesRepository import CandidatesRepository
from Repositories.PartiesRepository import PartiesRepository


class CandidatesController():
    def __init__(self):
        self.candidatesRepository = CandidatesRepository()
        self.partiesRepository = PartiesRepository()

    def getAll(self):
        return self.candidatesRepository.getAll()

    def create(self, candidate):
        new = Candidates(candidate)
        return self.candidatesRepository.create(new)

    def getCandidate(self, id):
        candidate = Candidates(self.candidatesRepository.findById(id))
        return candidate.__dict__

    def update(self, id, update):
        updated = Candidates(self.candidatesRepository.findById(id))
        updated.name = update["name"]
        return self.candidatesRepository.create(updated)

    def delete(self, id):
        return self.candidatesRepository.delete(id)

    def assignParty(self, id, idParty):
        res = Candidates(self.candidatesRepository.findById(id))
        party = Parties(self.partiesRepository.findById(idParty))
        res.party = party
        return self.candidatesRepository.create(res)

from Repositories.PartiesRepository import PartiesRepository as repository
from Models.Parties import Parties as Model

class PartiesController:
    def __init__(self):
        self.repository = repository()

    def getAll(self):
        return self.repository.getAll()

    def getById(self, id):
        res = Model(self.repository.findById(id))
        return res.__dict__

    def create(self, data):
        res = Model(data)
        return self.repository.create(res)

    def update(self, id, data):
        updated = Model(self.repository.findById(id))
        updated.name = data['name']
        updated.description = data['description']
        return self.repository.create(updated)

    def delete(self, id):
        return self.repository.delete(id)
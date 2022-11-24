from Repositories.TablesRepository import TablesRepository as repository
from Models.Tables import Tables as Model

class TablesController:
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
        updated.number = data['number']
        updated.location = data['location']
        return self.repository.create(updated)

    def delete(self, id):
        return self.repository.delete(id)

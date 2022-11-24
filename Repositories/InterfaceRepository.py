import json
from typing import TypeVar, Generic, get_args, get_origin

import certifi
import pymongo
from bson import DBRef
from bson.objectid import ObjectId

T = TypeVar('T')


class InterfaceRepository(Generic[T]):
    def __init__(self):
        ca = certifi.where()
        dataConfig = self.loadFileConfig()
        client = pymongo.MongoClient(dataConfig['mongo-string'], tlsCAFile=ca)
        self.db = client[dataConfig["db"]]
        model = get_args(self.__orig_bases__[0])
        self.collection = model[0].__name__.lower()

    def loadFileConfig(self):
        with open('config.json') as f:
            data = json.load(f)
        return data

    def create(self, item: T):
        collection = self.db[self.collection]
        id = ""
        item = self.transformRefs(item)
        if hasattr(item, "_id") and item._id != "":
            id = item._id
            _id = ObjectId(id)
            collection = self.db[self.collection]
            delattr(item, "_id")
            item = item.__dict__
            updateItem = {"$set": item}
            x = collection.update_one({"_id": _id}, updateItem)
        else:
            _id = collection.insert_one(item.__dict__)
            id = _id.inserted_id.__str__()
        x = collection.find_one({"_id": ObjectId(id)})
        x["_id"] = x["_id"].__str__()
        return self.findById(id)

    def delete(self, id):
        collection = self.db[self.collection]
        deleted = collection.delete_one({"_id": ObjectId(id)}).deleted_count
        return {"deleted_count": deleted}

    def update(self, id, item: T):
        _id = ObjectId(id)
        collection = self.db[self.collection]
        delattr(item, "_id")
        item = item.__dict__
        update = {"$set": item}
        x = collection.update_one({"_id": id}, update)
        return {"updated_count": x.matched_count}

    def findById(self, id):
        collection = self.db[self.collection]
        x = collection.find_one({"_id": ObjectId(id)})
        x = self.getValuesDBRef(x)
        if x == None:
            x = {}
        else:
            x["_id"] = x["_id"].__str__()
        return x

    def getAll(self):
        collection = self.db[self.collection]
        data = []
        for x in collection.find():
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

    def query(self, q):
        collection = self.db[self.collection]
        data = []
        for x in collection.find(q):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

    def queryAggregation(self, q):
        collection = self.db[self.collection]
        data = []
        for x in collection.aggregate(q):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

    def getValuesDBRef(self, x):
        keys = x.keys()
        for k in keys:
            if isinstance(x[k], DBRef):
                collection = self.db[x[k].collection]
                value = collection.find_one({"_id": ObjectId(x[k].id)})
                value["_id"] = value["_id"].__str__()
                x[k] = value
                x[k] = self.getValuesDBRef(x[k])
            elif isinstance(x[k], list) and len(x[k]) > 0:
                x[k] = self.getValuesDBRefFromList(x[k])
            elif isinstance(x[k], dict):
                x[k] = self.getValuesDBRef(x[k])
        return x

    def getValuesDBRefFromList(self, l):
        new = []
        collection = self.db[self.collection]
        for i in l:
            value = collection.find_one({"_id": ObjectId(i.id)})
            value["_id"] = value["_id"].__str__()
            new.append(value)
        return new

    def transformObjectIds(self, x):
        for attribute in x.keys():
            if isinstance(x[attribute], ObjectId):
                x[attribute] = x[attribute].__str__()
            elif isinstance(x[attribute], list):
                x[attribute] = self.formatList(x[attribute])
            elif isinstance(x[attribute], dict):
                x[attribute] = self.transformObjectIds(x[attribute])
        return x

    def formatList(self, x):
        new = []
        for i in x:
            if isinstance(i, ObjectId):
                new.append(i.__str__())
        if len(new) == 0:
            new = x
        return new

    def transformRefs(self, item):
        new = item.__dict__
        keys = list(new.keys())
        for k in keys:
            if new[k].__str__().count("object") == 1:
                newObject = self.ObjectToRefs(getattr(item, k))
                setattr(item, k, newObject)
        return item

    def ObjectToRefs(self, item: T):
        collectionName = item.__class__.__name__.lower()
        return DBRef(collectionName, ObjectId(item._id))
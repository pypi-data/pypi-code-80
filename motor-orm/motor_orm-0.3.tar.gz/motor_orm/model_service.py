from typing import Generic, List, Optional, Type, TypeVar

from bson import ObjectId  # type: ignore

from motor_orm.db import Database
from motor_orm.model import Model

T = TypeVar("T", bound=Model)


class ModelServiceBase(Generic[T]):
    model: Type[T]
    collection_name: Optional[str] = None

    @classmethod
    def _get_collection_name(cls):
        return cls.collection_name or cls.model.__name__

    def __init__(self, db: Database):
        self.db = db
        self.client = db.client
        self.collection_name = self._get_collection_name()
        self.collection = self.client[self.collection_name]


class ModelService(ModelServiceBase):
    @classmethod
    def _model_to_db(cls, model: T) -> dict:
        return model.dict(by_alias=True)

    @classmethod
    def _db_to_model(cls, data: dict) -> T:
        return cls.model(**data)

    async def create_collection(self):
        """
        Create custom indexes etc...
        """
        pass

    async def get_by_id(self, _id: ObjectId) -> Optional[T]:
        return await self.find_one({"_id": _id})

    async def find_one(self, filters: dict) -> Optional[T]:
        doc = await self.collection.find_one(filters)
        if doc is None:
            return None
        return self._db_to_model(doc)

    async def insert_one(self, model: T) -> ObjectId:
        doc = self._model_to_db(model)

        if '_id' in doc and doc.get('_id', None) is None:
            doc.pop('_id')

        insert_result = await self.collection.insert_one(doc)
        return insert_result.inserted_id

    async def insert_many(self, models: List[T]) -> List[ObjectId]:
        docs: List[dict] = []

        for m in models:
            doc = self._model_to_db(m)
            if '_id' in doc and doc.get('_id', None) is None:
                doc.pop('_id')
            docs.append(doc)

        insert_result = await self.collection.insert_many(docs)
        return insert_result.inserted_ids
